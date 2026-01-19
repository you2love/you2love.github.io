内存泄漏在Go中表现为：进程的堆内存占用持续增长，即使在业务低峰期也不回落，最终可能导致OOM（内存溢出）。

---

## 一、未正确终止的Goroutine（最常见）
### 核心原因
Goroutine是Go中最主要的内存泄漏来源。只要Goroutine不退出，它占用的栈、堆内存，以及引用的所有变量都无法被GC回收。常见触发场景：
- Goroutine阻塞在`chan`的接收/发送操作，且无其他协程唤醒；
- Goroutine陷入死循环（无退出条件）；
- Goroutine等待一个永远不会触发的锁/条件变量。

### 代码示例（chan阻塞导致泄漏）
```go
// 错误示例：启动的goroutine阻塞在chan接收，且无发送方，永久无法退出
func leakGoroutine() {
    ch := make(chan int)
    // 启动协程后，ch永远没有发送方，协程一直阻塞，内存泄漏
    go func() {
        val := <-ch // 阻塞在此处，协程永不退出
        fmt.Println("received:", val)
    }()
    // 函数返回后，ch无外部引用，但协程仍持有ch的引用，无法回收
}

func main() {
    for i := 0; i < 10000; i++ {
        leakGoroutine() // 循环调用，创建1万个泄漏的goroutine
    }
    // 阻塞主线程，观察内存占用
    select {}
}
```

### 解决方案
1. **使用带超时的chan操作**：通过`context.WithTimeout`或`time.After`设置超时，避免永久阻塞；
2. **显式关闭chan**：确保发送方/接收方有退出逻辑；
3. **使用context传递取消信号**：强制终止协程。

### 修复后的代码
```go
func fixedGoroutine(ctx context.Context) {
    ch := make(chan int, 1) // 可选：用缓冲chan减少阻塞概率
    go func() {
        select {
        case val := <-ch:
            fmt.Println("received:", val)
        case <-ctx.Done(): // 监听取消信号，触发时退出协程
            fmt.Println("goroutine exit:", ctx.Err())
            return
        }
    }()
    // 业务逻辑：若无需发送，主动取消
    ch <- 1 // 可选：发送数据
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel() // 函数退出时取消所有协程
    
    for i := 0; i < 10000; i++ {
        fixedGoroutine(ctx)
    }
    time.Sleep(1 * time.Second) // 等待协程退出
    fmt.Println("all goroutines exited")
}
```

---

## 二、未停止的time.Ticker/未释放的time.Timer
### 核心原因
- `time.Ticker`：创建后会启动一个后台协程，持续向`C`通道发送时间事件，若不调用`Stop()`，该协程永久运行，内存泄漏；
- `time.Timer`：若未触发（`Reset`）或未停止（`Stop`），且`Timer`对象被引用，会导致底层资源无法回收（注：未引用的Timer会被GC回收，但不推荐依赖此行为）。

### 代码示例（Ticker未Stop导致泄漏）
```go
func leakTicker() {
    // 创建Ticker，每100ms触发一次
    ticker := time.NewTicker(100 * time.Millisecond)
    // 仅读取一次，未调用Stop()，Ticker协程永久运行
    <-ticker.C
    fmt.Println("ticker once")
    // 函数返回后，ticker未Stop，后台协程持续运行
}

func main() {
    for i := 0; i < 100; i++ {
        leakTicker() // 创建100个未停止的Ticker
    }
    select {}
}
```

### 解决方案
1. **Ticker必须显式Stop**：在不再使用时调用`ticker.Stop()`；
2. **Timer使用后及时Stop/Reset**：即使Timer已触发，也建议调用`Stop()`（无副作用）；
3. **结合context使用**：通过context控制Ticker的生命周期。

### 修复后的代码
```go
func fixedTicker(ctx context.Context) {
    ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop() // 延迟调用Stop，确保函数退出时停止Ticker
    
    go func() {
        for {
            select {
            case <-ticker.C:
                fmt.Println("ticker tick")
            case <-ctx.Done():
                return // 监听取消信号，退出协程
            }
        }
    }()
}
```

---

## 三、全局集合（map/slice）无限增长
### 核心原因
全局的`map`、`slice`（或包级别的集合）若只添加元素、不删除/清理，会导致集合占用的内存持续增长，且集合引用的所有元素都无法被GC回收。

