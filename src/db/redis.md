# redis
<!-- toc --> 

### 安装运行

***

```sh
brew install redis
brew services start redis
```

***

```sh
wget https://download.redis.io/redis-stable.tar.gz
tar -xzvf redis-stable.tar.gz
cd redis-stable
make

# If the compile succeeds, you'll find several Redis binaries in the src directory, including:
# redis-server: the Redis Server itself
# redis-cli is the command line interface utility to talk with Redis.
# To install these binaries in /usr/local/bin, run:
make install
```

### 自带客户端

***

```sh
#Usage: redis-cli [OPTIONS] [cmd [arg [arg ...]]]
#Examples:
#  cat /etc/passwd | redis-cli -x set mypasswd
#  redis-cli get mypasswd
#  redis-cli -r 100 lpush mylist x
#  redis-cli -r 100 -i 1 info | grep used_memory_human:
#  redis-cli --quoted-input set '"null-\x00-separated"' value
#  redis-cli --eval myscript.lua key1 key2 , arg1 arg2 arg3
#  redis-cli --scan --pattern '*:12345*'
#When no command is given, redis-cli starts in interactive mode
#redis-cli的命令提示非常有帮助,比其他终端好用的多
redis-cli
```

### RedisInsight是Redis官方出品的可视化管理工具，可用于设计、开发、优化你的Redis应用

### redis4引入自动内存碎片整理

***

```sh
# 开启自动内存碎片整理(总开关),默认no
activedefrag yes
# 当碎片达到 100mb 时，开启内存碎片整理
active-defrag-ignore-bytes 100mb
# 当碎片超过 10% 时，开启内存碎片整理
active-defrag-threshold-lower 10
# 内存碎片超过 100%，则尽最大努力整理
active-defrag-threshold-upper 100
# 内存自动整理占用资源最小百分比
active-defrag-cycle-min 1
# 内存自动整理占用资源最大百分比
active-defrag-cycle-max 25
```

> **Notice:开启后,可能特定时间影响redis响应速度**

### redis5带来了Stream

***

>Redis对消息队列（MQ，Message Queue）的完善实现
![redis_stream](../webp/redis/redis_stream.webp)

### redis6增加了多线程

***

```sh
# io-threads 4
# Setting io-threads to 1 will just use the main thread as usual.
# io-threads-do-reads no
# Note that Gopher is not currently supported when 'io-threads-do-reads'
```

>Redis实例占用相当大的CPU耗时的时候才建议采用,否则使用多线程没有意义。基本上我们都是**观众**!!!

### 常用功能

***

| 功能 | 命令 | 备注 |
| -- | -- | -- |
| String | set,get,setnx,mget,mset,msetnx | 最大512MB,可存任何数据 |
| List | lpush,lpop,rpush,rpop,blpop,brpop,llen,lpushx,lrem,lrange | 超过40亿个元素 |
| Hash | hget,hset,hdel,hgetall,hkeys,hvals,hlen,hmset,hmget | 超过40亿个元素 |
| Set | sadd,spop,srem,scard,smembers,sismember,sdiff,sinter,sunion | 超过40亿个成员 |
| SortedSet | zadd,zrem,zcard,zcount,zscore,zrange | 超过40亿个成员 |
| Pub/Sub | subscribe,publish,unsubscribe | 消息不会保存,广播型 |
| Stream | xadd,xdel,xlen,xread,xgroup,xreadgroup,xinfo,xtrim | 消息会保存,每个消息都是一组键值对,同组竞争,组间广播 |
| Key | del,keys,type,object,ttl,persist,randomkey,rename | 针对键操作 |
| Pipelining |  优点:减少RTT(往返时间),多次网络IO,系统调用的消耗 | 缺点:独占链接,占用redis内存缓存命令结果 |
| Auth | auth password | 验证密码 |
| HyperLogLog | pfadd,pfcount | 基数估计 |

![string](../webp/redis/redis_string.webp)
![list](../webp/redis/redis_list.webp)
![hash](../webp/redis/redis_hash.webp)
![set](../webp/redis/redis_set.webp)
![sortedSet](../webp/redis/redis_sortedSet.webp)
![pub/sub](../webp/redis/redis_pubsub.webp)
![key](../webp/redis/redis_key.webp)
![hl](../webp/redis/redis_hl.webp)

* xreadgroup和xack配合使用

