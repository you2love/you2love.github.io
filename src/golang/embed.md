# embed

在 Go 语言中，`embed` 是一个用于将静态文件（如文本文件、图片、HTML 模板等）直接嵌入到 Go 二进制文件中的功能。这个功能是通过 Go 1.16 版本引入的 `embed` 包实现的。通过 `embed`，开发者可以将外部资源文件与 Go 代码一起编译，生成一个独立的可执行文件，从而简化部署和分发。

以下是对 Go 语言中 `embed` 功能的详细介绍：

---

### 1. 基本用法

`embed` 功能通过 `//go:embed` 指令来实现。它可以嵌入单个文件、多个文件或整个目录。

#### 1.1 嵌入单个文件

假设我们有一个文本文件 `hello.txt`，内容如下：

```
Hello, World!
```

我们可以通过以下方式将其嵌入到 Go 程序中：

```go
package main

import (
    _ "embed"
    "fmt"
)

//go:embed hello.txt
var s string

func main() {
    fmt.Println(s) // 输出: Hello, World!
}
```

- `//go:embed hello.txt`：表示将 `hello.txt` 文件的内容嵌入到变量 `s` 中。
- `s` 是一个字符串类型的变量，它会包含文件的内容。

#### 1.2 嵌入二进制文件

如果文件是二进制文件（如图片），可以使用 `[]byte` 类型来嵌入：

```go
package main

import (
    _ "embed"
    "fmt"
)

//go:embed logo.png
var logo []byte

func main() {
    fmt.Println("Logo size:", len(logo), "bytes")
}
```

#### 1.3 嵌入多个文件

可以使用切片来嵌入多个文件：

```go
package main

import (
    _ "embed"
    "fmt"
)

//go:embed file1.txt file2.txt
var files []byte

func main() {
    fmt.Println(string(files)) // 输出 file1.txt 和 file2.txt 的内容
}
```

#### 1.4 嵌入整个目录

可以嵌入整个目录及其子目录中的所有文件：

```go
package main

import (
    "embed"
    "fmt"
)

//go:embed static/*
var staticFiles embed.FS

func main() {
    data, _ := staticFiles.ReadFile("static/hello.txt")
    fmt.Println(string(data)) // 输出 static/hello.txt 的内容
}
```

- `embed.FS` 是一个文件系统类型，可以用于访问嵌入的文件。
- `staticFiles.ReadFile("static/hello.txt")` 用于读取嵌入的文件内容。

---

### 2. `embed.FS` 文件系统

`embed.FS` 是一个实现了 `io/fs.FS` 接口的文件系统类型，可以像操作普通文件系统一样操作嵌入的文件。

#### 2.1 遍历嵌入的文件

```go
package main

import (
    "embed"
    "fmt"
    "io/fs"
)

//go:embed static/*
var staticFiles embed.FS

func main() {
    fs.WalkDir(staticFiles, ".", func(path string, d fs.DirEntry, err error) error {
        if err != nil {
            return err
        }
        fmt.Println(path) // 输出嵌入的文件路径
        return nil
    })
}
```

#### 2.2 读取嵌入的文件

```go
package main

import (
    "embed"
    "fmt"
)

//go:embed static/*
var staticFiles embed.FS

func main() {
    data, _ := staticFiles.ReadFile("static/hello.txt")
    fmt.Println(string(data)) // 输出 static/hello.txt 的内容
}
```

---

### 3. 使用场景

`embed` 功能在以下场景中非常有用：

1. **静态资源嵌入**：将 HTML、CSS、JavaScript 等前端资源嵌入到 Go 二进制文件中，方便部署。
2. **配置文件嵌入**：将配置文件嵌入到程序中，避免外部依赖。
3. **模板文件嵌入**：将 HTML 模板或其他模板文件嵌入到程序中。
4. **二进制资源嵌入**：将图片、字体等二进制文件嵌入到程序中。

---

### 4. 注意事项

1. **路径问题**：
   - `//go:embed` 指令中的路径是相对于 Go 源文件的路径。
   - 嵌入目录时，路径必须以 `*` 结尾（如 `static/*`）。

2. **文件修改**：
   - 嵌入的文件在编译时被固定，运行时无法修改。

3. **文件大小**：
   - 嵌入的文件会增加二进制文件的大小，因此不适合嵌入非常大的文件。

4. **安全性**：
   - 嵌入的文件是只读的，无法在运行时修改或删除。

---

### 5. 示例：嵌入 HTML 模板

以下是一个将 HTML 模板嵌入到 Go 程序中的示例：

```go
package main

import (
    "embed"
    "html/template"
    "net/http"
)

//go:embed templates/*
var templates embed.FS

func main() {
    tmpl := template.Must(template.ParseFS(templates, "templates/*.html"))

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        tmpl.ExecuteTemplate(w, "index.html", nil)
    })

    http.ListenAndServe(":8080", nil)
}
```

- `templates/*` 嵌入了一个包含 HTML 模板的目录。
- `template.ParseFS` 用于从嵌入的文件系统中解析模板。

---

### 6. 总结

`embed` 是 Go 语言中一个非常实用的功能，能够将静态文件直接嵌入到 Go 二进制文件中，从而简化部署和分发。通过 `//go:embed` 指令和 `embed.FS` 文件系统，开发者可以轻松地访问和操作嵌入的文件。无论是嵌入配置文件、静态资源还是模板文件，`embed` 都能显著提高开发效率和程序的可移植性。
