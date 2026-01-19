## 一、slice（切片）核心结构

**slice并非原生数组，而是对底层数组的轻量级封装**，本质是"动态数组"，核心由`SliceHeader`结构体实现，源码定义于`runtime/slice.go`和`reflect/value.go`。

### 1. 核心结构体：SliceHeader

slice的底层是包含三个字段的结构体，`reflect`包将其暴露为`SliceHeader`，运行时内部逻辑等价结构体为`slice`，简化定义如下：

```go
// reflect包暴露的切片头部结构
type SliceHeader struct {
    Data uintptr // 指向底层数组的指针（核心：slice是对数组的引用）
    Len  int     // 切片长度（len(s)返回值，当前可访问元素个数）
    Cap  int     // 切片容量（cap(s)返回值，底层数组的可用空间）
}

// 运行时内部slice结构体（与SliceHeader语义一致）
type slice struct {
    array unsafe.Pointer // 指向底层数组的指针
    len   int            // 长度
    cap   int            // 容量
}
```

**关键字段解析**：

- **Data/array**：最核心字段，指向底层连续内存数组，slice所有操作最终作用于该数组
- **Len**：当前可访问元素数量，访问`s[len(s)]`会触发越界panic
- **Cap**：底层数组从Data指针开始的总可用空间，恒满足`Cap ≥ Len`

### 2. 核心工作机制

#### 切片操作（s[low:high]）：共享底层数组

切片操作不会复制底层数组，仅创建新的slice结构体，新结构体与原slice共享底层数组：

- 新slice的Data指针指向原底层数组的low索引位置
- 新slice的Len = high - low
- 新slice的Cap = 原Cap - low

```go
func main() {
    s1 := []int{1,2,3,4,5} // len=5, cap=5，底层数组[1,2,3,4,5]
    s2 := s1[1:3]           // len=2, cap=4，共享原底层数组
    s2[0] = 99              // 修改新切片元素，影响原切片
    fmt.Println(s1) // 输出 [1,99,3,4,5]
    fmt.Println(s2) // 输出 [99,3]
}
```

#### 扩容机制（append触发）

当`append`添加元素导致`Len == Cap`时，触发扩容，核心逻辑：

1. **计算新容量**：原容量<1024时翻倍，≥1024时增长25%，最终按元素类型内存对齐微调
2. **创建新数组**：分配对应新容量的连续内存
3. **拷贝数据**：将原底层数组元素拷贝至新数组
4. **更新结构体**：新slice的Data指向新数组，Len为原Len+1，Cap为新容量

**⚠️ 陷阱**：扩容后原slice仍指向旧数组，新slice指向新数组，二者不再共享数据。

#### nil slice vs 空slice

二者Len和Cap均为0，但Data指针状态不同：

- **nil slice**：Data=nil，未指向任何数组（如`var s []int`）
- **空slice**：Data≠nil，指向空底层数组（如`s := []int{}`或`make([]int, 0)`）

### 3. 关键特性

- **引用类型**：slice本身是值类型（结构体拷贝），但Data指针共享底层数组，传参时修改元素会影响原切片
- **长度/容量分离**：Len限制访问范围，Cap限制扩容基础，append优先使用空闲空间
- **连续内存**：底层数组连续，随机访问效率O(1)，扩容伴随拷贝开销
- **越界检查**：访问index≥Len触发panic，Cap范围内空间可通过`s[:cap(s)]`暴露

---

## 二、map（哈希表）核心结构

map基于哈希表实现，核心由`hmap`（顶层管理结构）和`bmap`（桶结构）组成，源码定义于`runtime/map.go`。

### 1. 核心结构体

#### hmap（哈希表顶层管理结构）

负责管理map元数据和桶数组，简化定义：

```go
type hmap struct {
    count     int           // 实际存储的键值对数量（len(map)返回值）
    B         uint8         // 桶数组大小指数，桶总数=2^B
    hash0     uint32        // 哈希种子，增加哈希值随机性
    buckets   unsafe.Pointer // 指向正常状态的桶数组
    oldbuckets unsafe.Pointer // 扩容时指向旧桶数组（双桶共存）
    nevacuate uintptr       // 扩容时搬迁进度标记
}
```

#### bmap（桶，存储键值对的最小单元）

单个bmap默认存储8个键值对，结构优化内存对齐，简化逻辑结构：

```go
type bmap struct {
    tophash [8]uint8  // 存储每个键哈希值的高8位，用于快速匹配
    // 内存布局：8个key → 8个value → overflow指针（指向溢出桶）
}
```

