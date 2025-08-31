# code
<!-- toc --> 

### 更丰富的errors

***

```golang
import (
 "fmt"

 "github.com/pkg/errors"
)

func main() {
  //%+v格式输出,则带上栈调用,调试好帮手
 fmt.Printf("err:%+v", errors.New("mynew"))
}
```

### memcached

***

```golang
package main

import (
 "fmt"
 //连接memcached
 "github.com/bradfitz/gomemcache/memcache"
)

func main() {
 key := "/golang"
 client := memcache.New("127.0.0.1:11211")
 err := client.Set(&memcache.Item{
  Key:        key,
  Flags:      0,
  Expiration: 0,
  Value:      []byte("<HTML><H2>hello,golang</H2></HTML>"),
 })
 if err != nil {
  fmt.Println(err.Error())
  return
 }

 item, err2 := client.Get(key)
 if err2 != nil {
    fmt.Println(err2.Error())
  return
 }

 fmt.Println(string(item.Value))
}

```

### redis

***

```golang
package main

import (
 "fmt"

 //连接redis
 "github.com/gomodule/redigo/redis"
)

func main() {
 conn, err := redis.Dial("tcp", ":6379")
 if err != nil {
  fmt.Println(err.Error())
  return
 }
 defer conn.Close()

 setReply, setReplyErr := redis.String(conn.Do("set", "firstKey", "firstValue"))
 if setReplyErr != nil {
  fmt.Println(setReplyErr.Error())
  return
 }

 fmt.Println("setReply:", setReply, reflect.TypeOf(setReply))

 mgetReplay, mgetReplyErr := redis.Strings(conn.Do("mget", "firstKey", "k1"))
 if mgetReplyErr != nil {
  fmt.Println(mgetReplyErr.Error())
  return
 }

 fmt.Println("mgetReplay:", mgetReplay, reflect.TypeOf(mgetReplay))

 hgetallReply, hgetallReplyErr := redis.StringMap(conn.Do("hgetall", "myhash"))
 if hgetallReplyErr != nil {
  fmt.Println(hgetallReplyErr.Error())
  return
 }

 fmt.Println("hgetallReply:", hgetallReply, reflect.ValueOf(hgetallReply))

 lrangeReply, lrangeReplyErr := redis.Strings(conn.Do("lrange", "mylist", "0", "-1"))
 if lrangeReplyErr != nil {
  fmt.Println(lrangeReplyErr.Error())
  return
 }

 fmt.Println("lrangeReply:", lrangeReply, reflect.ValueOf(lrangeReply))

 smembersReply, smembersReplyErr := redis.Strings(conn.Do("smembers", "myset"))
 if smembersReplyErr != nil {
  fmt.Println(smembersReplyErr.Error())
  return
 }

 fmt.Println("smembersReply:", smembersReply, reflect.TypeOf(smembersReply))

 zrangeReply, zrangeReplyErr := redis.Int64Map(conn.Do("zrange", "mySortedSet", "0", "-1", "withscores"))
 if zrangeReplyErr != nil {
  fmt.Println(zrangeReplyErr.Error())
  return
 }

 fmt.Println("zrangeReply:", zrangeReply, reflect.TypeOf(zrangeReply))
}
```

![golang_redis](golang_redis.webp)

### mongodb

***

```golang
package main

import (
 "context"
 "fmt"
 "reflect"
 "time"

//连接mongodb
 "go.mongodb.org/mongo-driver/bson"
 "go.mongodb.org/mongo-driver/mongo"
 "go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
 ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
 defer cancel()

 client, err := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://localhost:27017"))
 if err != nil {
  fmt.Println("connect:", err.Error())
  return
 }
 defer client.Disconnect(ctx)

// database,collection不存在,会自动创建,不必事先创建
 col := client.Database("firstDB").Collection("firstCol")

 reply, err := col.InsertOne(ctx, bson.D{{"name", "pai"}, {"value", 3.14159}})
 if err != nil {
  fmt.Println("list:", err.Error())
  return
 }

 fmt.Println(reflect.ValueOf(reply))
}
```

```golang
package main

import (
 "context"
 "database/sql"
 "fmt"
 "log"

 _ "github.com/go-sql-driver/mysql"
)

func main() {
 // user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local
 db, err := sql.Open("mysql", "root:@(127.0.0.1:3306)/mytest?charset=utf8mb4&parseTime=True&loc=Local")
 if err != nil {
  fmt.Println(err.Error())
  return
 }
 defer db.Close()

 ctx, stop := context.WithCancel(context.Background())
 defer stop()

 rows, err := db.QueryContext(ctx, "SELECT v FROM js")
 if err != nil {
  log.Fatal(err)
 }
 defer rows.Close()

 names := make([]string, 0)
 for rows.Next() {
  var name string
  if err := rows.Scan(&name); err != nil {
   log.Fatal(err)
  }
  names = append(names, name)
 }
 // Check for errors from iterating over rows.
 if err := rows.Err(); err != nil {
  log.Fatal(err)
 }
 fmt.Println(names)
}
```

```golang
//获取当前git的hash值
gitOut, gitErr := exec.Command("bash", "-c", "git rev-parse --short HEAD").Output()
if gitErr != nil {
 fmt.Println(gitErr)
 return
}
```

### trace

***

```golang
package main

import (
 "os"
 "runtime/trace"
)

func main() {
 trace.Start(os.Stderr)
 defer trace.Stop()

 ch := make(chan string)

 go func() {
  ch <- "hello,world"
 }()

 <-ch
}
```

```sh
#注意2>trace.out重定向,产生数据文件
go run main.go 2>trace.out
#pprof,trace有些需要graphviz
brew install graphviz
#采用trace工具分析显示数据,
go tool trace trace.out
```

![golang_trace](golang_trace.webp)

### strings.TrimLeft去掉连续的字符,strings.TrimPerfix只去掉一次

### profile

```golang
import (
  "github.com/pkg/profile"
  _ "net/http/pprof"
)

// go http.ListenAndServe("0.0.0.0:8080", nil)

func main() {
    // p.Stop() must be called before the program exits to
    // ensure profiling information is written to disk.
    p := profile.Start(profile.MemProfile, profile.ProfilePath("."), profile.NoShutdownHook)
    ...
    // You can enable different kinds of memory profiling, either Heap or Allocs where Heap
    // profiling is the default with profile.MemProfile.
    p := profile.Start(profile.MemProfileAllocs, profile.ProfilePath("."), profile.NoShutdownHook)

    // 采用web接口提供 http://localhost:8080/debug/profile
    go http.ListenAndServe("0.0.0.0:8080", nil)
}
```

```bash
# 等上步生成的的cpu.profile
go tool pprof cpu.profile

# 常见命令 top,前几个费时 web 输出临时svg图片展示
```
