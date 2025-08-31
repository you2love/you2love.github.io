# shell
<!-- toc --> 

## man中文手册(<https://github.com/man-pages-zh/manpages-zh>)

```sh
sudo apt update
sudo apt install manpages-zh

dnf update
dnf install man-pages-zh-CN
```

## 升级替换系统命令-[modern-unix)](https://github.com/ibraheemdev/modern-unix)

* bat代替cat, bat 相比 cat 增加了行号和颜色高亮 👍
* duf代替df
* exa代替ls
* dust代替du
* procs代替ps
* difft替代diff
* McFly(<https://github.com/cantino/mcfly>) 执行时间久,会影响启动速度
* zoxide代替cd,可能不用启动z
* tldr替代man, [tldr-github](https://github.com/tldr-pages/tldr) pip install tldr
* ctrl+r 搜索历史命令

### tmux-会话与窗口分离器

```sh
brew install tmux
Tmux 是一个终端复用器（terminal multiplexer），非常有用，属于常用的开发工具。
1.1 会话与进程

命令行的典型使用方式是，打开一个终端窗口（terminal window，以下简称"窗口"），在里面输入命令。用户与计算机的这种临时的交互，称为一次"会话"（session） 。

会话的一个重要特点是，窗口与其中启动的进程是连在一起的。打开窗口，会话开始；关闭窗口，会话结束，会话内部的进程也会随之终止，不管有没有运行完。

为了解决这个问题，会话与窗口可以"解绑"：窗口关闭时，会话并不终止，而是继续运行，等到以后需要的时候，再让会话"绑定"其他窗口。

Tmux 可以将窗口分成多个窗格（pane），每个窗格运行不同的命令。以下命令都是在 Tmux 窗口中执行。

tmux split-window 上下
tmux split-window -h 左右

# 光标切换到上方窗格
$ tmux select-pane -U

# 光标切换到下方窗格
$ tmux select-pane -D

# 光标切换到左边窗格
$ tmux select-pane -L

# 光标切换到右边窗格
$ tmux select-pane -R
```

```bash
# 或者ctrl+r
mcfly search
```

### 并发启动命令

```bash
for var in {0..2}
do
    #用{}把循环体括起来，后加一个&符号，代表每次循环都把命令放入后台运行
    #一旦放入后台，就意味着{}里面的命令交给操作系统的一个线程处理了
    {
        echo ${var}
    }&
done
wait

#wait命令的意思是，等待（wait命令）上面的命令（放入后台的）都执行完毕了再往下执行
```

### 常用源目录

* /etc/yum.repos.d

### systemd新时代linux服务管理软件,就是平时使用(systemctl start stop enable disable status) xxx

* systemd是一个服务管理器,它使管理服务器变得更加容易。
* 对于支持 systemd 的软件，安装的时候，它会自动的在 /usr/lib/systemd/system 目录添加一个配置文件
* /lib -> /usr/lib 通常路径被软链接
![link](webp/shell/link.webp)

### curl带用户名密码的pos提交

```bash
curl -i -X POST \
 http://localhost:4080/api/test/_doc \
 -u user:pwd \
  -H 'Content-Type: application/json' \
  -d '{"name":"中文12344", "value":"https://abc.iste/"}'

curl -X DELETE \
 http://127.0.0.1:4080/api/index/xxx/ \
 -u user:pwd

# 获取本机外网ip
curl ifconfig.me
```

## 查看哪个命令在哪个包中

```bash
# dnf是yum的继承者,更好用
# 查找提供指定内容的软件包
dnf provides '*/chsh'
# 以 Fedora 为基准的安装包如下
dnf install -y util-linux-user
# 搜索一定要加引号
dnf search 'keyword'

# 修改默认的shell
chsh [option] user

# 带调试查看ssh登陆过程,用于卡
ssh -vvv xxxx

# 后来ssh -v 登录查看了下日志，发现一直卡在debug1: SSH2_MSG_KEXINIT sent。直到最后链接失败。
# 网上查了很多，发现是因为mtu设置的数值太大。网络->高级->手动(平时是自动)->指定1500
```

## .ssh/config管理多个ssh密钥

***

1. ~/.ssh/config如果不存在,则创建.

    ```sh
    ...

    # Host可以自定义
    Host github2
        # github.com这个是真实远程服务器,不能修改
        # id_ecdsa.pub内容要在github相应帐户添加为ssh密钥
        HostName github.com
        PreferredAuthentications publickey
        # 指明用哪个文件
        IdentityFile ~/.ssh/id_ecdsa

    ...
    ```

    * Host的定义可以有多组,用指定哪个ssh密钥对应哪个HostName/Host
    * 一般不同域名不同ssh密钥不用配置config,能自动查找对应
2. 测试config

    ```sh

    #github2为config文件中的Host值
    ssh -T git@github2

    # 查看ssh登陆详情
    ssh -vvvT git@github2

    ```

    * 如果github.com的帐户username设置了id_ecdsa.pub
    * 则会回包Hi username! You've successfully authenticated, but GitHub does not provide shell access

3. 修改远程仓库url

    ```sh
    #git@github.com:username/reposname.git==>git@github2:username/reposname.git
    #github2为config文件中的Host值,表明reposname要采用id_ecdsa密钥
    git clone git@github2:username/reposname.git

    ```

4. 本地reposename配置.git/config

   ```sh
   cd reposname
   git config user.name 'username'
   git config user.email 'username@xx.com'
   ```

   * github根据配置文件的user.email来获取github帐号显示author信息

## 在连接远程SSH服务的时候,经常会发生长时间后的断线，或者无响应（无法再键盘输入)

* 客户端定时发送心跳,添加修改本机~/ssh/config

```bash
vim config

# 即每隔30秒，向服务器发出一次心跳
ServerAliveInterval 30
# 若超过100次请求，都没有发送成功，则会主动断开与服务器端的连接。
ServerAliveCountMax 100
```

* 服务器端定时向客户端发送心跳,修改服务器端 ssh配置 /etc/ssh/sshd_config

```bash
vim /etc/ssh/sshd_config
# 表示每隔多少秒，服务器端向客户端发送心跳
ClientAliveInterval 30
# 表示上述多少次心跳无响应之后，会认为Client已经断开
ClientAliveCountMax 6
```

## xargs(命令行参数)和|(标准输入)

***

```sh
#find标准输出为每行一个文件名

#直接通过管道转为grep的标准输入,则grep搜索标准输入包括protobuf的
#输出结果:文件名以.mod结束且包括protobuf
find . -name "*.mod" | grep protobuf

#管道转为xargs的标准输入,
#xargs把标准输入转化为grep的参数
#grep指定的文件名里内容包括protobuf的
#输出结果:文件名以.mod结束且文件内容包括protobuf
find . -name "*.mod" | xargs grep protobuf

# 搜索名字叫html目录
find . -type d -name 'html'
```

* 管道(|)的作用是将前面命令的标准输出作为后面命令的标准输入
* xargs将标准输入转成各种格式化的参数

## 常用命令

***

```sh

set -v 回显命令，但不替换变量值
set -x 回显命名，替换变量值

# 用双引号处理带空格的文件
cp "带空格的文件" newfile

ls -l | grep "^-" | wc -l 当前目录下文件总数

# linux网络共享网盘nfs，/etc/exports文件增加一个共享目录

#产生ssh密钥对,注意-C大写,保存id_rsa文件名,ssh会默认读取,否则就要明确指出
#-b：指定密钥长度；-C：添加注释；-f：指定用来保存密钥的文件名；-t：指定要创建的密钥类型。
#现在很多地方都不支持rsa,建议采用ed25519/ecdsa
# -t [dsa | ecdsa | ecdsa-sk | ed25519 | ed25519-sk | rsa]
ssh-keygen -t rsa -C "xxx@aliyun.com" -f id_rsa
# 注意-t之后的空格,有可能提示不识别参数
ssh-keygen -t ed25519 -C "xxx@aliyun.com" -f id_ed25519

# 显示正在使用的shell
echo $SHELL

# 快速切换目录, vim .bashrc/.zshrc source .bashrc/.zshrc
export $CDPATH=.:~:/xxx/

#获取历史命令
#zsh
cat  $HOME/.zsh_history
#bsh
cat  $HOME/.bash_history

# 查看磁盘占用情况
df -h
#查看当前一级目录文件大小
du -h --max-depth=1

# 清空./var/journalctl日志
journalctl --vacuum-size=10M

# ls人性化阅读
ls -lh

# 复制到粘贴板
#windows
clip < ~/.ssh/id_ed25519.pub
#mac
pbcopy < ~/.ssh/id_ed25519.pub
#linux
xclip -sel clip < ~/.ssh/id_ed25519.pub

# 获取脚本所在目录
dirname $0
cd `dirname $0`
pwd

# 获取home目录
echo $HOME


# 当前时间、系统已经运行了多长时间、目前有多少登陆用户、系统在过去的1分钟、5分钟和15分钟内的平均负载。
uptime

# 解决ssh超级慢(去除服务端利用dns反查客户端)
vi /etc/ssh/sshd_config
UseDNS no
GSSAPIAuthentication no

# 列出所有监听tcp端口程序
netstat -ltpn
#查看所有服务监听端口
netstat -a

# 监听tcp指定端口
tcpdump tcp port xxx

#查看网卡流量:每1秒 显示 1次 显示 10次
sar -n DEV 1 10

# 查看命令执行情况
set -V

#防火墙:
#查看是否打开端口:
firewall-cmd --list-all
#添加端口:
firewall-cmd --permanent --add-port=3000/tcp
#批量增加端口:
firewall-cmd --permanent --zone=public --add-port=7000-8000/tcp
#移除端口:
firewall-cmd --permanent --remove-port=7780/tcp
#重新加载规则生效
firewall-cmd --reload

#查找前20名占用内存较大:
ps aux | head -1;ps aux |grep -v PID |sort -rn -k +4 | head -20

# 建立软连接
ln -s 真实存在目录 软链接
```

## 积累

```sh
# 使用-j参数 不处理压缩文件中原来目录路径
zip -qj file.zip /xxx/xx/xx

# Parallel
https://linux.cn/article-9718-1.html  使用 GNU Parallel 提高 Linux 命令行执行效率
```

## 示例脚本

***

* linux 普通用户实现sudo免密

```bash
vim /etc/sudoers.d
增加一个文件，添加以下内容
username ALL=(ALL) NOPASSWD:ALL
```

* 利用git部署更新脚本

```bash
#!/usr/bin/env bash

cd ${gitdir}
# 批量杀死监控进程 shell脚本或专用管理程序
ps -ef|grep xxx | grep -v grep | awk '{print $2}' | xargs kill -9
# 批量杀死目标进程
ps -ef|grep yyy | grep -v grep | awk '{print $2}' | xargs kill -9
# 拉取最新程序
git pull
# 跑起监控进程
nohup ./xxx.sh >/dev/null 2>&1 &
```

* 监控脚本

```bash
#!/usr/bin/env bash

while true
do
   # 查看目标进程还在不在
   procnum=` ps -ef|grep "yyy$"|grep -v grep|wc -l`
   if [ $procnum -eq 0 ]; then
     cd ${basedir}
     nohup ./yyy >/dev/null 2>&1 &
   fi

   # 延时30秒
   sleep 30
done
```

* 编译脚本

```bash
#!/usr/bin/env bash
# 批量杀死目标进程
ps -ef|grep yyy | grep -v grep | awk '{print $2}' | xargs kill -9
hash=`git rev-parse --short HEAD`
rc=`date "+%Y-%m-%d_%H:%M:%S"`
target=yyy
go build -ldflags "-s -w -X main.GitHash=${hash} -X main.CompileTime=${rc}" -tags=jsoniter -o ${target} ${target}.go
chmod a+x ${target}
rundir=${target}_run
rm -rf ${rundir}
mkdir ${rundir}
mv ${target} ${rundir}
cp -r conf ${rundir}/
nohup ./${target} >/dev/null 2>&1 &
exit
```

* 设置北京时间

```bash
sudo timedatectl set-timezone Asia/Shanghai
```

### 常见包管理

* apt = apt-get、apt-cache 和 apt-config 中最常用命令选项的集合。
* dnf 是 yum的升级版

### 显卡

```bash
sudo lshw -numeric -C display显示显卡信息，lspci | grep -i vga
```

![vga](webp/shell/vga.webp)

### 权限错误

```bash
# Permissions 0644 for '/root/.ssh/id_ecdsa' are too open
# 降低权限
chmod 0600 ~/.ssh/id_ecdsa
```

### mlocate-更快的find

> 这个命令的原理是，先为文件系统创建索引数据库，mlocate只是搜索索引，所以速度快
对于新增文件应该先updatedb更新数据库，否则就搜不到，当然更新索引时，执行updatedb还是比较快的
mlocate在很多系统中和locate同名

```bash

#创建索引 扫描整个系统，为整个系统创建索引，数据库在/var/lib/mlocate/mlocate.db
sudo updatedb

mlocate  abc.txt

mlocate  -ie  abc.txt   如果 abc.txt已经删除了，使用-e会检查文件是否真实存在，而不必updatedb；-i，忽略大小写

mlocate  /etc/*profile   在/etc中查找类似profile的文件
```

### 古老的netrc,windows是_netrc文件

> .netrc文件是unix系统中古老的文件，该.netrc文件格式于 1978 年发明并首次用于Berknet，此后一直被各种工具和库使用。顺便说一句，这就是英特尔推出 8086 的同一年，而 DNS 还不存在。几十年来，ftp、curl（从 1998 年夏天开始）、wget、fetchmail 和大量其他工具和网络库一直支持 .netrc。在许多情况下，它是向远程系统提供凭据的唯一跨工具方式。

### Delta RPM

> Delta RPM软件包包含RPM软件包的新旧版本之间的差异。在旧的RPM上应用增量RPM会得到完整的新RPM。不必拥有旧RPM的副本，

### startship.rs值得一用
