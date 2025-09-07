# Cypher
<!-- toc --> 

### 简介

- 属性图
- 节点
- 关系(边)
- 路径

### 基础语法结构

1. **节点表示**

	* 基础格式：`(变量:标签 {属性键:属性值})`
		* 变量：可选，用于后续引用（如 `n`）。
		* 标签：可选，用于对节点进行分类（如 `User`）。
		* 属性：可选，键值对（如 `{name: "Alice"}`）。
	* 示例：
		* `(:Person)`：匿名 `Person` 节点。
		* `(p:Employee)`：别名为 `p` 的 `Employee` 节点。
		* `(:Book {title:"Neo4j Guide"})`：带属性的匿名节点。

2. **关系表示**

	* 基础格式：`[变量:类型 {属性键:属性值}]`
	* 方向：`-->`（出边）或 `<--`（入边）。
	* 示例：
		* `(a)-[:FRIEND]->(b)`：无属性关系。
		* `(a)-[r:FOLLOWS {since:2020}]->(b)`：带属性和变量的关系。

### 核心命令详解

1. **MATCH（模式匹配）**

	* 功能：定位图中的节点/关系。
	* 示例：
		* 查找 `Alice` 的朋友：`MATCH (a:User {name:"Alice"})-[:FRIEND]->(friend) RETURN friend.name`。
		* 查找所有电影及其导演：`MATCH (d:Director)-[:DIRECTED]->(m:Movie) RETURN d.name, m.title`。

2. **WHERE（条件过滤）**

	* 支持运算符：`=`、`>`、`<`、`<>`、`CONTAINS`、`STARTS WITH`、`IS NULL`、`IS NOT NULL` 等。
	* 示例：
		* 查找年龄大于 30 的用户：`MATCH(u:User) WHERE u.age>30 RETURN u`。
		* 查找名字以 "A" 开头的用户：`MATCH(u:User) WHERE u.name=~'A.*' RETURN u`。

3. **RETURN（结果返回）**

	* 支持聚合函数：`COUNT()`、`SUM()`、`AVG()`、`COLLECT()` 等。
	* 示例：
		* 返回节点和标签：`MATCH (n {name:"zhangsan"}) RETURN n, labels(n)`。
		* 统计每种职业的平均年龄：`MATCH (n:Person) RETURN n.profession, avg(n.age)`。

4. **CREATE（数据创建）**

	* 创建节点：`CREATE (n:Person {name: "Alice", age: 30})`。
	* 创建关系：`CREATE (a:User {name: "Alice"}), (b:User {name: "Bob"}) CREATE (a)-[:FRIEND]->(b)`。
	* 节点与关系同步创建：`CREATE (a:User {name:"Bob"})-[:WORKS_AT]->(c:Company {name:"Neo4j"})`。

5. **SET（属性更新）**

	* 修改属性：`MATCH (u:User {name:"Alice"}) SET u.age = 31`。
	* 添加新属性：`MATCH (n:Person {name: 'Alice'}) SET n.email = 'alice@example.com'`。
	* 更新关系属性：`MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'}) SET r.since = 2022`。
	* 添加标签：`MATCH (u:User {name:"Bob"}) SET u:VIP`。

6. **DELETE（数据删除）**

	* 删除节点：需先删除关联关系，`MATCH (u:User)-[r]-() DELETE r, u` 或 `MATCH (u:User {name:"Bob"}) DETACH DELETE u`。
	* 删除关系：`MATCH (a:Person {name: 'Alice'})-[r:KNOWS]->(b:Person {name: 'Bob'}) DELETE r`。
	* 删除属性：`MATCH (u:User {name:"Alice"}) REMOVE u.age`。

### 高级查询功能

1. **路径查询**

	* 多跳关系：使用 `*n..m` 指定跳数范围，如 `MATCH (a:User)-[:FRIEND*2]->(c:User) WHERE a.id=123 RETURN c.name`（查找朋友的朋友）。
	* 最短路径：使用 `shortestPath` 函数，如 `MATCH path = shortestPath((a:User)-[:FRIEND*..5]-(b:User)) WHERE a.id=1 AND b.id=100 RETURN path`。

