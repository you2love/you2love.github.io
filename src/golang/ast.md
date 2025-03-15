# BNF

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
