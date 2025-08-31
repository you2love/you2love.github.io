# web


### HTTP协议

***

```mermaid
    flowchart LR
      v1(HTTP1.1-1999年) --分帧复用--> v2(HTTP2-2015年)
      v2 --tcp转向udp-->v3(HTTP3-2021年)
```

* HTTP不变的协议过程
![http_proto](webp/web/http_proto.webp)

* HTTP底层传输变化
![HTTP协议](webp/web/http.webp)

* HTTP1.1改进
  * 默认持久连接
  * 增加Cookie,虚拟主机,动态内容支持
  * 使用CDN的实现域名分片机制

* HTTP1.1问题
  * TCP的慢启动
  * 多条TCP连接竞争带宽
  * 队头阻塞

* HTTP2改进
  * 二进制分帧层
  * 请求的优先级
  * 服务器推送
  * 头部压缩
![http2_tcp](webp/web/http2_tcp.webp)
![http2_frame_tcp](webp/web/http2_frame.webp)
![https_tcp_tls](webp/web/https_tcp_tls.webp)

* HTTP2问题
  * 有序字节流引出的队头阻塞（Head-of-line blocking），使得HTTP2的多路复用能力大打折扣
  * TCP与TLS叠加了握手时延，建链时长还有1倍的下降空间
  * 基于TCP四元组确定一个连接，这种诞生于有线网络的设计，并不适合移动状态下的无线网络，这意味着IP地址的频繁变动会导致TCP连接、TLS会话反复握手，成本高昂。

* HTTP3改进
  * HTTP3基于UDP协议重新定义了连接，在QUIC层实现了无序、并发字节流的传输，解决了队头阻塞问题
  * HTTP3重新定义了TLS协议加密QUIC头部的方式，既提高了网络攻击成本，又降低了建立连接的速度
  * HTTP3 将Packet、QUIC Frame、HTTP3 Frame分离，实现了连接迁移功能，降低了5G环境下高速移动设备的连接维护成本

### jwt(JSON Web Token)

***

* 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。
* 服务器采用秘钥签名检验token内部数据是否正确，不再保存session

* 传统session方案,占用内存,不易扩展

```mermaid

sequenceDiagram
    actor u as 用户
    actor s as 服务器
    u->>s: login登陆
    s-->>u: form填写用户名密码
    u->>s: Post用户名密码
    s->>s: 数据库检查,生成并保存session
    s-->>u: setcookie sessionID
    u->>s: cookies带上sessionID
    s->>s: 根据sessionID,获取session
    s-->>u: 提供服务
```

* jwt方案,服务器私用secret,除过期时间之外,token不易作废

```mermaid

sequenceDiagram
    actor u as 用户
    actor s as 服务器
    u->>s: login登陆
    s-->>u: form填写用户名密码
    u->>s: Post用户名密码
    s->>s: 数据库检查,利用secret生成token
    s-->>u: Authorization token
    u->>s: Authorization token
    s->>s: 根据secret,检验token
    s-->>u: 提供服务
```

* jwt-token构成

```mermaid

flowchart LR
  subgraph Header
        h(json对象base64编码)
    end
    subgraph Payload
        p(json对象base64编码)
    end
    subgraph Signature
        s(加密计算后base64编码)
    end

  Header--用点号.连接-->Payload--用点号.连接-->Signature
```

* Header示例

 ```json
 {
  "alg": "HS256",
  "typ": "JWT"
}
 ```

* Payload示例

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

* Signature

```js
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

* 实例展示

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ

### 系统容错 限流-熔断-降级

***

* 限流,当核心服务的处理能力不能应对外部请求的突增流量时，必须采取限流的措施。
* 熔断,非核心服务

```mermaid

  sequenceDiagram
      actor u as 用户
      actor l as 断路器
      actor s as 服务
      u->>l: 请求
      l->>s: 转发请求
      s-->>l: 成功回包
      l-->>u: 转发成功回包
      u->>l: 请求
      l->>s: 转发请求
      s-->>l: 失败
      l->>l: 累计失败,达到阀值
      l-->>u: 转发失败
      u->>l: 请求
      l->>l: 检查服务恢复?
      l-->>u: 回包失败

```

  * 服务熔断是指调用方访问服务时通过断路器做代理进行访问，断路器会持续观察服务返回的成功、失败的状态，当失败超过设置的阈值时断路器打开，请求就不能真正地访问到服务了。
  * CLOSED：默认状态。断路器观察到请求失败比例没有达到阈值，断路器认为被代理服务状态良好。
  * OPEN：断路器观察到请求失败比例已经达到阈值，断路器认为被代理服务故障，打开开关，请求不再到达被代理的服务，而是快速失败。
  * HALF OPEN：断路器打开后，为了能自动恢复对被代理服务的访问，会切换到半开放状态，去尝试请求被代理服务以查看服务是否已经故障恢复。如果成功，会转成CLOSED状态，否则转到OPEN状态

* 降级-采用预设方案行动,针对非核心，非必要服务

### webdav

***

* WebDAV （Web-based Distributed Authoring and Versioning） 一种基于 HTTP 1.1协议的通信协议。
* 它扩展了HTTP 1.1，在GET、POST、HEAD等几个HTTP标准方法以外添加了一些新的方法，
* 使应用程序可对Web Server直接读写，并支持写文件锁定(Locking)及解锁(Unlock)，还可以支持文件的版本控制。

### jsonnet

***

```sh
brew install jsonnet
```

![jsonnet](webp/web/jsonnet.webp)

### 优化方向

***

* 浏览器处理缓存,如下图所示
![缓存](webp/web/缓存.webp  "缓存")

* webpack打包

* 图片换格式WebP

* 浏览器处理HTML

![HTML渲染](webp/web/HTML渲染.webp  "HTML渲染")
![内部架构](webp/web/内部架构.webp  "内部架构")

### 优秀网站

***

* [nodejs-前端必备](https://nodejs.org/)

* [Bun-更快更现化的nodejs](https://v3.cn.vuejs.org/)

* [vue3-最火的前端框架](https://v3.cn.vuejs.org/)

* [echarts-必备图库](https://echarts.apache.org/zh/index.html)

* [apisix-api管理](https://apisix.apache.org/)

* [apache-大量优秀项目](https://apache.org)

* [nginx-官网](https://www.nginx.org/)

* [nginx-开源社区](https://www.nginx.org.cn/)

* [openresty](http://openresty.org/)

* [kong-网关](https://konghq.com/)

* [BizCharts-图形库](https://github.com/alibaba/BizCharts)

* [g2-图形库](https://antv.alipay.com/zh-cn/g2/3.x/tutorial)

* [angular](https://angular.io/)

* [dart](https://www.dartlang.org/), [pub-库集散地](https://pub.flutter-io.cn/packages),绝对值得多看看

* [javascript-英文学习站](https://www.javascript.com/)

* [javascript-w3c](http://www.w3school.com.cn/js/)

* [前端cdn](https://www.bootcdn.cn/)

* [mermaidjs-代码画图库](https://mermaidjs.github.io/)

* [plantuml-代码画图库](http://plantuml.com/)

* [团队文档-阿里出品语雀](https://www.yuque.com/)

* [Confluence-团队文档](https://www.atlassian.com/),据说现在不能私有部署

### 国内cdn介绍

* BootCDN: www.bootcdn.cn
* 七牛云: www.staticfile.org
* 360: cdn.baomitu.com
* 字节跳动: cdn.bytedance.com
* 饿了么：github.elemecdn.com npm.elemecdn.com
* 知乎：unpkg.zhimg.com
