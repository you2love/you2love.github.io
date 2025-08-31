# echo

### memcached中间件

***

```golang

import (
 "bytes"
 "net/http"
 "sync"

 "github.com/bradfitz/gomemcache/memcache"
 "github.com/labstack/echo/v4"
)

var memcacheClientMux sync.Mutex
var memcacheClient *memcache.Client

// TODO,要不要带上http头部,例如:数据类型html/json/js,Date,Cache-control等等
type middleResp struct {
 http.ResponseWriter
 isOK       bool
 key        string
 expiration int32
 bytes.Buffer
}

var StoreErrHandler func(error)

func (mr *middleResp) writeStore() {
 if mr.Buffer.Len() > 0 {
  err := memcacheClient.Set(&memcache.Item{
   Key:        mr.key,
   Flags:      0,
   Expiration: mr.expiration,
   Value:      mr.Bytes(),
  })

  if StoreErrHandler != nil {
   StoreErrHandler(err)
  }
 }
}

func (mr *middleResp) Write(body []byte) (int, error) {
 if mr.isOK && memcacheClient != nil {
  _, err := mr.Buffer.Write(body)
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

func MemcacheStore(server string, expireSecond int32) func(echo.HandlerFunc) echo.HandlerFunc {
 memcacheClientMux.Lock()
 defer memcacheClientMux.Unlock()

 if memcacheClient == nil {
  memcacheClient = memcache.New(server)
 }

 return func(next echo.HandlerFunc) echo.HandlerFunc {
  return func(c echo.Context) error {
   resp := c.Response()
   mr := &middleResp{
    ResponseWriter: resp.Writer,
    key:            c.Request().RequestURI,
    expiration:     expireSecond,
   }

   resp.Writer = mr

   err := next(c)

   mr.writeStore()

   return err
  }
 }
}

func MemcacheWrap(server string, expireSecond int32, handler echo.HandlerFunc) echo.HandlerFunc {
 return MemcacheStore(server, expireSecond)(handler)
}


```

### main使用

***

```golang
package main

import (
 "fmt"
 "math/rand"
 "net/http"

 "github.com/labstack/echo/v4"
 "github.com/labstack/echo/v4/middleware"
)

func main() {
 e := echo.New()

 // Middleware
 e.Use(middleware.Logger())
 e.Use(middleware.Recover())

 StoreErrHandler = func(err error) {
  e.Logger.Error(err)
 }

 // Routes
 e.GET("/echo/string", stringHandler, MemcacheStore("127.0.0.1:11211", 60))

 e.GET("/echo/html", MemcacheWrap("127.0.0.1:11211", 60, htmlHandler))

 // Start server
 e.Logger.Fatal(e.Start(":1323"))
}

// Handler
func stringHandler(c echo.Context) error {
 err := c.String(http.StatusOK, fmt.Sprintf("<H1>path:%s</H1>", c.Path()))
 if err != nil {
  return err
 }
 return c.String(http.StatusOK, fmt.Sprintf(
  "<H2>query:%s,rand:%d</H2>",
  c.QueryString(),
  rand.Int(),
 ))
}

// Handler
func htmlHandler(c echo.Context) error {
 err := c.HTML(http.StatusOK, fmt.Sprintf("<H1>uri:%s</H1>", c.Request().RequestURI))
 if err != nil {
  return err
 }
 return c.HTML(http.StatusOK, fmt.Sprintf(
  "<H2>query:%s,rand:%d</H2>",
  c.QueryString(),
  rand.Int(),
 ))
}

```

### nginx转发

***

```nginx
...
location /echo {
    set $memcached_key "$request_uri";
    memcached_pass 127.0.0.1:11211;
    #指示返回为html,方便浏览器直接显示
    default_type   text/html;
    error_page 404 502 504 = @echoServer;
}

location @echoServer {
    proxy_pass   http://127.0.0.1:1323;
}
...
```
