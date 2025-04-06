# ahocorasick,快速在输出文本中查找有没有出现字典中文本

```golang
package main

import (
 "fmt"

 "github.com/cloudflare/ahocorasick"
)

func main() {

 strList := []string{
  "apple", "banana", "cherry"}
 // 构建AC自动机
 ac := ahocorasick.NewStringMatcher(strList)
 // 在文本中查找匹配项
 matches := ac.Match([]byte("I like banana and cherry."))
 for _, match := range matches {
  fmt.Println("找到了：", strList[match])
 }
}
```

```golang
package main

import (
 "fmt"

 "github.com/anknown/ahocorasick"
)

func main() {
 // 构建AC自动机
 dict := [][]rune{
  []rune("apple"),
  []rune("banana"),
  []rune("cherry"),
 }
 content := []rune("your apple text")

 m := new(goahocorasick.Machine)
 if err := m.Build(dict); err != nil {
  fmt.Println(err)
  return
 }

 terms := m.MultiPatternSearch(content, false)
 for _, t := range terms {
  fmt.Printf("%d %s\n", t.Pos, string(t.Word))
 }
}
```
