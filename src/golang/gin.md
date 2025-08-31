# gin



### context中断原理

***

```golang
const abortIndex int8 = math.MaxInt8 / 2

// Abort prevents pending handlers from being called. Note that this will not stop the current handler.
// Let's say you have an authorization middleware that validates that the current request is authorized.
// If the authorization fails (ex: the password does not match), call Abort to ensure the remaining handlers
// for this request are not called.
func (c *Context) Abort() {
    // c.index赋值很大值,从导致下次Next都不执行,达到阻断执行链目的
 c.index = abortIndex
}

// Next should be used only inside middleware.
// It executes the pending handlers in the chain inside the calling handler.
// See example in GitHub.
func (c *Context) Next() {
 c.index++
 for c.index < int8(len(c.handlers)) {
  c.handlers[c.index](c)
  c.index++
 }
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
 "github.com/gin-gonic/gin"
)

var memcacheClientMux sync.Mutex
var memcacheClient *memcache.Client

// TODO,要不要带上http头部,例如:数据类型html/json/js,Date,Cache-control等等
type middleResp struct {
 // 匿名包括,变相继承
 gin.ResponseWriter
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

// Writes the string into the response body.
func (mr *middleResp) WriteString(s string) (int, error) {
 return mr.ResponseWriter.WriteString(s)
}

func MemcacheStore(server string, expireSecond int32) gin.HandlerFunc {
 return MemcacheWrap(server, expireSecond, func(c *gin.Context) { c.Next() })
}

func MemcacheWrap(server string, expireSecond int32, handler gin.HandlerFunc) gin.HandlerFunc {
 memcacheClientMux.Lock()
 defer memcacheClientMux.Unlock()

 if memcacheClient == nil {
  memcacheClient = memcache.New(server)
 }

 return func(c *gin.Context) {
  mr := &middleResp{
   ResponseWriter: c.Writer,
   key:            c.Request.RequestURI,
   expiration:     expireSecond,
  }

  c.Writer = mr

  handler(c)

  mr.writeStore()
 }
}
```

### main使用

***

```golang
import (
 "fmt"
 "math/rand"

 "github.com/gin-gonic/gin"
)

func main() {

 r := gin.Default()

 r.Use(gin.Logger())

 r.GET("/gin/wrap", MemcacheWrap("127.0.0.1:11211", 100, wrap))

 group := r.Group("/gin/group")

 group.Use(MemcacheStore("127.0.0.1:11211", 100))

 group.GET("/ping", func(c *gin.Context) {
  c.JSON(200, gin.H{
   "message": "pong",
  })
 })

 group.GET("/gin", func(c *gin.Context) {
  c.Data(200, "text/html",
   []byte(fmt.Sprintf("<H1>gin,%v</H1>", rand.Int())),
  )
 })

 r.Run("0.0.0.0:5050")
}

func wrap(c *gin.Context) {
 c.Data(200, "text/html",
  []byte(fmt.Sprintf("<H1>warp,%v</H1>", rand.Int())),
 )
}
```
