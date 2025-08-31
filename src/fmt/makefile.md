# makefile

## 常见编译变量参数

```bash
SHELL := /usr/bin/env bash -o pipefail

GIT_VERSION ?= $(shell git describe --always --tags --match 'v*' --dirty)
COMMIT     ?= $(shell git rev-parse HEAD)
BRANCH     ?= $(shell git rev-parse --abbrev-ref HEAD)
BUILD_DATE ?= $(shell date +%s)
BUILD_HOST ?= $(shell hostname)
BUILD_USER ?= $(shell id -un)
```

## 变量不同赋值区别

```bash
= 是最基本的赋值
:= 是覆盖之前的值
?= 是如果没有被赋值过就赋予等号后面的值
+= 是添加等号后面的值
```

## 生成makefile的cmakelist介绍

![cmakelist](/webp/makefile/cmakelist.webp)

## makelist介绍

![intro](/webp/makefile/intro.webp)
