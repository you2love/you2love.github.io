# bnf

在 Go 语言中，虽然没有直接支持 BNF（巴科斯-诺尔范式）的标准库，但有一些第三方库可以帮助你实现基于 BNF 的语法解析和生成式开发。以下是几个常用的 Go 库：

---

### **1. `gocc`**

- **简介**：`gocc` 是一个用于生成词法分析器和语法分析器的工具，支持 BNF 风格的语法定义。
- **特点**：
  - 支持 LALR(1) 语法。
  - 自动生成词法分析器和语法分析器。
  - 生成的代码性能高。
- **使用步骤**：
  1. 定义 BNF 语法文件（`.bnf` 文件）。
  2. 使用 `gocc` 生成解析器代码。
  3. 在 Go 项目中使用生成的解析器。
- **示例**：

  ```bnf
  // calc.bnf
  !whitespace : ' ' | '\t' | '\n' | '\r' ;
  Expression  : Term
              | Expression "+" Term
              | Expression "-" Term ;
  Term        : Factor
              | Term "*" Factor
              | Term "/" Factor ;
  Factor      : NUMBER
              | "(" Expression ")" ;
  NUMBER      : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
  ```

  生成解析器：

  ```bash
  gocc calc.bnf
  ```

---

### **2. `participle`**

- **简介**：`participle` 是一个强大的解析库，支持通过结构体标签定义语法规则。
- **特点**：
  - 无需生成代码，直接使用 Go 结构体定义语法。
  - 支持递归语法和复杂规则。
  - 易于集成到现有项目中。
- **示例**：

  ```go
  package main

  import (
      "fmt"
      "github.com/alecthomas/participle/v2"
  )

  type Expression struct {
      Left  *Term       `parser:"@@"`
      Right []*OpTerm   `parser:"@@*"`
  }

  type OpTerm struct {
      Op    string `parser:"@('+' | '-')"`
      Term  *Term  `parser:"@@"`
  }

  type Term struct {
      Left  *Factor    `parser:"@@"`
      Right []*OpFactor `parser:"@@*"`
  }

  type OpFactor struct {
      Op     string  `parser:"@('*' | '/')"`
      Factor *Factor `parser:"@@"`
  }

  type Factor struct {
      Number *int        `parser:"@Int"`
      Expr   *Expression `parser:"| '(' @@ ')'"`
  }

  func main() {
      parser, err := participle.Build[Expression]()
      if err != nil {
          panic(err)
      }

      expr := &Expression{}
      err = parser.ParseString("", "3 + 5 * (2 - 8)", expr)
      if err != nil {
          panic(err)
      }

      fmt.Printf("%+v\n", expr)
  }
  ```

---

### **3. `go-yacc`**

- **简介**：`go-yacc` 是 Go 语言的一个 Yacc 实现，用于生成 LALR(1) 语法分析器。
- **特点**：
  - 类似于传统的 Yacc/Bison 工具。
  - 支持 BNF 风格的语法定义。
- **示例**：
  1. 定义语法文件（`.y` 文件）。
  2. 使用 `go-yacc` 生成解析器。
  3. 在 Go 项目中使用生成的解析器。

---

### **4. `golang.org/x/tools/cmd/goyacc`**

- **简介**：这是 Go 官方工具链中的 Yacc 实现，用于生成语法分析器。
- **特点**：
  - 与 Go 语言紧密集成。
  - 支持 BNF 风格的语法定义。
- **示例**：
  1. 定义语法文件（`.y` 文件）。
  2. 使用 `goyacc` 生成解析器。
  3. 在 Go 项目中使用生成的解析器。

---

### **5. `peg`**

- **简介**：`peg` 是一个基于 PEG（Parsing Expression Grammar）的解析器生成工具。
- **特点**：
  - 支持 PEG 语法，类似于 BNF。
  - 生成高效的解析器。
- **示例**：
  1. 定义 PEG 语法文件（`.peg` 文件）。
  2. 使用 `peg` 生成解析器。
  3. 在 Go 项目中使用生成的解析器。

---

### **6. `go-ebnf`**

- **简介**：`go-ebnf` 是一个用于解析 EBNF（扩展巴科斯-诺尔范式）的库。
- **特点**：
  - 支持 EBNF 语法。
  - 可以用于解析和验证语法规则。
- **示例**：

  ```go
  package main

  import (
      "fmt"
      "github.com/alecthomas/go-ebnf"
  )

  func main() {
      grammar := `
      Expression  = Term , { ("+" | "-") , Term } ;
      Term        = Factor , { ("*" | "/") , Factor } ;
      Factor      = NUMBER | "(" , Expression , ")" ;
      NUMBER      = ? [0-9]+ ? ;
      `
      ast, err := ebnf.Parse("", []byte(grammar))
      if err != nil {
          panic(err)
      }
      fmt.Printf("%+v\n", ast)
  }
  ```

---

### **总结**

- 如果你需要生成词法分析器和语法分析器，推荐使用 **`gocc`** 或 **`go-yacc`**。
- 如果你希望直接在 Go 代码中定义语法规则，推荐使用 **`participle`**。
- 如果你需要解析 EBNF 语法，可以使用 **`go-ebnf`**。

根据你的需求选择合适的工具，可以高效地实现基于 BNF 的生成式开发。
