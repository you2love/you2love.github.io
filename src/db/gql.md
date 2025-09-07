# GQL
<!-- toc --> 

- 一种专为**属性图**模型设计的图查询语言
- 这是继**SQL**之后第二个数据库查询语言标准

### 二、GQL的核心数据模型：属性图（Property Graph）
GQL的所有操作都基于**属性图模型**，这是图数据的“基本结构单元”，需明确其四大核心元素：

| 元素         | 定义与特点                                                                 | 示例                          |
|--------------|----------------------------------------------------------------------------|-------------------------------|
| **节点（Node）** | 表示“实体”（如人、商品、订单），可携带**属性**（键值对），并可被**标签（Label）** 分类。 | 节点`(u:User {id: 1, name: "Alice"})`，标签为`User`，属性为`id`和`name`。 |
| **关系（Relationship）** | 表示节点间的“关联”（如“关注”“购买”“属于”），**有方向**（体现关系的语义，如“A关注B”≠“B关注A”），可携带属性，且有唯一**类型（Type）** 。 | 关系`(u)-[r:FOLLOWS {since: 2023}]->(v)`，类型为`FOLLOWS`，属性为`since`。 |
| **属性（Property）** | 附着于节点或关系的“键值对数据”，支持多种数据类型（字符串、数字、布尔、列表、结构等）。 | 节点属性`age: 30`、关系属性`weight: 0.8`（表示关系权重）。 |
| **路径（Path）** | 由“节点-关系”交替组成的序列（如`u->v->w`），表示多实体间的间接关联，是图查询的核心对象之一。 | 路径`(u:User)-[:FOLLOWS]->(v:User)-[:POSTED]->(p:Post)`（Alice关注的用户发布的帖子）。 |


### 三、GQL的核心查询能力（核心语法模块）
GQL的查询语法围绕“**模式匹配**”（图查询的灵魂）展开，同时支持传统数据库的过滤、聚合等能力，核心模块如下：

#### 1. 模式匹配（Pattern Matching）：图查询的核心
模式匹配是GQL区别于SQL的核心能力，通过“描述图的结构模式”来定位数据，语法与Cypher类似，支持**节点模式**、**关系模式**和**复合模式**。

- **基础语法**：用`()`表示节点，用`-[]->`表示有向关系，组合成“模式”后用`MATCH`关键字匹配。
- **示例1：匹配单个节点**  
  查找所有标签为`User`、且`age > 25`的用户：
  ```gql
  MATCH (u:User) 
  WHERE u.age > 25 
  RETURN u.name, u.age;
  ```
- **示例2：匹配节点+关系的复合模式**  
  查找“Alice关注的用户发布的帖子”：
  ```gql
  MATCH (alice:User {name: "Alice"})-[:FOLLOWS]->(friend:User)-[:POSTED]->(post:Post)
  RETURN post.title, post.createTime;
  ```
- **关键特性**：支持“可选匹配”（`OPTIONAL MATCH`），即模式中部分结构不存在时仍返回结果（类似SQL的`LEFT JOIN`）。


#### 2. 路径查询（Path Query）：遍历多步关联
路径是GQL的核心返回对象，支持查询“节点间的所有路径”“最短路径”“指定长度的路径”，解决层级/网状结构的遍历问题（如族谱、供应链溯源）。

- **核心语法**：通过`MATCH`匹配路径模式，用`PATH`关键字显式定义路径变量，或直接返回路径。
- **示例1：查询指定长度的路径**  
  查找“Alice到Bob的2~3步间接关系路径”（如Alice→C→Bob，Alice→C→D→Bob）：
  ```gql
  MATCH path = (alice:User {name: "Alice"})-[*2..3]->(bob:User {name: "Bob"})
  RETURN path;
  ```
- **示例2：查询最短路径**  
  GQL内置`shortestPath()`函数，查找两节点间的最短关联：
  ```gql
  MATCH shortestPath(path = (a:City {name: "Beijing"})-[*]->(b:City {name: "Shanghai"}))
  RETURN path;
  ```


#### 3. 数据操纵（Data Manipulation）：增删改
GQL标准化了图数据的全生命周期操作，语法简洁且与查询逻辑一致：

| 操作类型 | 关键字       | 功能描述                                  | 示例                                  |
|----------|--------------|-------------------------------------------|---------------------------------------|
| 新增     | `CREATE`     | 创建节点、关系或路径                      | `CREATE (u:User {id: 2, name: "Bob"})` |
| 删除     | `DELETE`     | 删除节点或关系（删除节点前需先删除关联关系） | `MATCH (u:User {name: "Bob"}) DELETE u`|
| 更新     | `SET`/`REMOVE`| 新增/修改属性（`SET`）、删除属性/标签（`REMOVE`） | `MATCH (u:User {name: "Bob"}) SET u.age = 28 REMOVE u.id` |
| 合并     | `MERGE`      | 若模式不存在则创建，存在则匹配（避免重复创建） | `MERGE (u:User {name: "Charlie"}) ON CREATE SET u.age = 30` |


