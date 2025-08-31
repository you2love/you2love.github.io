
<!-- toc --> 
# docker

## docker-compose.yml

```bash
# 多个services之间自动创建network,并且用web,redis当作别名，加入同个network
# 并且会默认创建volume共享
docker compose up
```

```yml
version: '3'
services:
 web:
   #冒号之后一定要空格，否则提示错误
    build: .
    ports: ["3000:3000"]
 redis:
    image: "redis:7.0-alpine3.17"
```

## dockerfile

```dockerfile
FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
COPY main.py main.py
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]

```

## main.py

```python

from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

# async def app(scope, receive, send):
app = FastAPI()


class Item(BaseModel):
        name: str
        price: float
        is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
        return {"item_id": item_id, "item": item}

import redis

client = redis.Redis(host='redis', port=6379, db=0)

@app.get("/hit")
def hit():
    val = client.incrby('hit')
    return {"hit": val}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=3000)


```

## requirements.txt

```txt
fastapi
redis
uvicorn[standard]
```
