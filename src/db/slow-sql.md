# MySQL慢SQL优化

```mermaid
graph LR
定位问题 --> 分析原因 --> 优化 --> 验证 --> 预防
```

## 定位问题

### 开启慢查询日志

> 慢查询日志是MySQL记录执行时间超过阈值的SQL的专用日志，是定位慢SQL的基础

#### 临时开启（重启失效）

```sql
-- 开启慢查询日志 
SET GLOBAL slow_query_log = 1; 
-- 设置慢查询阈值（单位：秒，建议设1秒，捕捉临界慢SQL） 
SET GLOBAL long_query_time = 1; 
-- 指定日志文件路径（可选） 
SET GLOBAL slow_query_log_file = '/var/lib/mysql/slow.log'; 
-- 记录未使用索引的SQL（即使执行快，也建议开启，提前发现索引问题） 
SET GLOBAL log_queries_not_using_indexes = 1;
```

#### 永久开启（修改配置文件my.cnf/my.ini）

```TOML
[mysqld]
slow_query_log = 1
long_query_time = 1
slow_query_log_file = /var/lib/mysql/slow.log
log_queries_not_using_indexes = 1 
```

修改后重启MySQL生效：

```shell
systemctl restart mysqld
```

### 分析慢查询日志

直接看日志文件内容杂乱，推荐用MySQL自带的mysqldumpslow工具分析：

```shell
# 按执行时间排序，取前10条慢SQL 
mysqldumpslow -s t -t 10 /var/lib/mysql/slow.log 
# 按查询次数排序，取前10条高频慢SQL 
mysqldumpslow -s c -t 10 /var/lib/mysql/slow.log
```

• 补充：实时排查可使用show processlist;关注Time（执行时间）、State（状态，如Sending data/Creating tmp table表示执行慢）、Info（SQL内容）字段。

### 注意点

• 把long_query_time设得太大，漏掉“临界慢SQL”，这些SQL高并发下会放大性能问题；

• 只看日志不结合业务，比如把“凌晨批量统计SQL”当成常规慢SQL优化，忽略业务场景。


## 分析原因

> 用explain分析执行计划，定位到底是“没走索引”“扫描行数多”还是“排序/临时表导致慢”

### 示例语句

```SQL
EXPLAIN SELECT * FROM `order` WHERE user_id = xx AND create_time >= 'xxxx-yy-dd';
```

### 核心字段

| 字段    | 核心含义                                               | 优化目标                             |
| ----- | -------------------------------------------------- | -------------------------------- |
| type  | 访问类型（从优到差：system>const>eq_ref>ref>range>index>ALL） | 至少达到range，避免ALL（全表扫描）            |
| key   | 实际使用的索引（NULL表示未走索引）                                | 非NULL，且是最优索引                     |
| rows  | 预估扫描行数（越接近实际结果越准）                                  | 越小越好                             |
| Extra | 额外信息（核心标识）                                         | 避免Using filesort/Using temporary |

### 常见案例

• 案例1：type=ALL + key=NULL → 全表扫描，未走索引，核心优化方向是加索引；

• 案例2：Extra=Using filesort → SQL需要排序但未走索引排序，需优化排序字段的索引；

• 案例3：Extra=Using temporary → SQL用到临时表（如group by/join），需优化关联/分组逻辑。

### 易犯错误

• 只关注type字段，忽略Extra（比如type=ref但Extra=Using filesort，依然是慢SQL）；

• 认为rows是“实际扫描行数”，其实是预估值，需结合业务数据量判断。


## 优化

```mermaid
graph LR
sql写法 --> 索引 --> 表结构 --> 服务器配置
```

### SQL写法

| 错误写法（慢）                                                                  | 正确写法（快）                                                                               | 优化原因               |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | ------------------ |
| SELECT * FROM user WHERE id IN (a,b,c)                                  | SELECT id, name, phone FROM user WHERE id IN (a,b,c)                                  | 避免查询无用字段，减少IO/内存消耗 |
| SELECT * FROM order WHERE DATE(create_time) = 'xxxx-yy-dd'              | SELECT * FROM order WHERE create_time >= 'xxxx-yy-dd' AND create_time < 'xxxx-yy-dd' | 索引字段做函数操作会导致索引失效   |
| SELECT * FROM order WHERE user_id IN (SELECT id FROM user WHERE age>x) | SELECT o.* FROM order o JOIN user u ON o.user_id=u.id WHERE u.age>x                 | 子查询会创建临时表，JOIN效率更高 |
| SELECT * FROM goods WHERE name LIKE '%xxx%'                              | SELECT * FROM goods WHERE name LIKE 'xx%'（业务允许）或用全文索引                                | %xxx会导致索引失效，xxx%不会 |

### 索引

> 索引是解决慢SQL的核心，但“不是建越多越好”，需精准建、合理删。

#### 几个方向

* 按“最左前缀原则”建联合索引：比如查询WHERE a=1 AND b=2 AND c=3，建(a,b,c)而非单独的a/b/c索引；

* 用覆盖索引减少回表：查询的字段都在索引里（Extra=Using index），比如SELECT id, name FROM user WHERE code='xxxxx'，建(code, name)索引；

* 删除无用索引：单表索引控制在5个以内，避免写操作（INSERT/UPDATE/DELETE）维护索引的开销；

* 避免索引失效场景：如隐式类型转换（字符串字段用数字查）、OR连接无索引字段等。

#### 表结构

> 适合表数据量大（百万/千万级）或字段设计不合理的场景：

* 反范式设计：比如订单表存user（而非每次关联用户表），减少JOIN次数；

* 水平分表：按时间/用户ID拆分大表（如order_xxx/order_yy）；

* 垂直分表：拆分大字段（如把商品表的desc拆到另外表）；

• 字段类型优化：用更小的类型（如tinyint存性别、datetime存时间，而非varchar）。

### 服务器


#### 调整MySQL配置参数：

* innodb_buffer_pool_size：建议设为物理内存的60%，让更多数据缓存在内存，减少磁盘IO；

* sort_buffer_size：调整排序缓存，避免排序时使用临时文件；

* max_connections：合理设置最大连接数，避免连接数不足导致SQL阻塞。

#### 架构优化

> 适合单库单表支撑不了的场景

* 读写分离：主库写、从库读，读写分流
* 缓存：用Redis,Memcached缓存热点数据（如商品详情、用户信息）
* 分库分表：用中间服务转发，综合数据
* 拆分业务:引入其他类型数据库,例如es做多条件分页查询

#### 注意点

* 过早做架构优化（比如小表也分库分表），增加系统复杂度；
* 盲目加索引，导致写操作性能暴跌
* 调大所有配置参数，导致服务器内存溢出。


## 验证

优化后必须验证，避免“越改越慢”：

* 重新执行EXPLAIN，检查type/key/Extra是否改善；

* 统计执行时间：

```SQL
SET profiling = 1; 
SELECT id, name FROM user WHERE code='xxx'; 
SHOW PROFILES;
```

* 对比优化前后的“执行时间”“扫描行数”“CPU/IO占用”

 
## 预防


* 制定SQL规范：禁止SELECT *、禁止大表全表扫描、禁止在索引字段做函数操作；

* 定期审计：每周用mysqldumpslow分析慢查询日志，提前发现问题；

* 压测：压测工具模拟高并发，验证SQL性能；

* 监控告警：对接监控平台，慢SQL触发时及时告警。
