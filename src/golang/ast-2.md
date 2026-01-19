#### 一、核心概念（基础接口与核心类型）

`go/ast` 包用于表示 Go 源代码的抽象语法树（AST），是静态分析、代码生成的基础。核心概念可分为“基础接口”和“核心节点类型”两类，所有节点均围绕树形结构组织，`File` 为 AST 根节点（代表单个 Go 源文件）。

1. **基础接口（所有节点的根基）**
- **Node**：顶层接口，所有 AST 节点均实现，提供 `Pos()`（起始位置）、`End()`（结束位置）方法，是遍历的基础。
- **Expr**：继承 Node，标识所有表达式节点（如 `a+b`、`fmt.Println()`），无额外方法。
- **Stmt**：继承 Node，标识所有语句节点（如赋值、if、for、return）。
- **Decl**：继承 Node，标识所有声明节点（如 var/const/type 声明、函数声明）。
- **Spec**：继承 Node，标识声明规范节点，是 GenDecl 的 Specs 字段元素类型，核心实现有 ValueSpec（var/const 声明项）、TypeSpec（type 声明项）。
- **ExprStmt**：继承 Stmt，标识表达式语句（即单独作为语句的表达式，如 `fmt.Println()`、`a++`）。

2. **核心节点类型（AST 的核心组成）**
- **AssignStmt**：赋值语句（如 `sum := a + b`）。
- **BinaryExpr**：二元表达式（如 `a + b`）。
- **CallExpr**：函数调用（如 `fmt.Println()`）。
- **ReturnStmt**：return 语句（如 `return sum`）。
- **BlockStmt**：代码块（花括号包裹的语句集合）。
- **UnaryExpr**：一元表达式（如 `!ok`、`a++`、`&x`），关键字段：`Op`（操作符）、`X`（操作数，Expr）。
- **SelExpr**：选择表达式（如 `fmt.Println`），前文已详述。
- **ExprStmt**：表达式语句（如单独一行的 `fmt.Println()`），前文已详述。
- **File**：AST 根节点，代表单个 Go 文件。关键字段：`Name`（包名，Ident 类型）、`Decls`（所有声明）、`Imports`（导入列表）。
- **Ident**：标识符（变量名、函数名、包名等）。关键字段：`Name`（名称字符串）。示例：代码中的 `a`、`add`、`fmt`。
- **BasicLit**：字面量（静态常量值）。关键字段：`Kind`（类型，如 INT/STRING）、`Value`（值字符串）。示例：`10`、`"fmt"`、`true`。
- **GenDecl**：通用声明（var/const/type）。关键字段：`Tok`（声明类型，如 VAR）、`Specs`（具体声明项，[]Spec 类型）。
- **FuncDecl**：函数/方法声明。关键字段：`Name`（函数名）、`Type`（函数签名，FuncType 类型）、`Body`（函数体，BlockStmt 类型）、`Recv`（接收者，方法特有）。
- **FuncType**：函数签名，包含 `Params`（参数列表）、`Results`（返回值列表），均为 FieldList 类型。
- **FieldList**：字段/参数列表，关键字段 `List`（[]*Field），用于函数参数、结构体字段等场景。
- **ValueSpec**：var/const 声明项，实现 Spec 接口。关键字段：`Names`（变量/常量名列表，[]*Ident）、`Type`（类型，可选）、`Values`（初始值列表，[]Expr）。示例：`var x int = 10` 中的 `x` 对应 ValueSpec。
- **TypeSpec**：type 声明项，实现 Spec 接口。关键字段：`Name`（类型名，*Ident）、`Type`（底层类型，Expr）。示例：`type User struct{}` 中的 `User` 对应 TypeSpec。
- **StructType**：结构体类型，实现 Expr 接口。关键字段：`Fields`（结构体字段列表，*FieldList）。示例：`struct{ Name string; Age int }`。
- **InterfaceType**：接口类型，实现 Expr 接口。关键字段：`Methods`（接口方法列表，*FieldList）。示例：`interface{ GetName() string }`。
- **SelectorExpr**：选择表达式，实现 Expr 接口，用于访问结构体/接口成员或包的导出成员。关键字段：`X`（接收者/包名，Expr）、`Sel`（成员名，*Ident）。示例：`fmt.Println`、`u.Name`。
- **IfStmt**：if 语句，实现 Stmt 接口。关键字段：`Cond`（条件表达式，Expr）、`Body`（if 体，*BlockStmt）、`Else`（else 体，Stmt，可选）。示例：`if a > 0 { ... } else { ... }`。
- **ForStmt**：for 语句，实现 Stmt 接口。关键字段：`Init`（初始化语句，Stmt）、`Cond`（条件表达式，Expr）、`Post`（后置语句，Stmt）、`Body`（循环体，*BlockStmt）。支持普通 for（`for i:=0;i<10;i++`）、无限 for（`for{}`）、range for（`for k,v:=range arr`）。
- **RangeStmt**：range 循环语句，实现 Stmt 接口（go/ast 中单独划分，非 ForStmt 子类）。关键字段：`Key`（键变量，Expr）、`Value`（值变量，Expr）、`X`（遍历对象，Expr）、`Body`（循环体，*BlockStmt）。示例：`for k, v := range arr { ... }`。
- **SwitchStmt**：switch 语句，实现 Stmt 接口。关键字段：`Tag`（判断表达式，Expr）、`Body`（switch 体，*BlockStmt）、`CaseList`（case 列表，[]*CaseClause）。
- **CaseClause**：case 子句，实现 Stmt 接口，是 SwitchStmt/TypeSwitchStmt 的 CaseList 字段元素。关键字段：`List`（case 表达式列表，[]Expr）、`Body`（case 体，[]Stmt）。