**关键字段解析**：

- **hmap.count**：直接对应len(map)，O(1)获取
- **hmap.B**：动态调整，平衡哈希冲突与内存占用
- **hmap.oldbuckets**：扩容期间临时存储旧桶，搬迁完成后置空
- **bmap.tophash**：快速过滤不匹配key，减少全量哈希对比
- **bmap.overflow**：桶满时链接溢出桶，形成链表

### 2. 核心工作流程（查找/插入）

1. **计算哈希值**：以hmap.hash0为种子，计算key的64位（32位系统32位）哈希值
2. **定位桶**：取哈希值低B位计算索引，找到对应bmap
3. **匹配key**：对比bmap.tophash（哈希高8位），匹配后验证key本身，无匹配则检查溢出桶
4. **扩容触发**：负载因子（count/2^B）超过6.5，或溢出桶过多时触发，分倍数扩容（桶数翻倍）和等量扩容（仅搬迁数据）

### 3. 关键特性

- **并发不安全**：无锁保护，多协程同时读写会触发panic
- **key可比较性**：key必须支持哈希和相等判断，slice、map、func不可作为key
- **内存高效**：key/value连续存储优化内存对齐，提升CPU缓存命中率
- **渐进式扩容**：扩容时逐步搬迁数据，避免单次操作耗时过长

---

## 三、channel（通道）核心结构

channel是goroutine间安全通信的同步原语，底层由`hchan`结构体实现，本质是"带锁的环形队列+等待队列"，源码定义于`runtime/chan.go`。

### 1. 核心结构体：hchan

hchan包含类型元数据、缓冲区、同步锁、等待队列四大核心部分，简化定义：

```go
type hchan struct {
    elemtype *_type // 元素类型信息，保证类型安全
    elemsize uint16 // 单个元素字节大小
    closed   uint32 // 关闭标记：0未关闭，1已关闭
    dataqsiz uint64  // 缓冲区容量（make(chan T, N)中的N）
    buf      unsafe.Pointer // 指向环形队列的指针
    sendx    uint64  // 环形队列写指针
    recvx    uint64  // 环形队列读指针
    qcount   uint64  // 缓冲区当前元素数量
    lock mutex       // 互斥锁，保证并发安全
    sendq waitq      // 发送者等待队列（因满阻塞的goroutine）
    recvq waitq      // 接收者等待队列（因空阻塞的goroutine）
}

// 等待队列结构
type waitq struct {
    first *sudog // 队列头
    last  *sudog // 队列尾
}

// 封装阻塞的goroutine
type sudog struct {
    g          *g     // 阻塞的goroutine
    elem       unsafe.Pointer // 元素数据指针
    next, prev *sudog // 链表节点指针
}
```

### 2. 核心工作流程

#### 无缓冲channel（make(chan T)）

dataqsiz=0，无缓冲区，核心是goroutine直接配对：

- **发送流程**：检查recvq有接收者则直接拷贝值并唤醒，无则封装发送者加入sendq并挂起
- **接收流程**：检查sendq有发送者则直接拷贝值并唤醒，无则封装接收者加入recvq并挂起

#### 有缓冲channel（make(chan T, N)）

优先使用环形队列存储数据，仅满/空时阻塞：

- **发送流程**：缓冲区未满则写入数据并移动写指针，已满则加入sendq挂起
- **接收流程**：缓冲区非空则读取数据并移动读指针，为空则加入recvq挂起

#### 关闭channel（close(ch)）

1. **加锁**并将closed置为1
2. **唤醒recvq所有接收者**（读到零值+关闭标识）
3. **唤醒sendq所有发送者**（触发panic）
4. **解锁并清理资源**

### 3. 关键特性

- **并发安全**：lock互斥锁保证所有操作原子性，多协程读写安全
- **类型安全**：elemtype和elemsize确保发送/接收类型一致，编译期校验
- **阻塞特性**：无缓冲同步通信，有缓冲异步通信，依赖等待队列实现阻塞唤醒
- **关闭后行为**：关闭后发送panic，接收先读缓冲区再返回零值

---

## 四、总结

- **slice**：基于底层数组的轻量封装，核心是SliceHeader三字段，依赖扩容实现动态增长，共享底层数组需注意数据污染
- **map**：哈希表实现，hmap管理桶数组，bmap存储键值对，通过溢出桶和渐进式扩容平衡性能与内存
- **channel**：带锁环形队列+等待队列，通过锁保证并发安全，通过等待队列实现goroutine阻塞唤醒，分有缓冲/无缓冲两种通信模式