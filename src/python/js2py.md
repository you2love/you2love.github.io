# js2py示例
<!-- toc --> 

```python
import js2py

# 超级慢,需要改写成python
js_code = """
function Add(x, y) {
    return x + y;
}
"""

js_add = js2py.eval_js(js_code)

if __name__ == "__main__":
    print(js_add(1, 3))
```
