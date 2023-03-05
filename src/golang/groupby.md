---
# 泛型切片分组
---

```golang
func GroupBy[T any, U comparable](collection []T, iteratee func(T) U) map[U][]T {
 result := map[U][]T{}

 for _, item := range collection {
  key := iteratee(item)

  result[key] = append(result[key], item)
 }

 return result
}
```
