# ast

Go 语言的 `ast`（Abstract Syntax Tree，抽象语法树）包是标准库中用于代码分析的核心工具，常用于代码检查、格式化、自动化重构等场景。以下是对 `ast` 包的详细说明和用法指南：

---

### **1. AST 基础概念**

- **抽象语法树**：将源代码解析为树状数据结构，保留逻辑结构但忽略细节（如空格、注释）。
- **节点类型**：所有 AST 节点实现 `ast.Node` 接口，常见类型包括：
  - `ast.File`: 单个 Go 文件
  - `ast.FuncDecl`: 函数声明
  - `ast.StructType`: 结构体定义
  - `ast.CallExpr`: 函数调用表达式

---

### **2. 核心流程**

#### **步骤 1：解析源代码**

使用 `go/parser` 将代码转换为 AST：

```go
fset := token.NewFileSet()
node, err := parser.ParseFile(fset, "demo.go", srcCode, parser.ParseComments)
// node 是 *ast.File 类型
```

#### **步骤 2：遍历 AST**

通过 `ast.Inspect` 或自定义遍历函数递归访问节点：

```go
ast.Inspect(node, func(n ast.Node) bool {
    if ident, ok := n.(*ast.Ident); ok {
        fmt.Println("Found identifier:", ident.Name)
    }
    return true // 继续遍历子节点
})
```

---

### **3. 关键结构体**

- **`ast.File`**: 文件节点

  ```go
  type File struct {
      Name    *Ident       // 包名
      Decls   []Decl       // 顶级声明（函数、结构体等）
      Imports []*ImportSpec // 导入声明
  }
  ```

- **`ast.FuncDecl`**: 函数声明

  ```go
  type FuncDecl struct {
      Recv *FieldList     // 接收器（方法）
      Name *Ident         // 函数名
      Type *FuncType      // 函数签名
      Body *BlockStmt     // 函数体
  }
  ```

- **`ast.StructType`**: 结构体定义

  ```go
  type StructType struct {
      Fields *FieldList   // 字段列表
  }
  ```

---

### **4. 实战示例**

#### **示例 1：提取所有函数名**

```go
func extractFunctions(node *ast.File) {
    for _, decl := range node.Decls {
        if fn, ok := decl.(*ast.FuncDecl); ok {
            fmt.Println("Function:", fn.Name.Name)
        }
    }
}
```

#### **示例 2：查找特定函数调用**

```go
func findPrintfCalls(node ast.Node) {
    ast.Inspect(node, func(n ast.Node) bool {
        if call, ok := n.(*ast.CallExpr); ok {
            if ident, ok := call.Fun.(*ast.Ident); ok && ident.Name == "Printf" {
                fmt.Printf("Found Printf at %v\n", fset.Position(n.Pos()))
            }
        }
        return true
    })
}
```

---

### **5. 高级技巧**

#### **修改 AST**

使用 `astutil` 包进行代码修改：

```go
// 重命名变量
newNode := astutil.Apply(node, func(cr *astutil.Cursor) bool {
    if ident, ok := cr.Node().(*ast.Ident); ok && ident.Name == "oldVar" {
        ident.Name = "newVar"
    }
    return true
}, nil)
```

#### **类型检查**

结合 `go/types` 包进行语义分析：

```go
conf := types.Config{Importer: importer.Default()}
info := &types.Info{Types: make(map[ast.Expr]types.TypeAndValue)}
_, err := conf.Check("pkg", fset, []*ast.File{node}, info)
```

---

### **6. 常见问题**

- **忽略注释**：`parser.ParseFile` 需设置 `parser.ParseComments` 标志。
- **处理作用域**：需手动跟踪变量作用域或依赖 `go/types`。
- **性能优化**：避免在大型代码库中频繁解析，可缓存 AST。

---

### **7. 工具推荐**

- **`astview`**: 可视化 AST 结构的第三方工具
- **`golang.org/x/tools/go/analysis`**: 官方静态分析框架

通过掌握 `ast` 包，你可以构建自定义代码分析工具（如 Linter、自动重构工具），深入理解 Go 代码的内在逻辑结构。