#### 4. 过滤、排序与聚合（Filtering, Sorting & Aggregation）
GQL支持传统数据库的“筛选-排序-聚合”流程，且适配图结构的特性（如按关系数量聚合）：

- **过滤（`WHERE`）**：支持属性条件（`u.age > 25`）、结构条件（`EXISTS((u)-[:FOLLOWS]->())`，判断用户是否有关注关系）、列表条件（`u.tags CONTAINS "tech"`）。
- **排序（`ORDER BY`）**：按属性升序（`ASC`）或降序（`DESC`）排序，支持多字段排序。
- **聚合（`AGGREGATION FUNCTIONS`）**：内置常用聚合函数，部分函数专为图设计：
  | 聚合函数       | 功能描述                                  | 示例                                  |
  |----------------|-------------------------------------------|---------------------------------------|
  | `COUNT()`      | 统计节点/关系/路径数量                    | `MATCH (u:User)-[:FOLLOWS]->() RETURN u.name, COUNT(*)`（统计每个用户的关注数） |
  | `SUM()`/`AVG()`| 求和/求平均值（属性需为数值类型）         | `MATCH (p:Post) RETURN AVG(p.likes)`（统计帖子平均点赞数） |
  | `COLLECT()`    | 将结果聚合为列表                          | `MATCH (u:User)-[:POSTED]->(p:Post) RETURN u.name, COLLECT(p.title)`（聚合每个用户的帖子标题） |


#### 5. 递归查询（Recursive Query）：处理深层层级结构
GQL通过`WITH RECURSIVE`语法支持递归查询，解决“无限层级”场景（如组织结构树、分类目录树），无需手动写多步匹配。

- **示例：查询“Alice所在部门的所有下属（含多级）”**  
  ```gql
  WITH RECURSIVE
    // 基础 case：Alice的直接下属
    direct_subordinates AS (
      MATCH (alice:User {name: "Alice"})-[:MANAGES]->(sub:User)
      RETURN sub.name AS username
    ),
    // 递归 case：下属的下属（循环直到无更多层级）
    all_subordinates AS (
      SELECT username FROM direct_subordinates
      UNION ALL
      MATCH (s:User {name: all_subordinates.username})-[:MANAGES]->(ss:User)
      RETURN ss.name AS username
    )
  // 返回所有下属
  SELECT username FROM all_subordinates;
  ```

### 二、数据定义语言（DDL）：定义图结构

GQL 支持对图的元数据（如标签、关系类型、属性类型）进行定义，确保数据一致性（类似 SQL 的`CREATE TABLE`）。

#### 1. 定义标签（节点类型）

```
// 定义标签User，并指定其属性及类型（可选，增强类型校验）

CREATE TAG User (

 id INT REQUIRED,  // 必选属性，整数类型

 name STRING REQUIRED,  // 必选属性，字符串类型

 age INT,  // 可选属性

 active BOOLEAN DEFAULT true  // 可选属性，默认值为true

);
```

#### 2. 定义关系类型

```
// 定义关系类型FOLLOWS，指定属性及类型

CREATE RELATIONSHIP FOLLOWS (

 since DATE REQUIRED,  // 必选属性，日期类型

 weight FLOAT DEFAULT 0.5  // 可选属性，浮点类型

);
```

#### 3. 创建图（数据库）

```
// 创建一个名为"social_network"的图数据库

CREATE GRAPH social_network;

// 切换到指定图

USE GRAPH social_network;
```

### 三、数据操纵语言（DML）：增删改图数据

GQL 提供直观的语法用于操作节点、关系和属性，覆盖数据全生命周期。

#### 1. 创建数据（`CREATE`）

*   **创建节点**

```
// 创建单个节点（可省略标签定义时的类型校验，直接动态添加属性）

CREATE (u:User {id: 2, name: "Bob", age: 28, city: "London"});

// 同时创建多个节点

CREATE (p1:Product {id: 101, name: "Laptop", price: 9999}),

      (p2:Product {id: 102, name: "Phone", price: 5999});
```

*   **创建关系（需关联已有节点）**

```
// 先匹配两个节点，再创建它们之间的关系

MATCH (u:User {name: "Alice"}), (p:Product {name: "Phone"})

CREATE (u)-\[b:BOUGHT {time: "2024-03-15", amount: 5999}]->(p);
```

*   **创建路径（节点 + 关系一次性创建）**

