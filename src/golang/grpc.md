---
# grpc示例
---

# server

|工具 |介绍|
|--|--|
|protobuf protocol |buffer 编译所需的命令行|
|protoc-gen-go |从 proto 文件，生成 .go 文件|
|protoc-gen-go-grpc |从 proto 文件，生成 GRPC 相关的 .go 文件|
|protoc-gen-grpc-gateway |从 proto 文件，生成 grpc-gateway 相关的 .go 文件|
|protoc-gen-openapiv2 |从 proto 文件，生成 swagger 界面所需的参数|

***

```golang
package main

import (
 "context"
 "flag"
 "fmt"
 "log"
 "net"

 "google.golang.org/grpc"
 "google.golang.org/grpc/metadata"
 "google.golang.org/grpc/peer"

 com "xxx.site/myself/grpc-common"
)

var (
 GitHash     = "Unkown"
 CompileTime = "Unkown"
 port        = flag.Int("port", 8411, "默认端口")
)

// 定义服务端中间件
func middleware(ctx context.Context, req interface{},
 info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
 log.Printf("middleware ctx:%v", ctx)
 log.Printf("middleware req:%v", req)
 log.Printf("middleware info:%v", info)
 log.Printf("middleware handler:%v", handler)
 resp, err = handler(ctx, req)
 log.Printf("middleware resp:%v", resp)
 log.Printf("middleware err:%v", err)
 return
}

type MathServer struct {
 com.UnimplementedMathServer
}

// 各种信息都通过ctx中valueCtx传递进来
// 由不同包获取转换
func (ms *MathServer) Add(ctx context.Context, req *com.AddReq) (*com.AddRsp, error) {
 log.Printf("ctx:%v, req:%v", ctx, req)
 if client, ok := peer.FromContext(ctx); ok {
  log.Printf("client:%v", client)
 }

 if ic, ok := metadata.FromIncomingContext(ctx); ok {
  log.Printf("ic:%v", ic)
 }

 if oc, ok := metadata.FromOutgoingContext(ctx); ok {
  log.Printf("oc:%v", oc)
 }

 if oc, ok := metadata.FromOutgoingContext(ctx); ok {
  log.Printf("oc:%v", oc)
 }

 sts := grpc.ServerTransportStreamFromContext(ctx)
 log.Printf("sts:%v", sts)

 return &com.AddRsp{
  Result: req.Left + req.Right,
 }, nil
}

func main() {
 flag.Parse()

 // ct, err := credentials.NewServerTLSFromFile(
 //  "grpc.xxx.site.pem",
 //  "grpc.xxx.site.key",
 // )
 // if err != nil {
 //  log.Fatalf("tls file;%v", err)
 // }

 // tcp表示优先使用ipv6,其次ipv4,两者都能用
 l, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
 if err != nil {
  log.Fatalf("fail listen tcp %d", *port)
 }

 // 安装中间件
 s := grpc.NewServer(
  // 默认没有采用安全传输ssl,tls
  // 增加证书认证
  //grpc.Creds(ct),
  grpc.UnaryInterceptor(middleware),
 )

 com.RegisterMathServer(s, &MathServer{})
 log.Printf(
  "githash:%v, compile:%v,listen:%v",
  GitHash,
  CompileTime,
  l.Addr())

 err = s.Serve(l)
 if err != nil {
  log.Fatalf("fail server:%v", err)
 }
}
```

## client

***

```golang
package main

import (
 "context"
 "flag"
 "log"
 "time"

 "google.golang.org/grpc"
 "google.golang.org/grpc/credentials/insecure"

 com "xxx.site/myself/grpc-common"
)

var (
 GitHash     = "unknown"
 CompileTime = "unknown"
 // addr = flag.String("addr", "dns:///grpc.xxx.site", "默认服务端端口")
 addr = flag.String("addr", "127.0.0.1:8411", "默认服务端端口")
)

// 定义客户端中间件
func middleware(ctx context.Context, method string,
 req, reply interface{}, c *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {

 log.Printf("middleware ctx:%v", ctx)
 log.Printf("middleware method:%v", method)
 log.Printf("middleware req:%v", req)
 log.Printf("middleware reply:%v", reply)
 log.Printf("middleware conn:%v", c)
 log.Printf("middleware invoker:%v", invoker)
 for pos, opt := range opts {
  log.Printf("middleware pos:%v, opt:%v", pos, opt)
 }

 err := invoker(ctx, method, req, reply, c, opts...)

 log.Printf("middleware err:%v", err)

 return err

}

func main() {
 flag.Parse()

 // ct, err := credentials.NewClientTLSFromFile("grpc.xxx.site.pem", "grpc.xxx.site")
 // if err != nil {
 //  log.Fatalf("err:%v", err)
 // }

 conn, err := grpc.Dial(
  *addr,
  // 采用禁用安全传输,即没有ssl/tls
  grpc.WithTransportCredentials(insecure.NewCredentials()),
  // 采用证书,注意跨平台，linux amd64/apple m1芯片之间可能不能通讯
  // grpc.WithTransportCredentials(ct),
  // 安装中间件
  grpc.WithUnaryInterceptor(middleware),
  grpc.WithTimeout(time.Minute),
 )
 if err != nil {
  log.Fatalf("dial:%v, %v", *addr, err)
 }
 defer conn.Close()

 client := com.NewMathClient(conn)

 req := com.AddReq{
  Left:  10,
  Right: 20,
 }

 resp, err := client.Add(context.Background(), &req)
 if err != nil {
  log.Fatalf("add fail:%v", err)
 }

 log.Printf("resp:%v", resp.Result)
}

```

## proto

***

* proto内容

```protobuf
syntax = "proto3";

option go_package = "./;common";

service Math {
    rpc Add(AddReq)returns(AddRsp){}
}

message AddReq {
    int64 left = 1;
    int64 right = 2;
}

message AddRsp {
    int64 result = 1;
}
```

* 生成脚本

```sh
#!/bin/bash

#--go-grpc_out表示启动protoc-gen-go-grpc插件
# --openapiv2_out 表示产生swagger.json 
protoc --go_out=. --go-grpc_out=. *.proto
```

## nginx

***

```nginx
...
server_names_hash_bucket_size 64;
server {
        listen 443 ssl http2;
        server_name grpc.xxx.site;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
        ssl_certificate grpc.xxx.site.pem;
        ssl_certificate_key grpc.xxx.site.key;

        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout 5m;

        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        location / {
            # grpc_pass localhost:9000; 等价于 grpc://127.0.0.1:8411 等价于 [::]:8411;
            # To use gRPC over SSL,就要带上grpcs:
            grpc_pass grpcs://[xxx]:8411;
            client_max_body_size 200M;
        }
    }
...
```

# 扩展工具(<https://buf.build/>)

> buf之于proto，类似go mod之于golang，它通过buf.yaml来声明一个proto的module，作为管理的最小单元，方便其它proto库引用，也可以用来声明对其它库的依赖，包括从远程仓库BSR（全称 Buf Schema Registry）拉取依赖的proto库。它同时提供了代码生成管理工具buf.gen.yaml方便我们指定protoc插件，以及对这些protoc插件的安装和管理，我们不用本地配置protoc工具和各种protoc插件，大大提升了开发效率。

* API 设计通常不一致
* 依赖管理通常是事后才想到的
* 不强制执行向前和向后兼容性
* proto文件分发是一个困难的、未解决的过程
* 工具生态系统是有限的
* 有很多附加工具及插件
