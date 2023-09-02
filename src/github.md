---
# github
---

### 重要提示

* [替代品-gitlab](https://about.gitlab.com/)
* [中文社区-github](https://www.githubs.cn/)
* [ossinsight-](https://ossinsight.io/)
* [api文档-github](https://docs.github.com/)

### 国内境像

* <https://hub.njuu.cf/>
* <https://hub.yzuu.cf/>
* <https://hub.nuaa.cf/>
* <https://kgithub.com/>
* <https://gitclone.com/>

### 解决访问超慢

***

1. [ip address.com](https://www.ipaddress.com/)查域名
![ip address](webp/github/ipaddress.webp)

2. 修改/etc/hosts

   ```sh
   140.82.113.21 collector.Github.com
   140.82.113.5 api.github.com
   140.82.114.4 github.com
   140.82.113.4 github.com
   185.199.108.154 github.githubassets.com
   185.199.109.154 github.githubassets.com
   185.199.110.154 github.githubassets.com
   185.199.111.154 github.githubassets.com
   185.199.110.153 assets-cdn.github.com
   185.199.111.153 assets-cdn.github.com
   185.199.108.153 assets-cdn.github.com
   199.232.69.194 github.global.ssl.fastly.net
   ```

3. 原因是国内dns解析相应域名都是到新加坡,有时候访问不了

4. [FastGithub](https://github.com/dotnetcore/FastGithub)github加速神器

* osx-arm64版本会直接被杀死,改用osx-x86

   ```sh
      [1]    9226 killed     ./fastgithub

      # 丢掉烦人的输出，并且后台运行
      ./fastgithub > /dev/null &
      godoc -http=:6060 &
   ```

* [MacOSx配置](https://github.com/dotnetcore/FastGithub/blob/master/MacOSXConfig.md)

* 最新版firefox替换证书, 证书-查看证书-颁发机构-导入cer证书,否则报错

* 设置系统自动代理为`http://127.0.0.1:38457`，或手动代理http/https为`127.0.0.1:38457`

### pages服务

***

1. User/Organization Pages 个人或公司站点

   1. 创建username.github.io仓库
   2. 仓库设置自定义域名,项目下面会自动增加CNAME文件
   3. 域名解析增加相应的CNAME记录

2. Project Pages 项目站点
   1. gh-pages分支用于构建和发布；
   2. 如果user/org pages使用了独立域名，那么托管在账户下的所有project pages将使用相同的域名进行重定向，除非project pages使用了自己的独立域名；
   如果没有使用独立域名，project pages将通过子路径的形式提供服务<http://username.github.com/projectname>；

### 自定义github主页

 1. 新建一个同名仓库

    > 官方提示：.... is a special repository. Its README.md will appear on your public profile!

 2. 编辑该仓库的 README.md 文件

### 官方工具

* [GitHub Desktop](https://desktop.github.com/)
* [GitHub CLI](https://cli.github.com/)

### 名词

* Sponsor：打赏

* Watch：如有更新，通知提醒。

* Fork：分支一份到你的仓库。

* Code：默认页面，通常会有一个 README.md 文件，用于介绍该项目。

* Pull requests：请求代码合并，如果你想为项目贡献代码，可以在这里提交。

* Actions：工作流。

   >大家知道，持续集成由很多操作组成，比如抓取代码、运行测试、登录远程服务器，发布到第三方服务等等。GitHub 把这些操作就称为 actions。
   >很多操作在不同项目里面是类似的，完全可以共享。GitHub 注意到了这一点，想出了一个很妙的点子，允许开发者把每个操作写成独立的脚本文件，存放到代码仓库，使得其他开发者可以引用。
   >如果你需要某个 action，不必自己写复杂的脚本，直接引用他人写好的 action 即可，整个持续集成过程，就变成了一个 actions 的组合。这就是 GitHub Actions 最特别的地方。
   >GitHub 会监控到，然后分配一台虚拟机先将你的项目 checkout 过去，然后按照你指定的 step 顺序执行定义好的 action

* Projects：项目管理

* Security：安全评估

* Wiki：说明文档

* Insights：数据统计

* codespaces 类似web IDE，省去环境配置环节，云端开发

* 高级搜索 例如包括nginx的pdf书 nginx extension:pdf

### 配套网站-[Netlify](https://app.netlify.com/)

* 用最快的方法构建最快的网站

> 当使用 Github 将网站项目文件夹里的所有东西上传完毕之后，那么就可以打开 Netlify 给予它访问 Github 仓库的权限。
> 当 Netlify 读取完你的网站所属仓库时，会自动识别你所用的静态网页生成器的程序，然后只要点击部署并发布，你的网站就会在 Netlify 被构建并且被发布.

* 能够托管服务，免费 CDN
* 能够绑定自定义域名
* 能够启用免费的TLS证书，启用HTTPS
* 支持自动构建
* 提供 Webhooks 和 API

* [开源有趣项目-介绍](https://hellogithub.com/)

* [github-中文社区](https://www.githubs.cn/)

### 多个帐号，多个ssh

```bash
# ~/.ssh/config配置

Host github3
   HostName github.com
   PreferredAuthentications publickey
   IdentityFile ~/.ssh/id_rsa

Host github2
   HostName github.com
   PreferredAuthentications publickey
   IdentityFile ~/.ssh/id_ecdsa

# 修改远程地址
# git@github.com:xxx/yyy -> git@github3:xxx/yyy
# git@github.com:xxx/yyy -> git@github2:xxx/yyy
```

### git项目在github打不开的时候,采用gitee映像解决

* <https://gitee.com/organizations/mirrors/projects>
* 搜索开源项目
* 修改远程地址, 一般情况下都有的.如果没有,可以自已创建项目同步克隆github代码

### 优秀的github项目

* <https://www.github-zh.com/>
* <https://github.com/GrowingGit/GitHub-Chinese-Top-Charts>
* <https://github.com/ruanyf/weekly>
* <https://github.com/EbookFoundation/free-programming-books>
* <https://github.com/521xueweihan/HelloGitHub/>
* <https://github.com/ljinkai/weekly>
