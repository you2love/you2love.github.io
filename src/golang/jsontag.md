# jsontag
<!-- toc -->

## 源代码

```go
package main

import (
	"flag"
	"fmt"
	"go/ast"
	"go/parser"
	"go/printer"
	"go/token"
	"os"
	"strings"
)

func main() {
	// 解析命令行参数
	input := flag.String("input", "", "Go 源文件路径")
	output := flag.String("output", "", "输出文件路径（可选）")
	flag.Parse()

	if *input == "" {
		fmt.Println("Usage: jsontagger -input file.go [-output file_generated.go]")
		os.Exit(1)
	}

	// 解析 Go 源文件
	fset := token.NewFileSet()
	node, err := parser.ParseFile(fset, *input, nil, parser.ParseComments)
	if err != nil {
		fmt.Printf("Error parsing file: %v\n", err)
		os.Exit(1)
	}

	// 遍历 AST，修改结构体字段
	ast.Inspect(node, func(n ast.Node) bool {
		if structType, ok := n.(*ast.StructType); ok {
			for _, field := range structType.Fields.List {
				if field.Names != nil {
					fieldName := field.Names[0].Name
					// 添加 json 标签（跳过已有标签的字段）
					if field.Tag == nil {
						field.Tag = &ast.BasicLit{
							Kind:  token.STRING,
							Value: fmt.Sprintf("`json:\"%s\"`", strings.ToLower(fieldName)),
						}
					}
				}
			}
		}
		return true
	})

	// 输出结果
	var out *os.File
	if *output != "" {
		out, err = os.Create(*output)
		if err != nil {
			fmt.Printf("Error creating output file: %v\n", err)
			os.Exit(1)
		}
		defer out.Close()
	} else {
		out = os.Stdout
	}

	// 使用 go/format 格式化代码
	if err := printer.Fprint(out, fset, node); err != nil {
		fmt.Printf("Error printing AST: %v\n", err)
		os.Exit(1)
	}
}
```

## 编译安装

```shell
go build -o $GOPATH/bin/jsontagger
```

## 应用(user.go)--生成前

```go
//go:generate jsontagger -input user.go -output user.go
type User struct {
	ID	int	
	Name	string
	Age	int	
}
```

## 应用(user.go)--生成后
```go
//go:generate jsontagger -input main.go -output main.go
type User struct {
	ID	int	`json:"id"`
	Name	string	`json:"name"`
	Age	int	`json:"age"`
}
```