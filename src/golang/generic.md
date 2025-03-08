---
# 泛型
---

# 示例

```golang
// go 1.18+
package main

import (
 "fmt"
)
type SubType interface {
 int | string | float32
}

// func Sub[T int | string | float32](array []T, ele T) []T {
func Sub[T SubType](array []T, ele T) []T {
 res := make([]T, 0, len(array))

 for _, a := range array {
  if a == ele {
   continue
  }
  res = append(res, a)
 }
 return res
}

func main() {
 fmt.Println(Sub([]string{"a", "b", "c", "b"}, "b"))

 fmt.Println(Sub([]int{10, 20, 30, 10}, 10))
}
```

在软件开发中，自动生成代码可以显著提高开发效率，减少重复劳动。以下是一些常用的工具和框架，能够自动生成 Go 代码：

---

### 1. **Protocol Buffers (protobuf)**

- **用途**：用于定义数据结构并生成序列化代码。
- **工具**：`protoc` + `protoc-gen-go` 插件。
- **示例**：

     ```bash
     protoc --go_out=. --go_opt=paths=source_relative your_proto_file.proto
     ```

- **生成内容**：根据 `.proto` 文件生成 Go 结构体和序列化代码。

---

### 2. **gRPC**

- **用途**：用于生成 RPC 服务的客户端和服务器端代码。
- **工具**：`protoc` + `protoc-gen-go-grpc` 插件。
- **示例**：

     ```bash
     protoc --go-grpc_out=. --go-grpc_opt=paths=source_relative your_proto_file.proto
     ```

- **生成内容**：生成 gRPC 服务的接口和实现代码。

---

### 3. **Swagger/OpenAPI**

- **用途**：用于生成 RESTful API 的客户端和服务器端代码。
- **工具**：
  - **oapi-codegen**：根据 OpenAPI 规范生成 Go 代码。
  - **swagger-codegen**：生成多种语言的客户端和服务端代码。
- **示例**：

     ```bash
     oapi-codegen -generate types,server -package myapi myapi.yaml > myapi.gen.go
     ```

- **生成内容**：生成 API 的类型定义、路由和处理函数。

---

### 4. **SQLBoiler**

- **用途**：根据数据库表结构生成 Go 模型和 CRUD 代码。
- **工具**：`sqlboiler`。
- **示例**：

     ```bash
     sqlboiler psql
     ```

- **生成内容**：生成与数据库表对应的 Go 模型、查询和操作方法。

---

### 5. **GORM**

- **用途**：用于生成 ORM 模型代码。
- **工具**：`gorm` + `gorm-gen`。
- **示例**：

     ```bash
     gorm-gen -dsn "user:password@tcp(127.0.0.1:3306)/dbname" -outPath ./models
     ```

- **生成内容**：生成数据库表对应的 ORM 模型代码。

---

### 6. **Wire**

- **用途**：用于生成依赖注入代码。
- **工具**：`wire`。
- **示例**：

     ```bash
     wire gen ./...
     ```

- **生成内容**：生成依赖注入的初始化代码。

---

### 7. **Mockery**

- **用途**：用于生成接口的 Mock 实现。
- **工具**：`mockery`。
- **示例**：

     ```bash
     mockery --name=MyInterface --output=mocks
     ```

- **生成内容**：生成接口的 Mock 实现，用于单元测试。

---

### 8. **Go Generate**

- **用途**：用于自定义代码生成。
- **工具**：`go generate`。
- **示例**：
     在 Go 文件中添加：

     ```go
     //go:generate stringer -type=MyEnum
     ```

     然后运行：

     ```bash
     go generate ./...
     ```

- **生成内容**：根据自定义规则生成代码（如枚举的字符串表示）。

---

### 9. **Ent**

- **用途**：用于生成实体模型和 CRUD 代码。
- **工具**：`ent`。
- **示例**：

     ```bash
     go run entgo.io/ent/cmd/ent generate ./ent/schema
     ```

- **生成内容**：生成实体模型、查询和操作方法。

---

### 10. **Cobra**

- **用途**：用于生成命令行应用程序的框架代码。
- **工具**：`cobra-cli`。
- **示例**：

     ```bash
     cobra-cli init myapp
     cobra-cli add mycommand
     ```

- **生成内容**：生成命令行应用程序的框架代码和子命令。

---

### 11. **Goa**

- **用途**：用于生成微服务框架代码。
- **工具**：`goa`。
- **示例**：

     ```bash
     goa gen myapp/design
     ```

- **生成内容**：生成微服务的 API 定义、路由和处理函数。

---

### 12. **Gunk**

- **用途**：用于生成 gRPC 和 RESTful API 代码。
- **工具**：`gunk`。
- **示例**：

     ```bash
     gunk generate ./...
     ```

- **生成内容**：生成 gRPC 和 RESTful API 的代码。

---

### 13. **Go Kit**

- **用途**：用于生成微服务框架代码。
- **工具**：`go-kit`。
- **示例**：

     ```bash
     go-kit addsvc -gen
     ```

- **生成内容**：生成微服务的框架代码。

---

### 14. **Go-Fuzz**

- **用途**：用于生成模糊测试代码。
- **工具**：`go-fuzz`。
- **示例**：

     ```bash
     go-fuzz-build -o=fuzz.zip .
     ```

- **生成内容**：生成模糊测试的代码。

---

### 15. **GoReleaser**

- **用途**：用于生成发布流程的配置文件。
- **工具**：`goreleaser`。
- **示例**：

     ```bash
     goreleaser init
     ```

- **生成内容**：生成 `.goreleaser.yml` 配置文件。

---

### 总结

以上工具涵盖了从数据结构定义、API 生成、数据库操作到测试和发布的各个方面。根据具体需求选择合适的工具，可以显著提高 Go 开发的效率和质量。
