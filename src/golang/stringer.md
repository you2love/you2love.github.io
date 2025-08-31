# stringer
<!-- toc --> 

# 官方自动生成string

* main.go内容

```golang
//go:generate stringer -type=Pill
type Pill int

const (
 Placebo Pill = iota
 Aspirin
 Ibuprofen
 Paracetamol
 Acetaminophen = Paracetamol
)
```

* 执行命令

```sh
go generate
```

* 生成的pill_string.go内容

```golang
import "strconv"

// 这段防止generate之后,修改后没有再次generate,通过编译错误强制提示
func _() {
 // An "invalid array index" compiler error signifies that the constant values have changed.
 // Re-run the stringer command to generate them again.
 var x [1]struct{}
 _ = x[Placebo-0]
 _ = x[Aspirin-1]
 _ = x[Ibuprofen-2]
 _ = x[Paracetamol-3]
}

const _Pill_name = "PlaceboAspirinIbuprofenParacetamol"

var _Pill_index = [...]uint8{0, 7, 14, 23, 34}

func (i Pill) String() string {
 if i < 0 || i >= Pill(len(_Pill_index)-1) {
  return "Pill(" + strconv.FormatInt(int64(i), 10) + ")"
 }
 return _Pill_name[_Pill_index[i]:_Pill_index[i+1]]
}
```
