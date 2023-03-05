---
# shell
---


### 编译常用示例

```shell
#! /bin/bash

target=local

set -x #回显执行命令

GOPATH=$(go env GOPATH)
GITVERSION=$(git describe --tags --always)
GITBRANCH=$(git symbolic-ref -q --short HEAD)
DATETIME=$(date "+%Y-%m-%d_%H:%M:%S")
HOSTNAME=$(hostname)

golangci-lint run --timeout=1h

revive -formatter friendly ./...

rm -rf ${target}*

go build -o ${target} -ldflags "-w -s -X main.GitHash=${GITVERSION}-${GITBRANCH} -X main.CompileTime=${DATETIME} -X main.HostName=${HOSTNAME}" .

./${target}
```
