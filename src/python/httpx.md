# httpx示例
<!-- toc --> 

```python
import httpx
r = httpx.get('https://www.baidu.com/')
print(r.headers['content-type'])
print(r.text)
```