Go 语言的 `ast`（抽象语法树）包在代码分析、生成和转换中有着广泛的应用。以下是一些典型应用场景、实现方法和实战示例：

---

### **1. 静态代码分析**

#### **场景**

- **代码规范检查**：检查命名规范、未使用的变量、错误的函数调用等。
- **安全扫描**：检测 SQL 注入、硬编码密码等潜在漏洞。
- **依赖分析**：统计包或函数的依赖关系。

#### **示例：检测 `fmt.Printf` 未格式化参数**

```go
func CheckPrintfArgs(node *ast.File, fset *token.FileSet) {
    ast.Inspect(node, func(n ast.Node) bool {
        callExpr, ok := n.(*ast.CallExpr)
        if !ok {
            return true
        }

        // 检查是否为 fmt.Printf
        if selExpr, ok := callExpr.Fun.(*ast.SelectorExpr); ok {
            if pkgIdent, ok := selExpr.X.(*ast.Ident); ok && pkgIdent.Name == "fmt" {
                if selExpr.Sel.Name == "Printf" {
                    // 检查第一个参数是否为格式化字符串
                    if len(callExpr.Args) == 0 {
                        pos := fset.Position(callExpr.Pos())
                        fmt.Printf("错误：%s 处缺少格式化参数\n", pos)
                    }
                }
            }
        }
        return true
    })
}
```

---

### **2. 自动生成代码**

#### **场景**

- **生成序列化/反序列化代码**（如 JSON、Protobuf）。
- **生成 API 路由**：根据注释自动生成 HTTP 路由。
- **实现依赖注入框架**：自动解析结构体依赖。

#### **示例：根据结构体生成 JSON 标签**

```go
// 为结构体字段自动添加 JSON 标签
func AddJSONTags(node *ast.File) {
    for _, decl := range node.Decls {
        genDecl, ok := decl.(*ast.GenDecl)
        if !ok || genDecl.Tok != token.TYPE {
            continue
        }

        for _, spec := range genDecl.Specs {
            typeSpec, ok := spec.(*ast.TypeSpec)
            if !ok {
                continue
            }

            structType, ok := typeSpec.Type.(*ast.StructType)
            if !ok {
                continue
            }

            // 遍历结构体字段
            for _, field := range structType.Fields.List {
                if field.Tag == nil {
                    field.Tag = &ast.BasicLit{
                        Kind:  token.STRING,
                        Value: fmt.Sprintf("`json:\"%s\"`", field.Names[0].Name),
                    }
                }
            }
        }
    }
}
```

---

### **3. 代码重构工具**

#### **场景**

- **变量重命名**：安全地替换变量名（避免误改字符串中的内容）。
- **函数提取**：将重复代码片段提取为独立函数。
- **接口实现检查**：验证结构体是否实现了某个接口。

#### **示例：重命名变量**

```go
func RenameVariable(node ast.Node, oldName, newName string) ast.Node {
    return astutil.Apply(node, func(cursor *astutil.Cursor) bool {
        ident, ok := cursor.Node().(*ast.Ident)
        if ok && ident.Name == oldName {
            ident.Name = newName
        }
        return true
    }, nil)
}
```

---

### **4. 依赖分析与可视化**

#### **场景**

- **包依赖图**：生成项目的包依赖关系图。
- **函数调用链**：分析函数之间的调用关系。

#### **示例：统计函数调用**

```go
type CallGraph map[string][]string

