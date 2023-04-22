---
# mysql
---

### SQL

* mysql没有完全实现[sql标准](https://datacadamia.com/data/type/relation/sql/ansi)
* 不区分大小写,一般内置关键词,函数等采用大写,用户表,列,参数采用小写
* 用分号作为结束语句标识,允许一行多条语句,一条语句多行.
* 有不同模式,建议采用strict mode
* 默认autocommit,除非显式取消
* 注释
  * 单行: 以#开头,到行结束
  * 单行: 以-- 开头,到行结束
  * 多行: /*开头，*/结束,c风格

* 字符集(Character)与校对规则(Collation)
  * 字符集都对应着一个默认的校对规则,也可以对应多个规则
  * 变量character_set_server记录服务器默认值,mysql8.0默认是utf8mb4(可储各种表情符号,最长4字节)
  * 每个库/表/字段可单独指定,库不指定则用服务器,表不指定则用库,字段不指定则用表
  * character_set_client服务器认为客户端发送过来的sql语句的编码
  * character_set_conneciton执行sql内部编码,所以服务器把客户端发送的sql从character_set_client转为character_set_conneciton
  * character_set_results 返回结果集
  * 客户端用连接参数一次性指定这三个值character_set_client, character_set_results, character_set_connection

* 自带4个数据库
  * information_schema 保存所有数据库/表/列/索引/权限等信息
  * performance_schema 收集数据库服务器性能参数，资源消息，资源等待
  * sys 存储来自performance_schema,简化说明，易于DBA理解
  * mysql 存储库用户，权限，关键字等mysql自已需要必要信息
* 程序表

   | 名称 | 作用 |
   | -- | -- |
   | mysqld | 服务器 |
   | mysqld_safe | 用来启动mysqld的脚本 |
   | mysql.server | 系统启动脚本,调用mysqld_safe脚本 |
   | mysqld_multi | 允许同时多个mysqld进程 |
   | mysql | 客户端 |
   | mysqladmin | 客户端管理数据库 |
   | mysqldump | 客户端导出数据 |
   | mysqlimport | 客户端导入数据 |

* 联表

```sql
...
joined_table: {
table_reference {[INNER | CROSS] JOIN | STRAIGHT_JOIN} table_factor [join_specification]
 | table_reference {LEFT|RIGHT} [OUTER] JOIN table_reference join_specification
 | table_reference NATURAL [INNER | {LEFT|RIGHT} [OUTER]] JOIN table_factor
}
join_specification: {
 ON search_condition
 | USING (join_column_list) }
 ...
```

* JOIN, CROSS JOIN, and INNER JOIN等价,和sql标准不相同

  ```c
  // 简化翻译sql逻辑
  // select tbl1.col1, tbl2.col2 from tbl1 inner join tbl2 using(col3) where tbl1.col1 in (5, 6);
  // 内联没有指明驱动表,优化器会根据过滤行数少作为驱动表,这里假设选择tbl1作为驱动表
  // STRAIGHT_JOIN用来指定哪个表作为驱动表,示例如下:
  // select tbl1.col1, tbl2.col2 from tbl1 STRAIGHT_JOIN tbl2 using(col3) where tbl1.col1 in (5, 6);
  outer_iter = iterator over tbl1 where col1 in (5, 6)
  outer_row = outer_iter.next
  while outer_row
      inner_iter = iterator over tbl2 where col3 = outer_row.col3
      inner_row = inner_iter.next
      while inner_row
          output [ outer_row.col1, inner_row.col2]
          inner_row = inner_iter.next
      end
      outer_row = outer_iter.next
  end
  ```

* LEFT, RIGHT [OUTER] JOIN,外连关键词(outer)可省略,写不写都是一样功能

  ```c
  // 简化翻译sql逻辑
  // select tbl1.col1, tbl2.col2 from tbl1 left outer join tbl2 using(col3) where tbl1.col1 in (5, 6); 
  // left,right表明了哪个表作为驱动表
  outer_iter = iterator over tbl1 where col1 in (5, 6)
  outer_row = outer_iter.next
  while outer_row
      inner_iter = iterator over tbl2 where col3 = outer_row.col3
      inner_row = inner_iter.next
      if inner_row
          while inner_row
              output [ outer_row.col1, inner_row.col2]
              inner_row = inner_iter.next
          end
      else
          output [ outer_row.col1, null]
      end
          outer_row = outer_iter.next
  end
  ```

* FULL OUTER JOIN暂不支持
* NATURAL表示join_specification采用USING(join_column_list),不用手动写出来,join_column_list选取两个表都有的列名

* EXPLAIN/DESCRIBE/DESC 作用一样的

  ```sql
  -- 获取表结构/信息
  {EXPLAIN | DESCRIBE | DESC}
  tbl_name [col_name | wild]

  -- 获取执行计划信息
  {EXPLAIN | DESCRIBE | DESC}
  [explain_type]
  {explainable_stmt | FOR CONNECTION connection_id}

  -- 获取更详执行计划细信息
  {EXPLAIN | DESCRIBE | DESC} ANALYZE [FORMAT = TREE] select_statement
  explain_type: {
  FORMAT = format_name
  }
  format_name: {
  TRADITIONAL
  | JSON
  | TREE
  }
  explainable_stmt: {
  SELECT statement
  | TABLE statement
  | DELETE statement
  | INSERT statement
  | REPLACE statement
  | UPDATE statement
  }
  ```

* help语句

```sql
-- 显示select语句语法,较便利
HELP 'select'
```

### 数据类型

***

* 数字,默认是有符号(SIGNED),无符号(UNSIGNED)要特别指定

  | 类型 | 字节数 |
  | -- | -- |
  | TINYINT | 1 |
  | SMALLINT | 2 |
  | MEDIUMINT | 3 |
  | INT | 4 |
  | BIGINT | 8 |
  | FLOAT | 4 |
  | DOUBLE | 8 |
  | DECIMAL | 二进制存储 |
  * 其他有一些别名
  * All arithmetic is done using signed BIGINT or DOUBLE values

* 时间

  | 类型 | 范围 | 零值 | 说明 |
  | -- | -- | -- | -- |
  | DATE | '1000-01-01'到'9999-12-31' | '0000-00-00' | 年月日 |
  | TIME |  '-838:59:59.000000'到'838:59:59.000000' | '00:00:00' | 时分秒|
  | DATETIME |  '1000-01-01 00:00:00'到'9999-12-31 23:59:59' | 0000-00-00 00:00:00 | 年月日时分秒 |
  | TIMESTAMP |'1970-01-01 00:00:01.000000'到'2038-01-19 03:14:07.999999'| 0000-00-00 00:00:00 | 时间戳 |
  | YEAR |  别用 | '0000' | 别用,有坑 |

  * TIME,DATETIME,TIMESTAMP默认精确到秒,增加参数指定精确小数,最多到6位

  ```sql
  create table mytime (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    --  '00:00:00.000000'
    t TIME(6) not null,
    --   '1000-01-01 00:00:00.00000'
    dt DATETIME(5) not null,
    ts TIMESTAMP(4) not null,
    t2 TIME(3) not null,
    dt2 DATETIME(2) not null,
    ts2 TIMESTAMP(1) not null
  );
  ```

  * DATETIME,TIMESTAMP都可以用DEFAULT CURRENT_TIMESTAMP指定默认值

* 字符串
  * char
    * CHAR(len),VARCHAR(len)最多储存len个char字符,储存占用字节由字符集处理
    * char固定大小,varchar变化大小,指消费储存占用字节
    * varchar默认去尾空格空白
  * binary
    * BINARY(len),VARCHAR(len)最多储存len个字节,字符集转化字符后字节

  * 短字符串
  | 字符存储 | 字节存储 |
  | -- | -- |
  | char | binary |
  | varchar | varbinary |
  
  * 长字符串
  | text(字符存储,类似char) | blob(字节存储,类似binary) |
  | -- | -- |
  | tinytext | tinyblob |
  | mediumtext | mediumblob |
  | text | blob |
  | longtext | longblob |

* json

   ```sql
   create table js(v json);
   insert into js(v) values('[10, 20, 30]');
   insert into js(v) values('{"a":10}');
   ```

### 分区表

* 分类类型
  * RANGE,分区必须指定范围

  ```sql
  CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT NOT NULL,
    store_id INT NOT NULL
  )
  PARTITION BY RANGE (store_id) (
    PARTITION p0
    VALUES
      LESS THAN (6),
      PARTITION p1
    VALUES
      LESS THAN (11),
      PARTITION p2
    VALUES
      LESS THAN (16),
      PARTITION p3
    VALUES
      LESS THAN MAXVALUE
  );
  ```

  * LIST,分区必须指定集合,每条记录只能属于其中一个集合

  ```sql
  CREATE TABLE person (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
  ) PARTITION BY LIST(store_id) (
    PARTITION pNorth
    VALUES
      IN (3, 5, 6, 9, 17),
      PARTITION pEast
    VALUES
      IN (1, 2, 10, 11, 19, 20),
      PARTITION pWest
    VALUES
      IN (4, 12, 13, 14, 18),
      PARTITION pCentral
    VALUES
      IN (7, 8, 15, 16)
  );
   ```

  * HASH,注意hash分布,造成热点分区

  ```sql
  CREATE TABLE worker (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
  ) PARTITION BY [LINEAR] HASH(store_id) PARTITIONS 4;
  -- LINEAR 带上则指定hash算法
  ```

  * KEY,隐式hash,服务器采用hash(key)实现,可任意类型

  ```sql
  CREATE TABLE tm1 (s1 CHAR(32) PRIMARY KEY) PARTITION BY KEY(s1) PARTITIONS 10;
  ```

* 分区pruning

```sql
#  where子句能够转化为下面两种,optimizer优化器就能选定分区,省去不必要查找
partition_column = constant
partition_column IN (constant1, constant2, ..., constantN)

# select update delete 都需要注意
# insert 只会影响一个分区,不必考虑分区修剪
```

* Subpartitioning 子分区

* select语法

```sql
SELECT
 [ALL | DISTINCT | DISTINCTROW ]
 [HIGH_PRIORITY]
 [STRAIGHT_JOIN]
 [SQL_SMALL_RESULT] [SQL_BIG_RESULT] [SQL_BUFFER_RESULT]
 [SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
select_expr [, select_expr] ...
 [into_option]
 [FROM table_references
 [PARTITION partition_list]]
 [WHERE where_condition]
 [GROUP BY {col_name | expr | position}, ... [WITH ROLLUP]]
 [HAVING where_condition]
 [WINDOW window_name AS (window_spec)
 [, window_name AS (window_spec)] ...]
 [ORDER BY {col_name | expr | position}
 [ASC | DESC], ... [WITH ROLLUP]]
 [LIMIT {[offset,] row_count | row_count OFFSET offset}]
 [into_option]
 [FOR {UPDATE | SHARE}
 [OF tbl_name [, tbl_name] ...]
 [NOWAIT | SKIP LOCKED]
 | LOCK IN SHARE MODE]
 [into_option]
into_option: {
 INTO OUTFILE 'file_name'
 [CHARACTER SET charset_name]
export_options
 | INTO DUMPFILE 'file_name'
 | INTO var_name [, var_name] ...
}
```

* insert

```sql
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 { {VALUES | VALUE} (value_list) [, (value_list)] ... }
 [AS row_alias[(col_alias [, col_alias] ...)]]
 [ON DUPLICATE KEY UPDATE assignment_list]

INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [AS row_alias[(col_alias [, col_alias] ...)]]
 SET assignment_list
 [ON DUPLICATE KEY UPDATE assignment_list]

INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 [AS row_alias[(col_alias [, col_alias] ...)]]
 {SELECT ... 
 | TABLE table_name
 | VALUES row_constructor_list
 }
 [ON DUPLICATE KEY UPDATE assignment_list]
```

* 实例解释

  ```sql
  -- 每列采用默认值插入
  INSERT INTO tbl_name () VALUES();

  -- 允许后面出现的列引用前面列值
  -- AUTO_INCREMENT在列赋值之后,所以引用此列值会为0
  INSERT INTO tbl_name (col1,col2) VALUES(15,col1*2);

  -- With INSERT ... SELECT插入多行,速度较快,ta表中AUTO_INCREMENT仍然自增,先赋值才执行AUTO_INCREMENT
  -- 等价于 INSERT INTO ta SELECT * FROM tb

  INSERT INTO ta TABLE tb;

  -- 附上DUPLICATE,要求a,b,c至少一个是唯一或主键
  -- 当多个是唯一或主键时,任选一个执行
  -- UPDATE t1 SET c=c+1 WHERE a=1 OR b=2 LIMIT 1;
  INSERT INTO t1 (a,b,c) VALUES (1,2,3) ON DUPLICATE KEY UPDATE c=c+1;

  -- VALUES(colname)用来引用指定列插入值,相当于下面两句结果
  -- INSERT INTO t1 (a,b,c) VALUES (1,2,3) ON DUPLICATE KEY UPDATE c=3;
  -- INSERT INTO t1 (a,b,c) VALUES (4,5,6) ON DUPLICATE KEY UPDATE c=9;
  INSERT INTO t1 (a,b,c) VALUES (1,2,3),(4,5,6)
  ON DUPLICATE KEY UPDATE c=VALUES(a)+VALUES(b);
  ```

* delete

  * 删除自增字段不会重用

  * 单表

  ```sql
  DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name [[AS] tbl_alias]
  [PARTITION (partition_name [, partition_name] ...)]
  [WHERE where_condition]
  -- 删除顺序,配合limit可用来分段删除
  [ORDER BY ...]
  -- 限制删除行数,通常用来防止删除影响其他业务,每次只删除部分,多次删除
  [LIMIT row_count]
  ```

  * 多表

  ```sql
  DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
  -- 删除在from之前的表中行
  tbl_name[.*] [, tbl_name[.*]] ...
  FROM table_references
  [WHERE where_condition]

  DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
  -- 删除在from子句中表的行
  FROM tbl_name[.*] [, tbl_name[.*]] ...
  USING table_references
  [WHERE where_condition]
  ```

  * 大表删除多行,InnoDB引擎优化

  ```sql
  -- 把不删除数据插入一张新表中
  INSERT INTO t_copy SELECT * FROM t WHERE ... ;
  -- 新表,老表互换名字
  RENAME TABLE t TO t_old, t_copy TO t;
  -- 删除老表,但名字为改名后
  DROP TABLE t_old;
  ```

* replace

```sql
REPLACE [LOW_PRIORITY | DELAYED]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 { {VALUES | VALUE} (value_list) [, (value_list)] ...
 |
 VALUES row_constructor_list
 }
REPLACE [LOW_PRIORITY | DELAYED]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 SET assignment_list
REPLACE [LOW_PRIORITY | DELAYED]
 [INTO] tbl_name
 [PARTITION (partition_name [, partition_name] ...)]
 [(col_name [, col_name] ...)]
 {SELECT ... | TABLE table_name}
```

* update

```sql
UPDATE [LOW_PRIORITY] [IGNORE] table_reference
 SET assignment_list
 [WHERE where_condition]
 [ORDER BY ...]
 [LIMIT row_count]
```

### 特有功能

***

```sql
show databases;
use databasename;
show tables;
describe tablename;

#从本地导入数据
#windows用\r\n,mac用\r,linux用\n
LOAD DATA LOCAL INFILE '/path/pet.txt' INTO TABLE tablename LINES TERMINATED BY '\r\n';

#mysql查变量,获取mysql默认行为,各种参数值
SHOW VARIABLES;
#只关注想要的
SHOW VARIABLES LIKE '%timeout%'

# 查看客户端连接详情,用来检查执行客户端的sql情况，特别慢查询,多连接
show full processlist;

#客户端连接数
select client_ip,count(client_ip) as client_num 
from (select substring_index(host,':' ,1) as client_ip from information_schema.processlist ) as connect_info 
group by client_ip order by client_num desc;

#执行sql时间倒序
select * from information_schema.processlist where Command != 'Sleep' order by Time desc;

# 查看表创建语句
show create table xx;

#mysql关闭安全模式
show variables like 'SQL_SAFE_UPDATES';
SET SQL_SAFE_UPDATES = 0;

#通用日志,调试好帮手,需要root权限
show variables like '%general%';
set @@global.general_log=1;
set @@global.general_log=0;

# 设置连接超时时间,下次登陆有效
show variables like '%timeout%';
--604800=60*60*24
set @@GLOBAL.interactive_timeout=604800;
set @@GLOBAL.wait_timeout=604800;

# 查看默认引擎
show engines;

# 查询表中重复数据
select col from table group by col having count(col) > 1;

# 带忽略重复的插入
insert ignore into table(name)  value('xx')

# 常用时间函数
FROM_UNIXTIME(unix_timestamp)是MySQL里的时间函数。
UNIX_TIMESTAMP('2018-09-17') 是与之相对正好相反的时间函数 。

# IF条件表达式
IF(expr1,expr2,expr3)
--如果 expr1 为真(expr1 <> 0 以及 expr1 <> NULL)，那么 IF() 返回 expr2，否则返回 expr3。IF() 返回一个数字或字符串，这取决于它被使用的语境：

#concat把int转varchar类型
update user set nickname = concat(id,'号') where id > 0;

# 字符串替换
update user set nickname = REPLACE(id,'old', 'now') where id > 0

# 查询数据库占用空间及索引空间
# Binlog,阿里云的rds默认把它也计算在内,要手动设置控制大小.大量数据删除时,会突然增加Binlog文件
select TABLE_NAME, concat(truncate(data_length/1024/1024,2),' MB') as data_size,
concat(truncate(index_length/1024/1024,2),' MB') as index_size
from information_schema.tables where TABLE_SCHEMA = 'databaseName'
```

```bash
# 修改root密码
killall mysqld
mysqld_safe --skip-grant-tables &
update mysql.user set password=PASSWORD('newpassword') where user='root';
flush privileges;
mysqld_safe &

# 设置默认字符集
mysql -u user -D db --default-character-set=utf8 -p
```

### explain优化sql

***

```sql

explain select col from table where con group by xx order by yy;  

```

输出说明:

1. table 显示该语句涉及的表
2. type 这列很重要，显示了连接使用了哪种类别,有无使用索引，反映语句的质量。
3. possible_keys 列指出MySQL能使用哪个索引在该表中找到行
4. key 显示MySQL实际使用的键（索引）。如果没有选择索引，键是NULL。
5. key_len 显示MySQL决定使用的键长度。如果键是NULL，则长度为NULL。使用的索引的长度。在不损失精确性的情况下，长度越短越好
6. ref 显示使用哪个列或常数与key一起从表中选择行。
7. rows 显示MySQL认为它执行查询时必须检查的行数。
8. extra 包含MySQL解决查询的详细信息。
9. 其中：Explain的type显示的是访问类型，是较为重要的一个指标，结果值从好到坏依次是：
    system > const > eq_ref > ref > fulltext > ref_or_null > index_merge > unique_subquery > index_subquery > range > index > ALL（优-->差）　一般来说，得保证查询至少达到range级别，最好能达到ref，否则就可能会出现性能问题

### 碎片产生的原因

***

* 表的存储会出现碎片化，每当删除了一行内容，该段空间就会变为空白、被留空，而在一段时间内的大量删除操作，会使这种留空的空间变得比存储列表内容所使用的空间更大；
* 当执行插入操作时，MySQL会尝试使用空白空间，但如果某个空白空间一直没有被大小合适的数据占用，仍然无法将其彻底占用，就形成了碎片；
* 当MySQL对数据进行扫描时，它扫描的对象实际是列表的容量需求上限，也就是数据被写入的区域中处于峰值位置的部分；
* 清除不要数据,记得要optimize table xx;不然空间仍旧占用.

> 例如：
一个表有1万行，每行10字节，会占用10万字节存储空间，执行删除操作，只留一行，实际内容只剩下10字节，但MySQL在读取时，仍看做是10万字节的表进行处理，所以，碎片越多，就会越来越影响查询性能。

### 免密码登陆

 1. 利用.my.cnf

    ```bash
    vi ~/.my.cnf
    [client]
    # 注意mysql的库中user表,localhost和127.0.0.1区别
    host = "127.0.0.1"
    user = "user"
    password = "pwd"
    database = "xx"
    ```

 2. 利用命令行参数,或者别名

    ```bash
    mysql -h localhost -u root -p xxx
    ```

### 小知识

***

* 哪个是JOIN，哪个是过滤器?

```sql
-- 隐式内联,不好理解容易出错,不建议
-- a,b ==> inner join 简写
-- a.ID = b.ID ==> 用来关联,不是过滤,
SELECT * FROM a,b WHERE a.ID = b.ID
-- 显示内联,建议这种
-- a JOIN b ==> inner join
SELECT * FROM a JOIN b ON a.ID = b.ID
-- USING(ID) == > ON a.ID = b.ID
-- 要求两个表都存在ID列
SELECT * FROM a JOIN b USING(ID)
```

* 分组连接

```sql
select sch_id, count(sch_id) as c, GROUP_CONCAT(sch_name) from sch_basic_info sbi group by sch_id HAVING count(sch_id) > 1 order by c desc;
select  GROUP_CONCAT(sch_name) from sch_basic_info sbi group by sch_id HAVING count(sch_id) > 1;
```

* 支持opengis,geometry
![opengis](webp/ysql/mysql_opengis.webp)
  * Geometry (noninstantiable)
  * Point (instantiable)
  * Curve (noninstantiable)
  * LineString (instantiable)
  * Line
  * LinearRing
  * Surface (noninstantiable)
  * Polygon (instantiable)
  * GeometryCollection (instantiable)
  * MultiPoint (instantiable)
  * MultiCurve (noninstantiable)
  * MultiLineString (instantiable)
  * MultiSurface (noninstantiable)
  * MultiPolygon (instantiable)

### 附录

* [表一般不超过2000万行](https://my.oschina.net/u/4090830/blog/5559454)
* [postgresql-开源替代品](https://www.postgresql.org/)
* [c++-图数据库](https://www.nebula-graph.io/)
* [golang-图数据库](https://github.com/dgraph-io/dgraph)
* [ferretdb-开源的mongodb替代品](https://docs.ferretdb.io/)