```c
WHILE true
    entries = XREADGROUP $GroupName $ConsumerName BLOCK 2000 COUNT 10 STREAMS mystream >
    if entries == nil
        puts "Timeout... try again"
        CONTINUE
    end

    FOREACH entries AS stream_entries
        FOREACH stream_entries as message
            process_message(message.id,message.fields)

            # ACK the message as processed
            XACK mystream $GroupName message.id
        END
    END
END
```

### 常见问题

***

1. **缓存雪崩:短时间内大量键超时失效**

2. **缓存击穿:缓存中没有键值**

    1. 确实不存在:用布隆过滤器优化
    2. 键超时:设置永不超时,受最大内存限制

### 批量删除

***

```lua
--批量删除msg开始的键值
EVAL "return redis.call('del', unpack(redis.call('keys', ARGV[1])))" 0 'msg*'
```

### redis通讯协议-RESP

***

* 请求协议
  1. *后面数量表示存在几个$
  2. $后面数量表示字符串的长度
  3. 每项用\r\n分隔

```sh
*3\r\n$3\r\nSET\r\n$5\r\nmykey\r\n$7\r\nmyvalue\r\n
```

>**pipeline实现就是连接发送命令,不用每个都等**

### 常见Redis模块


| **模块名称**        | **核心特性**                                            | **适用场景**                           | **关键命令示例**                             |
| --------------- | --------------------------------------------------- | ---------------------------------- | -------------------------------------- |
| RedisJSON       | 原生支持 JSON 数据类型，支持 JSONPath 语法，可直接修改 JSON 内部字段       | 存储结构化 JSON 数据（用户信息、配置文件）、需要嵌套数据的场景 | `JSON.SET`、`JSON.GET`、`JSON.ARRAPPEND` |
| RediSearch      | 提供全文搜索和次级索引，支持模糊匹配、分词、排序、聚合，可与 RedisJSON 结合         | 实时搜索（商品搜索、日志检索）、多维度数据过滤和排序         | `FT.CREATE`（建索引）、`FT.SEARCH`           |
| RedisGraph      | 基于属性图模型，支持 Cypher 查询语言，高效处理节点与边的关系                  | 社交网络关系（好友推荐）、知识图谱、路径分析（如供应链溯源）     | `GRAPH.QUERY`、`GRAPH.DELETE`           |
| RedisTimeSeries | 优化时序数据存储，自动压缩、降采样，支持时间范围查询和聚合（均值、最大值）               | 物联网传感器数据、系统监控指标（CPU / 内存）、金融高频交易记录 | `TS.CREATE`、`TS.ADD`、`TS.RANGE`        |
| RedisBloom      | 包含布隆过滤器、计数布隆过滤器、布谷鸟过滤器，高效判断元素存在性（低内存）               | 缓存穿透防护、大数据去重（爬虫 URL）、黑名单 / 白名单判断   | `BF.ADD`、`BF.EXISTS`、`CF.ADD`          |
| RedisGears      | 服务器端 Python 脚本执行，支持 Map/Reduce、事件触发（如键过期时处理）        | 实时数据清洗、分布式任务调度、复杂业务规则计算（如促销价格实时计算） | `RG.PYEXECUTE`（执行脚本）                   |
| RedisAI         | 加载 TensorFlow/PyTorch 模型，在 Redis 内部执行实时推理，减少数据传输开销  | 实时推荐系统、图像识别、NLP 情感分析（如评论实时分类）      | `AI.MODELSET`、`AI.TENSORSET`、`AI.RUN`  |
| RedisCell       | 基于令牌桶算法的分布式限流，支持突发流量处理，确保多节点规则一致性                   | API 接口限流、防止恶意请求（如爬虫）、游戏防作弊（限制操作频率） | `CL.THROTTLE`（设置限流规则）                  |
| RedisSQL        | 支持 SQL 语法（SELECT/INSERT/UPDATE），映射 Redis 哈希表为 SQL 表 | 从关系型数据库迁移过渡、需要混合使用 SQL 与 Redis 的场景 | `SQL SELECT * FROM users`              |
| HyperLogLog     | 估算集合基数（不重复元素数），占用内存极小（约 12KB / 千万级数据）               | 统计独立访客（UV）、页面浏览去重、活动参与人数估算         | `PFADD`、`PFCOUNT`、`PFMERGE`            |
| Streams         | 持久化消息队列，支持发布 - 订阅、消息分组消费，替代 Kafka/RabbitMQ 轻量场景     | 微服务间事件传递（如订单创建）、实时日志收集、游戏服务器消息同步   | `XADD`（发消息）、`XREAD`（读消息）               |