3. **辅助类型**
- **CommentGroup**：一组注释（关联到节点，如函数注释、包注释）。
- **ImportSpec**：单个导入声明（如 `import "fmt"`）。

#### 二、示例解析（代码 ↔ AST 节点对应）

1. **示例代码（demo.go）**

```go
// 包注释
package main

import "fmt"

// 计算两数之和
func add(a, b int) int {
    sum := a + b
    fmt.Println("sum =", sum)
    return sum
}

func main() {
    result := add(10, 20)
    println(result)
}
```

2. **代码与 AST 节点对应表**

| 代码片段 | 对应 AST 核心类型 | 关键说明 |
| :--- | :--- | :--- |
| `package main` | File + Ident | File.Name 为值为 main 的 Ident |
| `import "fmt"` | ImportSpec | 属于 File.Imports 列表元素 |
| `// 计算两数之和` | CommentGroup | 关联到 FuncDecl.Doc |
| `func add(a, b int) int` | FuncDecl + FuncType + FieldList | FuncType 包含参数 (a,b int) 和返回值 (int)，由 FieldList 描述 |
| `sum := a + b` | AssignStmt + BinaryExpr | 右侧 a+b 是 BinaryExpr（操作符 +） |
| `fmt.Println(...)` | CallExpr + SelectorExpr | fmt.Println 是 SelectorExpr（访问包成员） |
| `10, 20` | BasicLit | Kind 为 INT，Value 为 "10"、"20" |
| `return sum` | ReturnStmt + Ident | 参数为 sum（Ident） |

3. **简单 AST 解析代码（可运行）**

通过 `go/parser` 解析代码为 AST，实现 `ast.Visitor` 遍历节点，输出关键信息：

```go
package main

import (
"fmt"
"go/ast"
"go/parser"
"go/token"
"os"
)

type visitor struct{}

func (v *visitor) Visit(node ast.Node) ast.Visitor {
if node == nil {
return nil
}
switch n := node.(type) {
case *ast.File:
fmt.Printf("[File] 包名: %s\n", n.Name.Name)
case *ast.ImportSpec:
fmt.Printf("[ImportSpec] 导入路径: %s\n", n.Path.Value)
case *ast.FuncDecl:
fmt.Printf("[FuncDecl] 函数名: %s\n", n.Name.Name)
if n.Type.Params != nil {
fmt.Printf("  [参数列表]: ")
for _, f := range n.Type.Params.List {
for _, name := range f.Names {
fmt.Printf("%s ", name.Name)
}
if ident, ok := f.Type.(*ast.Ident); ok {
fmt.Printf("(%s) ", ident.Name)
}
}
fmt.Println()
}
case *ast.AssignStmt:
fmt.Printf("[AssignStmt] 赋值变量: ")
for _, lhs := range n.Lhs {
if ident, ok := lhs.(*ast.Ident); ok {
fmt.Printf("%s ", ident.Name)
}
}
fmt.Println()
case *ast.BinaryExpr:
if x, ok := n.X.(*ast.Ident); ok && y, ok2 := n.Y.(*ast.Ident); ok2 {
fmt.Printf("[BinaryExpr] 表达式: %s %s %s\n", x.Name, n.Op, y.Name)
}
case *ast.BasicLit:
fmt.Printf("[BasicLit] 字面量: %s (类型: %s)\n", n.Value, n.Kind)
case *ast.CallExpr:
if sel, ok := n.Fun.(*ast.SelectorExpr); ok {
pkg := sel.X.(*ast.Ident).Name
method := sel.Sel.Name
fmt.Printf("[CallExpr] 调用: %s.%s()\n", pkg, method)
} else if ident, ok := n.Fun.(*ast.Ident); ok {
fmt.Printf("[CallExpr] 调用: %s()\n", ident.Name)
}
}
return v
}

func main() {
fset := token.NewFileSet()
file, err := parser.ParseFile(fset, "demo.go", nil, parser.AllErrors)
if err != nil {
fmt.Printf("解析错误: %v\n", err)
os.Exit(1)
}
fmt.Println("=== AST 遍历结果 ===")
ast.Walk(&visitor{}, file)
}
```

4. **运行输出（关键片段）**

```text
=== AST 遍历结果 ===
[File] 包名: main
[ImportSpec] 导入路径: "fmt"
[FuncDecl] 函数名: add
  [参数列表]: a b (int) 
[AssignStmt] 赋值变量: sum 
[BinaryExpr] 表达式: a + b
[CallExpr] 调用: fmt.Println()
[FuncDecl] 函数名: main
[AssignStmt] 赋值变量: result 
[BasicLit] 字面量: 10 (类型: INT)
[BasicLit] 字面量: 20 (类型: INT)
[CallExpr] 调用: println()
```

#### 三、核心总结

1. **AST 结构**：以 File 为根，所有代码拆解为 Decl（声明）、Stmt（语句）、Expr（表达式）三级节点。
2. **原子节点**：Ident（标识符）和 BasicLit（字面量）是构成 AST 的最小单元。
3. **核心用法**：通过实现 ast.Visitor 接口的 Visit 方法遍历节点，实现代码分析、生成等功能。