2. **聚合与分组**

	* 统计数量：`MATCH (u:User)-[:BOUGHT]->(p:Product) RETURN u.name, COUNT(p) AS purchase_count`。
	* 分组统计：`MATCH (p:Person)-[:WORKS_AT]->(c:Company) RETURN c.name, COUNT(p) AS employeeCount`。

3. **分页与排序**

	* 分页查询：`MATCH (p:Person) RETURN p.name ORDER BY p.age DESC SKIP 10 LIMIT 5`（跳过前 10 条结果，返回接下来的 5 条）。
	* 动态分页：`MATCH (p:Person) RETURN p.name ORDER BY p.age DESC SKIP $offset LIMIT $limit`（使用参数 `$offset` 和 `$limit` 控制分页）。

4. **WITH 子句**

	* 功能：将查询结果传递给下一个部分，允许在查询中进行聚合、排序、分页等操作。
	* 示例：
		* 过滤聚合函数的结果：`MATCH (n {name: "zhangsan" })--(m)-->(s) WITH m, COUNT(*) AS m_count WHERE m_count>1 RETURN m`。
		* 限制路径搜索的分支：`MATCH (n {name: "zhangsan"})--(m) WITH m ORDER BY m.name DESC LIMIT 1 MATCH (m)--(o) RETURN o.name`。

5. **UNION 和 UNION ALL**

	* 功能：将多个查询结果组合起来。`UNION` 会移除重复的行，`UNION ALL` 会包含所有的结果不会移除重复的行。
	* 示例：
		* 去重：`MATCH (n:Person) RETURN n.name AS name UNION MATCH(n:Movie) RETURN b.title AS name`。
		* 不去重：`MATCH (n:Person) RETURN n.name AS name UNION ALL MATCH(n:Movie) RETURN b.title AS name`。

6. **CALL 子句**

	* 功能：调用数据库中的内置过程（Procedure），内置过程类似于关系型数据库中的存储过程，是一组完成特定功能的方法。
	* 示例：
		* 调用数据库内置过程查询数据库中所有的点类型：`CALL db.labels()`。
		* 调用内置过程并将结果绑定变量或过滤：`CALL db.labels() yield label return count(type) as numTypes`。

### 性能优化技巧

- **使用索引**

	* 为属性创建索引加速查询：`CREATE INDEX FOR (p:Person) ON (p.name)`。

- **标签限定**

    * 在 MATCH 中优先使用标签缩小搜索范围，避免全图扫描

```cypher
MATCH (a:User) 
WHERE a.name STARTS WITH 'A'
RETURN a;
```

2. **执行计划分析**

	* 使用 `EXPLAIN` 查看查询的执行计划，避免全图扫描：`EXPLAIN MATCH (p:Person {name: "Alice"}) RETURN p`。

3. **参数化查询**

	* 防止注入攻击：`MATCH (p:Person {name: $name}) RETURN p`。使用 `$name` 替代直接拼接参数。

### 注释与参数化查询

1. **注释**

	* 单行注释：使用 `//` 进行单行注释，如 `// 这是一个单行注释 MATCH (n:Person) RETURN n`。
	* 多行注释：使用 `/* ... */` 进行多行注释，如 `/* 这是一个多行注释 */ MATCH (n:Person) RETURN n`。

2. **参数化查询**

	* Cypher 支持通过参数化查询来提高性能和安全性，通常用于防止 SQL 注入攻击。例如：`MATCH (n:Person {name: $name}) RETURN n`。

### **实际场景示例：社交网络分析**

**场景**：查找与 `Alice` 有共同兴趣且购买过高价商品的朋友。  
**查询**：  
```cypher
MATCH 
  (a:Person {name: 'Alice'})-[:FRIEND]->(b:Person),
  (b)-[:INTEREST]->(i:Interest),
  (a)-[:INTEREST]->(i),
  (b)-[:BUY]->(p:Product)
WHERE p.price > 1000
RETURN DISTINCT b.name, i.name, p.name;
```
- **步骤解析**：  
  1. 匹配 `Alice` 的朋友 `b`（`FRIEND` 关系）。  
  2. 匹配 `b` 和 `Alice` 的共同兴趣 `i`（`INTEREST` 关系）。  
  3. 匹配 `b` 购买的高价商品 `p`（`BUY` 关系且价格 > 1000）。  
  4. 返回去重后的结果：朋友姓名、共同兴趣、购买商品。