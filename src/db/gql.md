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
