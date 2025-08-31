# vim
<!-- toc --> 

### 常用命令

* ddp-交换上下行-光标在上行，其与下行交换
* :$ 跳转到最后一行
* :1 跳转到第一行

### 查找字符串

* /hello 查找光标处下一个"hellp" ,键入"n" 继续查找下一个,键入"shift+n"(大写N), 向上查找
* ?hello朝找光标处上一个"hellp" 键入"n" 继续查找上一个, 键入"shift+n"(大写N), 向下查找
* /\<printf\> 精确搜索printf："<“表示匹配单词开头，”>“表示匹配单词末尾，需要加转义符"\"

### 复制粘贴

* 复制一行，我们只要把光标移动到想复制的那一行，按yy，就是两次y键，
* 粘贴，把光标移动到你想粘贴的那一行，按p键即可。
* 复制多行，把光标移动到想复制多行的开头，想要向下复制几行，就按nyy，比如我想从这一行开始复制5行，就按5yy

### 插件管理器-vim-plug

* vim-plug 是 vim 下的插件管理器, 可以帮我们统一管理后续的所有插件, 后续的安装插件全部由此工具完成
类似的插件管理工具还有 Vundle, 相较而言 vim-plug 支持异步且效率非常高, 具体选择交由读者自己

* 安装

```bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

* 配置声明

```bash

vim .vimrc

:set term=builtin_ansi
:set encoding=utf-8
:set nocompatible
:set nu
:set hlsearch
:syn on
call plug#begin()
Plug 'preservim/nerdtree'
Plug 'jiangmiao/auto-pairs'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'morhetz/gruvbox'
Plug 'frazrepo/vim-rainbow'
Plug 'chiel92/vim-autoformat'
Plug 'vim-scripts/bash-support.vim'
Plug 'zaach/jsonlint'
Plug 'plasticboy/vim-markdown'
Plug 'ambv/black'
Plug 'fatih/vim-go'
Plug 'sheerun/vim-polyglot'
Plug 'ekalinin/Dockerfile.vim'
call plug#end()
```

* 激活安装-相应插件

```bash
$ vim        #打开vim
:PlugStatus  #查看插件状态
:PlugInstall #安装之前在配置文件中声明的插件
```

* [优秀插件网站](https://vimawesome.com/)(<https://github.com/vim-awesome/vim-awesome>)

```bash
机器上/.vimrc 修改无法显示中文及方向键不能移动光标
 :set term=builtin_ansi
 :set encoding=utf-8
 :set nocompatible
 修改~/.bashrc 打开force_color_prompt=yes
```

* 右键不能复制

```bash
vim set mouse-=a屏蔽了鼠标右健功能.
```