func BuildCallGraph(node *ast.File) CallGraph {
    graph := make(CallGraph)
    currentFunc := ""

    ast.Inspect(node, func(n ast.Node) bool {
        // 记录当前函数名
        if fnDecl, ok := n.(*ast.FuncDecl); ok {
            currentFunc = fnDecl.Name.Name
            return true
        }

        // 记录函数调用
        if callExpr, ok := n.(*ast.CallExpr); ok {
            if ident, ok := callExpr.Fun.(*ast.Ident); ok {
                if currentFunc != "" {
                    graph[currentFunc] = append(graph[currentFunc], ident.Name)
                }
            }
        }
        return true
    })

    return graph
}
```

---

### **5. 实现领域特定语言 (DSL)**

#### **场景**

- **自定义配置解析**：将特定格式的代码转换为配置结构。
- **ORM 查询生成器**：解析类似 SQL 的链式调用生成真实 SQL。

#### **示例：解析路由定义**

```go
// 解析类似以下代码生成路由：
// Route("/user/:id", GetUser)
func ParseRoutes(node *ast.File) map[string]string {
    routes := make(map[string]string)
    ast.Inspect(node, func(n ast.Node) bool {
        callExpr, ok := n.(*ast.CallExpr)
        if !ok {
            return true
        }

        // 检查是否为 Route 函数调用
        if ident, ok := callExpr.Fun.(*ast.Ident); ok && ident.Name == "Route" {
            if len(callExpr.Args) >= 2 {
                path := evalStringLiteral(callExpr.Args[0]) // 解析字符串参数
                handler := evalFuncName(callExpr.Args[1])   // 解析函数名
                routes[path] = handler
            }
        }
        return true
    })
    return routes
}
```

---

### **6. 结合类型检查（go/types）**

#### **场景**

- **验证类型安全**：检查接口实现、类型转换是否合法。
- **自动补全**：为 IDE 提供类型推导支持。

#### **示例：检查接口实现**

```go
func CheckInterfaceImpl(fset *token.FileSet, file *ast.File, ifaceName string) {
    conf := types.Config{Importer: importer.Default()}
    info := &types.Info{
        Defs: make(map[*ast.Ident]types.Object),
        Uses: make(map[*ast.Ident]types.Object),
    }

    // 类型检查
    _, err := conf.Check("pkg", fset, []*ast.File{file}, info)
    if err != nil {
        log.Fatal(err)
    }

    // 遍历结构体，检查是否实现了接口
    for _, decl := range file.Decls {
        if genDecl, ok := decl.(*ast.GenDecl); ok && genDecl.Tok == token.TYPE {
            for _, spec := range genDecl.Specs {
                typeSpec := spec.(*ast.TypeSpec)
                structType, ok := typeSpec.Type.(*ast.StructType)
                if !ok {
                    continue
                }

                // 获取结构体类型
                structObj := info.Defs[typeSpec.Name].(*types.TypeName)
                iface := types.NewInterfaceType(nil, nil).Complete() // 需替换为实际接口
                if types.Implements(structObj.Type(), iface) {
                    fmt.Printf("%s 实现了接口 %s\n", typeSpec.Name.Name, ifaceName)
                }
            }
        }
    }
}
```

---

### **7. 性能优化**

#### **场景**

- **内联优化建议**：识别高频调用的小函数，建议内联。
- **内存分配检查**：检测不必要的堆内存分配（如返回局部变量指针）。

#### **示例：检测返回局部变量指针**

```go
func CheckReturnLocalPointer(node *ast.File) {
    ast.Inspect(node, func(n ast.Node) bool {
        ret, ok := n.(*ast.ReturnStmt)
        if !ok {
            return true
        }

        for _, result := range ret.Results {
            unary, ok := result.(*ast.UnaryExpr)
            if !ok || unary.Op != token.AND {
                continue
            }

            // 检查是否为局部变量地址
            if ident, ok := unary.X.(*ast.Ident); ok {
                fmt.Printf("警告：函数返回局部变量 %s 的指针\n", ident.Name)
            }
        }
        return true
    })
}
```

---

### **关键工具与库**

1. **`go/ast`**：核心 AST 解析库。
2. **`go/parser`**：解析源代码生成 AST。
3. **`go/token`**：处理代码位置信息。
4. **`golang.org/x/tools/go/ast/astutil`**：提供 AST 修改工具。
5. **`golang.org/x/tools/go/loader`**：加载完整的包信息。

---

### **注意事项**

1. **作用域处理**：AST 不包含作用域信息，需结合 `go/types`。
2. **注释处理**：需在 `parser.ParseFile` 时启用 `ParseComments` 标志。
3. **性能问题**：大规模代码库的 AST 遍历可能较慢，需优化遍历逻辑。

通过灵活使用 `ast` 包，开发者可以构建强大的代码分析、生成和重构工具，深入理解代码的静态结构和逻辑。
