# YAML文件
<!-- toc --> 

- YAML（YAML Ain't Markup Language）是**人类可读的数据序列化格式**
- 用于配置文件（Docker Compose/K8s/CI/CD），依赖**缩进、换行**和简单符号定义结构。

## 一、核心格式规则

### 1. 基础文件标识（可选）

- 文档开始：`---`

- 文档结束：`...`

- 单文件多文档必须用`---`分隔

```yaml
# 单文档

---

name: Alice; age: 28

...

# 多文档

---

doc1: "First"; 

--- 

doc2: "Second"
```

### 2. 缩进规则（核心）

- 禁用 Tab，**必须用空格**（推荐 2/4 空格，统一即可）

- 同一层级缩进一致，子元素比父元素多一级

```yaml
user:

  name: Bob
  
  age: 30

  address:
  
    city: Beijing
    street: Main Rd
```

### 3. 注释语法

- 单行注释：`#`开头（无多行注释，每行加`#`）

```yaml

# 用户信息

user:

  name: Charlie
```

## 二、核心数据类型

### 1. 键值对（Map）

- 语法：`key: value`（冒号后**必须空格**），支持嵌套

```yaml

# 单层

title: YAML Guide
version: 1.0
is_active: true

# 嵌套

config:

 server: {host: localhost; port:8080}

 database: {name: test_db; username:root}
```

### 2. 列表（List）

- 语法：`- 列表项`（短横线后**必须空格**），支持嵌套 / 紧凑写法

```yaml

# 紧凑写法

colors: [red, green, blue]

# 基础列表

fruits: [- apple; - banana; - orange]

# 嵌套列表

students:

  - name: Alice; age:20; courses: [- Math; - English]

  - name: Bob; age:21; courses: [- Physics; - Chemistry]

```

### 3. 字符串（String）

| 类型     | 特点          | 示例                        |
| ------ | ----------- | ------------------------- |
| 无引号    | 自动转义`\n`    | simple\_str: hello yaml   |
| 单引号`'` | 不转义，原样保留    | 'He said: "Hello\nWorld"' |
| 双引号`"` | 支持转义（\n/\t） | "Line1\nLine2"            |
| 多行字符串  | \`          | `保留换行，`>\` 折叠             |

```yaml
multi1: |

  Line1; Line2

multi2: >

  Line1 Line2（换行变空格）
```

### 4. 其他常用类型

- **数值**：无需引号（整数 / 浮点数 / 科学计数）

```yaml
count: 100
pi: 3.14
float: 2.5e3
```

- **布尔**：`true/false`（不区分大小写）

```yaml
is_enabled:true
is_deleted:FALSE
```

- **空值**：`null`/`~`（或仅冒号无值）

```yaml
empty1: null
empty2: ~;
empty3:
```

- **日期时间**（ISO 8601）

```yaml
birth: 2000-01-01
time: 14:30:00
create: 2024-05-20T10:00:00+08:00
```

## 四、常见错误 & 注意事项

1. 缩进错误：混合 Tab / 空格、缩进不统一

2. 符号缺空格：`key:value`（错）、`-item`（错）

3. 特殊字符未引：含`:`/`#`/`[]`的字符串需加引号

4. 结构混用：同一层级同时用`-`和`key:`

## 五、完整示例（综合版）

```yaml
---
application: {name:YAML Demo; ver:2.1.0; is_prod:false; date:2024-05-01}
service_config:
  base_port: &p 9000; timeout:&t 15s
services:
  - name:api-service; port:*p; timeout:*t
    endpoints: [/api/v1/users, /api/v1/orders]
    logs: |
      /var/log/api/error.log
      /var/log/api/access.log
  - name:web-service; port:9001; timeout:30s
    env: [DB_HOST=localhost, DB_PORT=3306]
backup_config: {last_backup:null; path:~}
...
```