### 代码示例（全局map泄漏）
```go
// 全局map，存储所有请求的日志，永不清理
var globalLogMap = make(map[string]interface{})

// 记录日志，但从不删除
func logRequest(id string, data interface{}) {
    globalLogMap[id] = data // 只增不减，map无限膨胀
}

func main() {
    // 模拟持续接收请求，向全局map添加数据
    for i := 0; ; i++ {
        id := fmt.Sprintf("req-%d", i)
        // 每个请求存储1KB数据，持续占用内存
        data := make([]byte, 1024)
        logRequest(id, data)
        time.Sleep(1 * time.Millisecond)
    }
}
```

### 解决方案
1. **设置过期策略**：定期清理过期元素（如用`time.Ticker`定时删除）；
2. **使用带容量限制的集合**：当集合大小超过阈值时，触发清理（如LRU缓存）；
3. **避免全局集合**：尽量将集合的生命周期限制在函数/请求内；
4. **使用第三方缓存库**：如`github.com/hashicorp/golang-lru`（LRU缓存），自动淘汰过期数据。

### 修复后的代码
```go
import (
    "sync"
    "time"
)

type ExpirableMap struct {
    mu    sync.RWMutex
    data  map[string]item
    ticker *time.Ticker
}

type item struct {
    value     interface{}
    expireAt  time.Time
}

// 初始化带过期清理的map
func NewExpirableMap(cleanupInterval time.Duration) *ExpirableMap {
    m := &ExpirableMap{
        data:  make(map[string]item),
        ticker: time.NewTicker(cleanupInterval),
    }
    // 启动清理协程
    go m.cleanup()
    return m
}

// 清理过期元素
func (m *ExpirableMap) cleanup() {
    for range m.ticker.C {
        m.mu.Lock()
        now := time.Now()
        for id, item := range m.data {
            if now.After(item.expireAt) {
                delete(m.data, id) // 删除过期元素
            }
        }
        m.mu.Unlock()
    }
}

// 添加元素，设置1分钟过期
func (m *ExpirableMap) Set(id string, value interface{}) {
    m.mu.Lock()
    defer m.mu.Unlock()
    m.data[id] = item{
        value:    value,
        expireAt: time.Now().Add(1 * time.Minute),
    }
}

// 全局实例
var globalLogMap = NewExpirableMap(30 * time.Second)
```

---

## 四、切片截取导致的底层数组泄漏
### 核心原因
切片的底层是数组，当你从一个**大切片**截取一个**小切片**时，小切片会引用整个底层大数组。即使大切片无其他引用，只要小切片存在，整个大数组就无法被GC回收，导致内存泄漏。

### 代码示例
```go
func leakSlice() []int {
    // 创建一个100MB的大切片（100*1024*1024个int，每个int8字节）
    bigSlice := make([]int, 100*1024*1024)
    // 截取最后1个元素，返回小切片
    smallSlice := bigSlice[len(bigSlice)-1:]
    // 函数返回后，bigSlice被销毁，但smallSlice引用底层大数组，100MB内存泄漏
    return smallSlice
}

func main() {
    // 保存小切片，导致大数组无法回收
    leakySlice := leakSlice()
    fmt.Println("leaky slice len:", len(leakySlice))
    select {}
}
```

### 解决方案
1. **复制切片**：使用`copy`创建新切片，切断对原底层数组的引用；
2. **显式置空原切片**：若无需保留原切片，手动将其置为`nil`（加速GC）。

### 修复后的代码
```go
func fixedSlice() []int {
    bigSlice := make([]int, 100*1024*1024)
    smallSlice := make([]int, 1)
    // 复制最后1个元素到新切片，新切片的底层数组仅1个元素
    copy(smallSlice, bigSlice[len(bigSlice)-1:])
    bigSlice = nil // 显式置空，帮助GC回收大数组
    return smallSlice
}
```

---

## 五、闭包引用导致的变量无法回收
### 核心原因
闭包会捕获外部变量的引用，若闭包的生命周期远长于外部变量的预期生命周期，会导致外部变量（及引用的资源）无法被GC回收。

### 代码示例
```go
func leakClosure() func() {
    // 大对象，预期仅在函数内使用
    bigData := make([]byte, 100*1024*1024)
    // 闭包引用bigData，即使函数返回，bigData也无法被回收
    return func() {
        fmt.Println("len of bigData:", len(bigData)) // 仅引用，无实际用途
    }
}

func main() {
    // 保存闭包，导致bigData持续占用100MB内存
    f := leakClosure()
    // 即使不调用f，bigData也无法回收
    time.Sleep(10 * time.Second)
    f() // 调用闭包
    select {}
}
```