```
// 创建"Charlie"→关注→"Bob"→购买→"Laptop"的完整路径

CREATE (c:User {name: "Charlie"})-\[f:FOLLOWS]->(b:User {name: "Bob"})-\[b2:BOUGHT]->(l:Product {name: "Laptop"});
```

#### 2. 更新数据（`SET`/`REMOVE`）

*   **更新属性（**`SET`**）**

```
// 修改Alice的年龄，新增city属性

MATCH (u:User {name: "Alice"})

SET u.age = 31, u.city = "Paris";
```

*   **删除属性或标签（**`REMOVE`**）**

```
// 移除Bob的city属性，移除User标签（需谨慎，可能影响查询）

MATCH (u:User {name: "Bob"})

REMOVE u.city, u:User;
```

*   **批量更新（基于条件）**


```
// 给所有age>30的User添加"Senior"标签

MATCH (u:User)

WHERE u.age > 30

SET u:Senior;
```

#### 3. 删除数据（`DELETE`/`DETACH DELETE`）



*   **删除关系**



```
// 删除Alice购买Phone的关系

MATCH (u:User {name: "Alice"})-\[b:BOUGHT]->(p:Product {name: "Phone"})

DELETE b;
```



*   **删除节点（需先删除关联关系，否则报错）**


```
// 方法1：先删关系，再删节点

MATCH (u:User {name: "Charlie"})-\[r]->()

DELETE r;  // 删除所有出向关系

MATCH (u:User {name: "Charlie"})

DELETE u;  // 删除节点

// 方法2：用DETACH DELETE一键删除节点及所有关联关系（推荐）

MATCH (u:User {name: "Charlie"})

DETACH DELETE u;
```

#### 4. 合并数据（`MERGE`：避免重复创建）

`MERGE` 用于 “若模式存在则匹配，不存在则创建”，适合防止重复数据：



```
// 若"Dave"用户存在则匹配，不存在则创建并设置age=25

MERGE (u:User {name: "Dave"})

ON CREATE SET u.age = 25  // 仅在创建时执行

ON MATCH SET u.lastSeen = CURRENT_DATE();  // 仅在匹配时执行（更新最后访问时间）
```

### 四、数据查询语言（DQL）：查询图数据

查询是 GQL 的核心能力，通过 “模式匹配” 定位数据，支持过滤、排序、聚合等操作。

#### 1. 基础查询（`MATCH`+`RETURN`）



```
// 查询所有User节点的name和age

MATCH (u:User)

RETURN u.name, u.age;

// 给结果起别名

MATCH (u:User)

RETURN u.name AS username, u.age AS user_age;
```

#### 2. 条件过滤（`WHERE`）

支持属性条件、结构条件、逻辑运算（`AND`/`OR`/`NOT`）：



```
// 条件1：属性过滤（age>25且city为"Paris"）

MATCH (u:User)

WHERE u.age > 25 AND u.city = "Paris"

RETURN u.name;

// 条件2：结构过滤（存在关注关系的用户）

MATCH (u:User)

WHERE EXISTS((u)-\[:FOLLOWS]->())  // 检查u是否有出向的FOLLOWS关系

RETURN u.name;

// 条件3：列表包含（tags属性包含"tech"）

MATCH (p:Post)

WHERE "tech" IN p.tags

RETURN p.title;
```

#### 3. 关系模式匹配（核心能力）

通过描述 “节点 - 关系” 模式查询关联数据：



```
// 查询所有购买了Product的User，返回用户名和商品名

MATCH (u:User)-\[b:BOUGHT]->(p:Product)

RETURN u.name, p.name, b.time;

// 查询Alice的直接好友（1度关系）

MATCH (alice:User {name: "Alice"})-\[f:FOLLOWS]->(friend:User)

RETURN friend.name;

// 查询Alice的好友购买的商品（2度关系）

MATCH (alice:User {name: "Alice"})-\[:FOLLOWS]->(friend:User)-\[b:BOUGHT]->(p:Product)

RETURN friend.name, p.name;
```

#### 4. 路径查询（多跳关系）

用`*n`表示关系的长度（`n`为数字或范围），支持灵活的多跳遍历：

```
// 查询Alice的1\~3度好友（1到3跳FOLLOWS关系）

MATCH (alice:User {name: "Alice"})-\[f:FOLLOWS\*1..3]->(friend:User)

RETURN friend.name, LENGTH(f) AS degree;  // LENGTH(f)返回路径长度

// 查询Alice到Bob的所有路径（不限长度）

MATCH path = (alice:User {name: "Alice"})-\[\*]->(bob:User {name: "Bob"})

RETURN path;
```

#### 5. 可选匹配（`OPTIONAL MATCH`：类似左连接）

当模式中部分结构不存在时，仍返回已有部分（避免数据丢失）：



