
# jenkins

## 动作

* 重启-直接在地址后面加个 /restart

```bash
https://jenkins.xxx/restart
```

* 退出-直接在地址后面加个/exit

```bash
https://jenkins.xxx/exit
```

* 出现错误

```bash
# 一般是私钥的-----BEGIN OPENSSH PRIVATE KEY-----没有复制全
stderr: Load key "/tmp/jenkins-gitclient-ssh7026290831916999837.key": invalid format 
```

* 复制到远程主机

  * 安装publish-over-ssh插件
