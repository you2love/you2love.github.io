---
# rtmp
---

### [下载安装rtmp模块](https://github.com/arut/nginx-rtmp-module)

### 编译

```sh
/configure --prefix=/Users/Shared/nginx \
             --add-module=../nginx-party-module/nginx-rtmp-module \
             --with-http_ssl_module \
             --with-openssl=/opt/homebrew/Cellar/openssl@1.1/1.1.1m\
             --with-debug
make
make install
```

### 修改配置

```nginx
rtmp {
    server {
        listen 1935;
        application vod {
            play /Users/xxx/iCloud-archive/video;
        }
    }
}
```

### 访问

```sh
#vlc打开串流地址
rtmp://host/vod/xxx.mp4
```

### 附录

* RTMP、RTSP、HTTP协议理论上都可以用来做视频直播或点播,直播一般用RTMP,RTSP,点播用 HTTP

* RTMP协议
  * 是流媒体协议。
  * RTMP协议是 Adobe 的私有协议，未完全公开。
  * RTMP协议一般传输的是 flv，f4v 格式流。
  * RTMP一般在 TCP 1个通道上传输命令和数据。

* RTSP协议
  * 是流媒体协议。
  * RTSP协议是共有协议，并有专门机构做维护
  * RTSP协议一般传输的是 ts、mp4 格式的流。
  * RTSP传输一般需要 2-3 个通道，命令和数据通道分离。

* HTTP协议
  * 不是是流媒体协议。
  * HTTP协议是共有协议，并有专门机构做维护
  * HTTP协议没有特定的传输流
  * HTTP传输一般需要 2-3 个通道，命令和数据通道分离
