# hugo

## 简介

* Hugo是由Go语言实现的静态网站生成器 [官网](https://gohugo.io)
* 用户编辑内容文件,主题插件提供显示方式,hugo利用两者生成纯静态网站
* Hugo靠shortcode扩展
* 用最新的mermaid.js替换Hugo-theme-learn主题自带的mermaid.js,可获取最新mermaid功能
* config.toml中"home = ["HTML", "RSS", "JSON"]",会产生index.json索引，不要删除

## 本地运行官网

```sh

git clone https://github.com/gohugoio/hugoDocs.git

cd hugoDocs

hugo -D server

```

> 默认访问<http://localhost:1313/>
>
> 出现类似下面报错,hugoDocs中的config.toml增加timeout = 100000000000,单位ms
>
> timeout默认值过短,原因为hugo生成网站时间超出默认配置

```sh

Error building site: ".../hugoDocs/content/en/troubleshooting/faq.md:1:1": timed out initializing value. You may have a circular loop in a shortcode, or your site may have resources that take longer to build than the `timeout` limit in your Hugo config file.

```

## 优秀的主题网站(<https://wowchemy.com/>)

## 替代品-jekyll

* 官网(<http://jekyllcn.com/>)

* 中文官网(<http://jekyllcn.com/>)

* mac自带的ruby,gem安装权限问题-示例[本地运行fyne官网](https://segmentfault.com/a/1190000023872147)

```bash
ERROR:  While executing gem ... (Gem::FilePermissionError)
You don't have write permissions for the /usr/bin directory.
```

* sudo gem install fastlane,采用sudo
* gem install fastlane --user-install, 采用用户级别安装
* sudo gem install -n /usr/local/bin fastlane,同时指时路径
* bundle exec jekyll serve-如果出错

* 常用参数

```bash
# -w 表示监控文件变化及时生成网站
# --incremental 增量构建
# 启动过程会有点慢,需要等待一会儿
jekyll serve -w --port=4001 
```

* github项目中，如果只有__config.yml,没有Gemfile,则可能手动添加,方便本地跑起来

```yml
gem 'github-pages', group: :jekyll_plugins
```

### Ruby Version Manager-RVM (<https://rvm.io/>)

```bash
curl -sSL https://get.rvm.io | bash -s stable
```
