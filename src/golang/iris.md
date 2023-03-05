---
# iris
---


### context中断原理

***

```golang
// I don't set to a max value because we want to be able to reuse the handlers even if stopped with .Skip
const stopExecutionIndex = -1 

// StopExecution if called then the following .Next calls are ignored,
// as a result the next handlers in the chain will not be fire.
func (ctx *context) StopExecution() {
 ctx.currentHandlerIndex = stopExecutionIndex
}

// IsStopped checks and returns true if the current position of the context is -1,
// means that the StopExecution() was called.
func (ctx *context) IsStopped() bool {
 return ctx.currentHandlerIndex == stopExecutionIndex
}

func DefaultNext(ctx Context) {
 if ctx.IsStopped() {
  return
 }
 if n, handlers := ctx.HandlerIndex(-1)+1, ctx.Handlers(); n < len(handlers) {
  ctx.HandlerIndex(n)
  handlers[n](ctx)
 }
}

func (ctx *context) HandlerIndex(n int) (currentIndex int) {
 if n < 0 || n > len(ctx.handlers)-1 {
  return ctx.currentHandlerIndex
 }

 ctx.currentHandlerIndex = n
 return n
}
```

### memcache中间件

***

```golang
import (
 "bytes"
 "net/http"
 "sync"

 "github.com/bradfitz/gomemcache/memcache"
 "github.com/kataras/iris/v12/context"
)

var memcacheClientMux sync.Mutex
var memcacheClient *memcache.Client

// TODO,要不要带上http头部,例如:数据类型html/json/js,Date,Cache-control等等
type middleResp struct {
 // 匿名包括,变相继承
 http.ResponseWriter
 isOK       bool
 key        string
 expiration int32
 // 如果匿名包括,变相继承会和ResponseWriter冲突,导致接口重复写
 b bytes.Buffer
}

var StoreErrHandler func(error)

func (mr *middleResp) writeStore() {
 if mr.b.Len() > 0 {
  err := memcacheClient.Set(&memcache.Item{
   Key:        mr.key,
   Flags:      0,
   Expiration: mr.expiration,
   Value:      mr.b.Bytes(),
  })

  if StoreErrHandler != nil {
   StoreErrHandler(err)
  }
 }
}

func (mr *middleResp) Write(body []byte) (int, error) {
 if mr.isOK && memcacheClient != nil {
  _, err := mr.b.Write(body)
  if StoreErrHandler != nil {
   StoreErrHandler(err)
  }
 }
 return mr.ResponseWriter.Write(body)
}

func (mr *middleResp) WriteHeader(statusCode int) {
 mr.isOK = statusCode == http.StatusOK
 mr.ResponseWriter.WriteHeader(statusCode)
}

func MemcacheStore(server string, expireSecond int32) context.Handler {
 return MemcacheWrap(server, expireSecond, func(c context.Context) { c.Next() })
}

func MemcacheWrap(server string, expireSecond int32, handler context.Handler) context.Handler {
 memcacheClientMux.Lock()
 defer memcacheClientMux.Unlock()

 if memcacheClient == nil {
  memcacheClient = memcache.New(server)
 }

 return func(c context.Context) {
  mr := &middleResp{
   ResponseWriter: c.ResponseWriter().Naive(),
   key:            c.Request().RequestURI,
   expiration:     expireSecond,
  }

  c.ResponseWriter().BeginResponse(mr)

  handler(c)

  mr.writeStore()
 }
}
```

### main使用

***

```golang
import (
 "math/rand"

 "github.com/kataras/iris/v12"
 "github.com/kataras/iris/v12/middleware/recover"
)

func main() {

 app := iris.New()

 booksAPI := app.Party(
  "/iris/books",
  recover.New(),
  MemcacheStore("127.0.0.1:11211", 60),
 )
 {
  booksAPI.Get("/", list)
 }

 app.Get("/iris/other", MemcacheWrap("127.0.0.1:11211", 60, other))

 app.Listen(":9090")
}

func other(ctx iris.Context) {
 ctx.HTML(
  "<H1>%s, %v</H1>",
  ctx.Request().RequestURI,
  rand.Int(),
 )

}

// Book example.
type Book struct {
 Title string `json:"title"`
}

func list(ctx iris.Context) {
 books := []Book{
  {"Mastering Concurrency in Go"},
  {"Go Design Patterns"},
  {"Black Hat Go"},
 }

 // ctx.JSON(books)
 ctx.HTML("%v", books)
 // TIP: negotiate the response between server's prioritizes
 // and client's requirements, instead of ctx.JSON:
 // ctx.Negotiation().JSON().MsgPack().Protobuf()
 // ctx.Negotiate(books)
}
```