### 解决方案
1. **避免闭包引用不必要的大变量**：仅引用需要的字段，而非整个大对象；
2. **复制变量到闭包内**：切断对外部大变量的引用；
3. **显式置空引用**：在闭包使用完后，将引用置为`nil`。

### 修复后的代码
```go
func fixedClosure() func() {
    bigData := make([]byte, 100*1024*1024)
    // 复制需要的值到闭包内，不引用整个bigData
    dataLen := len(bigData)
    // 闭包仅引用dataLen，bigData可被GC回收
    return func() {
        fmt.Println("len of bigData:", dataLen)
    }
}
```

---

## 六、sync.Pool使用不当
### 核心原因
`sync.Pool`是Go提供的对象池，用于复用临时对象、减少GC压力，但使用不当会导致泄漏：
- 向Pool中存入**大对象/长生命周期对象**：Pool的回收策略由GC控制，若对象过大，会导致Pool占用大量内存；
- 依赖Pool存储关键数据：Pool中的对象可能被GC随时清理，但若错误地将Pool作为持久存储，会导致逻辑错误+内存泄漏。

### 解决方案
1. **仅用Pool存储临时、高频创建的小对象**（如临时缓冲区、请求上下文）；
2. **不要存储长生命周期对象**：Pool适合“创建成本高、使用频率高”的临时对象；
3. **设置对象池的大小限制**：自定义Pool的`New`函数，避免无限制创建对象。

---

## 七、外部资源未关闭
### 核心原因
Go的GC仅回收内存，不会自动关闭文件句柄、网络连接、数据库连接等外部资源。若这些资源未关闭：
- 操作系统会为每个资源分配文件描述符（FD），FD耗尽会导致进程无法创建新连接/文件；
- 部分资源（如数据库连接）会占用内存，未关闭会导致内存泄漏。

### 常见未关闭的资源
- 文件/目录：`os.Open`/`os.Create`后未调用`Close()`；
- 网络连接：`net.Dial`/`http.Client`请求后未关闭响应体（`resp.Body.Close()`）；
- 数据库连接：未关闭`sql.DB`/`redis.Client`的连接；
- 管道/锁：`os/exec`的`Cmd`未关闭`Stdout`/`Stderr`。

### 代码示例（HTTP响应体未关闭）
```go
func leakHTTP() {
    resp, err := http.Get("https://example.com")
    if err != nil {
        fmt.Println(err)
        return
    }
    // 错误：未关闭resp.Body，导致连接/内存泄漏
    body, _ := io.ReadAll(resp.Body)
    fmt.Println("body len:", len(body))
}
```

### 解决方案
1. **使用defer关闭资源**：遵循“打开即延迟关闭”原则；
2. **检查所有分支**：确保错误分支也关闭资源；
3. **使用`context`控制资源生命周期**：超时自动关闭资源。

### 修复后的代码
```go
func fixedHTTP() {
    resp, err := http.Get("https://example.com")
    if err != nil {
        fmt.Println(err)
        return
    }
    defer resp.Body.Close() // 延迟关闭响应体，确保所有分支都执行
    body, _ := io.ReadAll(resp.Body)
    fmt.Println("body len:", len(body))
}
```

---

## 如何检测Go内存泄漏？
除了代码审查，还可以通过工具快速定位：
1. **pprof**：Go内置的性能分析工具，通过`go tool pprof`分析堆内存（`-inuse_space`）和goroutine数量；
   ```bash
   # 启动程序时开启pprof
   go run main.go -pprof=:6060
   # 访问http://localhost:6060/debug/pprof/，查看heap/goroutine/profile
   ```
2. **trace**：分析goroutine的生命周期，定位阻塞的goroutine；
3. **第三方工具**：如`gops`（查看进程状态）、`go-torch`（火焰图）。

---

### 总结
1. **最核心泄漏源**：未终止的Goroutine（尤其是chan阻塞），需通过`context`/超时机制确保协程可退出；
2. **高频场景**：未Stop的`time.Ticker`、全局集合无限增长、切片截取导致的底层数组泄漏；
3. **通用避坑原则**：
   - 所有资源（文件、连接、Ticker）遵循“打开即延迟关闭”；
   - 避免全局集合只增不减，设置过期/容量限制；
   - 协程必须有明确的退出条件（context/超时/chan关闭）。