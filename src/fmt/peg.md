# PEG
<!-- toc --> 

# PEG 解析示例

下面为你提供一些 PEG（解析表达式文法）规范的具体实例，帮助你理解其语法和应用场景。

### 一、简单算术表达式解析

这个例子展示了如何用 PEG 解析包含加减乘除和括号的算术表达式，同时处理运算符优先级。



```
# 算术表达式语法

Expression  <- Term (AddOp Term)\*

Term        <- Factor (MulOp Factor)\*

Factor      <- Number / '(' Expression ')'

Number      <- \[0-9]+ / '-' \[0-9]+

AddOp       <- '+' / '-'

MulOp       <- '\*' / '/'
```

**解释**：



*   `Expression` 由 `Term` 后跟零个或多个 `AddOp Term` 组成（加法 / 减法）。

*   `Term` 由 `Factor` 后跟零个或多个 `MulOp Factor` 组成（乘法 / 除法）。

*   `Factor` 可以是数字或括号内的表达式。

*   `Number` 支持整数和负数（如 `123` 或 `-456`）。

*   **优先级**：通过规则嵌套实现（`MulOp` 在 `Term` 中，比 `AddOp` 优先级高）。

### 二、JSON 格式解析（简化版）

PEG 非常适合解析 JSON 这种无歧义的数据格式。



```
JSONValue   <- JSONObject / JSONArray / JSONString / JSONNumber / "true" / "false" / "null"

JSONObject  <- '{' (JSONPair (',' JSONPair)\*)? '}'

JSONPair    <- JSONString ':' JSONValue

JSONArray   <- '\[' (JSONValue (',' JSONValue)\*)? ']'

JSONString  <- '"' \[^"]\* '"'

JSONNumber  <- \[0-9]+ ('.' \[0-9]+)? (\[eE] \[+-]? \[0-9]+)?
```

**解释**：



*   `JSONValue` 可以是对象、数组、字符串、数字或字面量（`true`/`false`/`null`）。

*   `JSONObject` 是键值对的集合，用逗号分隔。

*   `JSONArray` 是值的有序列表，用逗号分隔。

*   `JSONString` 是双引号包裹的任意字符（简化版，实际需处理转义）。

*   `JSONNumber` 支持整数、小数和科学计数法（如 `123`、`3.14`、`1e-10`）。

### 三、CSV 格式解析

CSV（逗号分隔值）是一种简单的表格数据格式。

```
CSVFile     <- Row ('\n' Row)\*

Row         <- Value (',' Value)\* '\n'?

Value       <- QuotedValue / UnquotedValue

QuotedValue <- '"' ('""' / \[^"])\* '"'

UnquotedValue <- \[^",\n]\*
```

**解释**：

*   `CSVFile` 由多行 `Row` 组成，行之间用换行符分隔。

*   `Row` 由多个 `Value` 组成，用逗号分隔，行末可选换行符。

*   `Value` 可以是带引号的值或不带引号的值。

*   `QuotedValue` 支持双引号转义（如 `"a""b"` 表示 `a"b`）。

### 四、标识符和关键字解析

这个例子展示了如何区分关键字和普通标识符，避免匹配冲突。

```
Identifier  <- !Keyword \[a-zA-Z\_] \[a-zA-Z0-9\_]\*

Keyword     <- "if" / "else" / "while" / "function"
```

**解释**：



*   `!Keyword` 是负向断言，确保当前位置不会匹配关键字。

*   例如，`if` 会匹配 `Keyword`，而 `if_else` 会匹配 `Identifier`。

### 五、HTML 标签解析（简化版）

解析 HTML 标签结构，处理嵌套关系。

```
HTML        <- Element\*

Element     <- OpenTag Content CloseTag

OpenTag     <- '<' TagName Attribute\* '>'

CloseTag    <- '\</' TagName '>'

TagName     <- \[a-zA-Z]+

Attribute   <- ' ' AttrName '=' '"' AttrValue '"'

AttrName    <- \[a-zA-Z]+

AttrValue   <- \[^"]\*

Content     <- Text / Element

Text        <- \[^<]\*
```

**解释**：

*   `Element` 由开始标签、内容和结束标签组成。

*   `Attribute` 是键值对（如 `id="main"`）。

*   `Content` 可以是文本或嵌套的元素。

*   **注意**：这是简化版，实际 HTML 解析需处理自闭合标签（如 `<br>`）和更多复杂情况。

### 六、使用正向断言和负向断言

PEG 的断言运算符 `&` 和 `!` 允许在不消耗输入的情况下检查匹配。

```
// 匹配以 "http" 开头的 URL

URL         <- &"http" "http" ("s" / "") "://" Domain Path?

// 匹配非空行（至少包含一个非空白字符）

NonEmptyLine <- !'\n' \[^\n]\* '\n'

// 匹配非零数字

NonZeroDigit <- !'0' \[0-9]
```

**解释**：

*   `&"http"` 确保后续字符是 `http`，但不消耗输入。

*   `!'0'` 排除 `0`，只允许 `1-9`。

### 七、PEG.js 中的实际应用

如果你使用 JavaScript 的 PEG.js 库，可以这样定义语法：



```
// PEG.js 语法文件示例

start = expression

expression

&#x20; \= additive

additive

&#x20; \= left:multiplicative "+" right:additive { return left + right; }

&#x20; / multiplicative

multiplicative

&#x20; \= left:primary "\*" right:multiplicative { return left \* right; }

&#x20; / primary

primary

&#x20; \= integer

&#x20; / "(" expr:expression ")" { return expr; }

integer "integer"

&#x20; \= digits:\[0-9]+ { return parseInt(digits.join(""), 10); }
```

**解释**：



*   这是一个可执行的 PEG 语法，包含动作代码（大括号内的 JavaScript）。

*   解析时会自动生成抽象语法树（AST）节点。

### 总结

PEG 的核心优势在于：



1.  **无歧义性**：规则顺序决定匹配优先级，无需额外优先级规则。

2.  **高效解析**：无回溯，适合处理复杂语法。

3.  **灵活断言**：通过 `&` 和 `!` 实现预检查，不消耗输入。

以上实例覆盖了常见场景，你可以根据需要调整规则或添加新的运算符 / 结构。
