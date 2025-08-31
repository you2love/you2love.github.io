# requests示例
<!-- toc --> 

```python
#!python3
# -*- coding:utf8 -*-

# pip3 install requests

import requests

r = requests.get("https://www.baidu.com/")

print(r.headers)
print(r.text)
```
