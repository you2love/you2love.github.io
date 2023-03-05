---
# exgexp包
---

* 正则语法

```golang
// 连续的汉字字母数字
var maxHanDigitAlphaReg = regexp.MustCompile(`[\p{Han}[:digit:][:alpha:]]+`)
// 单个汉字字母数字
var minHanDigitAlphaReg = regexp.MustCompile(`[\p{Han}[:digit:][:alpha:]]+?`)
```
