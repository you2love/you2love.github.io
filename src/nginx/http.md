---
# HTTP模块
---

## 核心模块阶段

***

```mermaid

flowchart TD
    subgraph POST_READ
        realip(realip)
    end
    subgraph SERVER_REWRITE
        rewrite(rewrite)
    end
    subgraph FIND_CONFIG
        NULL(NULL)
    end
    subgraph REWRITE
        rewrite2(rewrite)
    end
    subgraph POST_REWRITE
        NULL2(NULL)
    end
    subgraph PREACCESS
        direction LR
        degradation(degradation) --> limit_conn(limit_conn)
        limit_conn --> limit_req(limit_req)
        limit_req --> realip2(realip)
    end
    subgraph ACCESS
        direction LR
        access(access) --> auth(auth)
    end
    subgraph POST_ACCESS
        NULL3(NULL)
    end
    subgraph PRECONTENT
        direction LR
        mirror(mirror) --> try_files(try_files)
    end
    subgraph CONTENT
        direction LR
        static(static) --> gzip_static(gzip_static)
        gzip_static --> dav(dav)
        dav --> autoindex(autoindex)
        autoindex --> index(ndex)
        index --> random_index(random_index)
    end
    subgraph LOG
        log(log)
    end
POST_READ --> SERVER_REWRITE
SERVER_REWRITE --> FIND_CONFIG
FIND_CONFIG --> REWRITE
REWRITE --> POST_REWRITE
POST_REWRITE --> PREACCESS
PREACCESS --> ACCESS
ACCESS --> POST_ACCESS
POST_ACCESS --> PRECONTENT
PRECONTENT --> CONTENT
CONTENT --> LOG

```

> * POST_REWRITE阶段如果有rewrite，则会跳回到FIND_CONFIG阶段
>
> * 源代码中定义,如下图所示:
![http_phase图](/webp/http/http_phase.webp)

## FastCGI模块

***

```mermaid

sequenceDiagram
    actor n as nginx进程
    actor c as CGI进程
    n->>c: begin_request处理开始
    n->>c: params请求参数
    n->>+c: stdin请求数据内容
    c->>c:请求处理
    c-->>-n: stdout处理结果
    c-->>n: end_request处理结束

```

## static模块

***

> 把请求url中path映射本地路径,读取本地文件返回客户端
>
> 核心源代码,如下图所示:
![static_module图](/webp/http/nginx_static_module.webp)

## index模块

***

> 引入配置参数index,如下图所示:
![index_command图](/webp/http/nginx_index_command.webp  "index_command图")

> 请求url为目录时,把配置参数index值附加在url上,然后内部转跳

```c


static ngx_int_t
ngx_http_index_handler(ngx_http_request_t *r)
{
    ...
    if (index[i].name.data[0] == '/') {
                return ngx_http_internal_redirect(r, &index[i].name, &r->args);
            }
    ...

    ngx_log_debug1(NGX_LOG_DEBUG_HTTP, r->connection->log, 0,
                       "open index \"%V\"", &path);

    ...
    return ngx_http_internal_redirect(r, &uri, &r->args);
}

```

> 转跳调试日志,如下图所示:
![index_redirect图](/webp/http/nginx_index_redirect.webp  "index_redirect图")