```
// 查询所有User及其购买的商品，没有购买记录的User也会返回（商品字段为NULL）

MATCH (u:User)

OPTIONAL MATCH (u)-\[b:BOUGHT]->(p:Product)

RETURN u.name, p.name;
```

#### 6. 排序与限制（`ORDER BY`/`LIMIT`/`SKIP`）



```
// 查询所有Product，按价格降序排列，返回前3个（分页：跳过前2个，取3个）

MATCH (p:Product)

RETURN p.name, p.price

ORDER BY p.price DESC

SKIP 2  // 跳过前2条

LIMIT 3;  // 最多返回3条
```

### 五、聚合查询（`AGGREGATION`）

GQL 提供丰富的聚合函数，支持对节点、关系或路径的统计分析：



| 函数              | 功能        | 示例                                                                                           |
| --------------- | --------- | -------------------------------------------------------------------------------------------- |
| `COUNT()`       | 统计数量      | `MATCH (u:User)-[b:BOUGHT]->() RETURN u.name, COUNT(b) AS buy_count`（统计用户购买次数）               |
| `SUM()`         | 求和        | `MATCH (p:Product) RETURN SUM(p.price) AS total_value`（统计所有商品总价）                             |
| `AVG()`         | 平均值       | `MATCH (u:User) RETURN AVG(u.age) AS avg_age`（统计用户平均年龄）                                      |
| `MIN()`/`MAX()` | 最小值 / 最大值 | `MATCH (p:Product) RETURN MIN(p.price) AS cheapest`（最便宜的商品价格）                                |
| `COLLECT()`     | 聚合为列表     | `MATCH (u:User)-[:POSTED]->(p:Post) RETURN u.name, COLLECT(p.title) AS posts`（聚合用户发布的所有帖子标题） |

示例：按标签分组统计节点数量



```
// 统计每个标签的节点数量（如User、Product各有多少节点）

MATCH (n)

RETURN LABELS(n) AS tags, COUNT(n) AS node_count

ORDER BY node_count DESC;
```

### 六、递归查询（`WITH RECURSIVE`）

处理无限层级结构（如组织结构、分类树），通过递归遍历所有层级：



```
// 查询"Alice"管理的所有下属（含多级：直接下属→下属的下属→...）

WITH RECURSIVE

 // 基础case：直接下属

 direct_subs AS (

   MATCH (alice:User {name: "Alice"})-\[:MANAGES]->(sub:User)

   RETURN sub.id AS sub_id, sub.name AS sub_name, 1 AS level  // level=1表示直接下属

 ),

 // 递归case：下属的下属（循环直到无更多层级）

 all_subs AS (

   SELECT sub_id, sub_name, level FROM direct_subs

   UNION ALL  // 合并结果（保留重复，若去重用UNION）

   MATCH (s:User {id: all_subs.sub_id})-\[:MANAGES]->(ss:User)

   RETURN ss.id AS sub_id, ss.name AS sub_name, all_subs.level + 1 AS level  // 层级+1

 )

// 返回所有下属及层级

SELECT sub_name, level FROM all_subs

ORDER BY level;
```

### 七、事务（`TRANSACTION`）

GQL 支持 ACID 事务，确保多操作的原子性（要么全成功，要么全失败）：



```
// 开始事务

BEGIN TRANSACTION;

// 事务内操作：创建用户并创建其部门关系

CREATE (u:User {id: 5, name: "Eve"});

MATCH (u:User {name: "Eve"}), (d:Dept {name: "Engineering"})

CREATE (u)-\[:WORKS_IN]->(d);

// 提交事务（所有操作生效）

COMMIT;

// 若操作有误，回滚事务（所有操作取消）

// ROLLBACK;
```

### 八、视图与片段（复用查询逻辑）

#### 1. 视图（`VIEW`：虚拟图）

将常用查询结果定义为视图，后续可直接引用：



```
// 创建"高价值用户"视图（购买金额>10000的用户）

CREATE VIEW HighValueUser AS

 MATCH (u:User)-\[b:BOUGHT]->()

 WITH u, SUM(b.amount) AS total_spent

 WHERE total_spent > 10000

 RETURN u;

// 查询视图

MATCH (hvu:HighValueUser)

RETURN hvu.name, hvu.city;
```

#### 2. 片段（`FRAGMENT`：复用模式）

定义重复使用的模式片段，减少代码冗余：

```
// 定义"用户发布帖子"的模式片段

DEFINE FRAGMENT UserPost AS (u:User)-\[:POSTED]->(p:Post);

// 引用片段查询（查找发布了"tech"标签帖子的用户）

MATCH UserPost

WHERE "tech" IN p.tags

RETURN u.name, p.title;
```