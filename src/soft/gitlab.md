# gitlab
<!-- toc --> 


### 安装私有部署(内存最低2GB,机器配置越高越好,否则会有各种问题)

```bash
# 下载安装docker
curl -fsSL <https://get.docker.com> | bash -s docker --mirror Aliyun

# 启动docker
systemctl start docker

# 创建gitlab home
mkdir /srv/gitlab
# 导出环境变量 vim .bash_profile
export GITLAB_HOME=/srv/gitlab

# docker跑起来,采用社区版,自带常见服务足够了
docker run --detach \
  --hostname gitlab.example.com \
  --publish 443:443 --publish 80:80 --publish 8090:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  --shm-size 256m \
  registry.gitlab.cn/omnibus/gitlab-jh:latest

# 初始化过程可能需要很长时间。 您可以通过以下方式跟踪此过程,查看日志
docker logs -f gitlab

# 获取默认初始化密码,用户名是root
docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
```

[官方安装说明](https://docs.gitlab.cn/jh/install/docker.html)

```bash
# 安装sourcegraph
docker run --detach \
    --publish 8091:7080 \
    --publish 127.0.0.1:3370:3370 \
    --rm --volume ~/.sourcegraph/config:/etc/sourcegraph \
    --volume ~/.sourcegraph/data:/var/opt/sourcegraph sourcegraph/server:3.40.0
```
