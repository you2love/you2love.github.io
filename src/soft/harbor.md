# harbor
<!-- toc --> 

### 简介

* [官网](https://goharbor.io/) [github](https://github.com/goharbor/harbor)

* Harbor是VMware公司开源的企业级Docker Registry项目，其目标是帮助用户迅速搭建一个企业级的Docker Registry服务

* Harbor以 Docker 公司开源的Registry 为基础，提供了图形管理UI、基于角色的访问控制(Role Based AccessControl)、AD/LDAP集成、以及审计日志(Auditlogging)等企业用户需求的功能，同时还原生支持中文

* Harbor的每个组件都是以Docker 容器的形式构建的，使用docker-compose 来对它进行部署。用于部署Harbor 的docker- compose模板位于harbor/ docker- compose.yml

* linux至少4核/8G

![harbor组件图](webp/harbor/harbor-1.webp)
![harbor说明](webp/harbor/harbor-2.webp)

```bash
# 下载离线安装包
~/Downloads/harbor-offline-installer-v1.10.11.tgz
```

### 最好在linux机器上

```bash
# mac机器出现
ERROR: for portal  Cannot start service portal: failed to initialize logging driver: dial tcp 127.0.0.1:1514: connect: connection refused
ERROR: Encountered errors while bringing up the project.
```

### docker-compose脚本转发命令

* docker compose自带,不必另外按装.
* harbor需要启动docker-compose相关依赖,所以需要一个转发

```bash
vim docker-compose
#!/bin/bash
docker compose $*
```

### 修改common.sh

```bash
# 注释掉dockercompose检查
function check_dockercompose {
 return
 ....
}
```

### 修改配置

```yml
# The IP address or hostname to access admin UI and registry service.
# DO NOT use localhost or 127.0.0.1, because Harbor needs to be accessed by external clients.
hostname: 修改自定义ip或域名

# 根据自已需求来配置http/https
# http related config
http:
  # port for http, default is 80. If https enabled, this port will redirect to https port
  port: 80

# https related config
#https:
  # https port for harbor, default is 443
#  port: 443
  # The path of cert and key files for nginx
#  certificate: /your/certificate/path
#  private_key: /your/private/key/path
```

### [免费制品管理-nexus]https://www.sonatype.com/products/repository-oss-download