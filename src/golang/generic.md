---
# 泛型
---

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
