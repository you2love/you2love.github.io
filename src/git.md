---
# git
---

### 优秀文档

* [git-scm]<https://git-scm.com/book/zh/>)

### 文件状态变迁图

```mermaid

flowchart LR
    subgraph WorkDirectory
        ut(Untracked)
        um(Unmodified)--编辑修改-->md(Modified)
    end
    subgraph Staged
        s(Staged/Index)
    end
    subgraph Repo
        r(Commit对象)
    end
WorkDirectory --add--> Staged
Staged --restore或checkout--> WorkDirectory

Staged --commit--> Repo
Repo --restore或reset或checkout--> Staged

```

![git_lint](webp/git/git_lint.webp)

```mermaid
sequenceDiagram
    actor ut as Untracked
    actor um as Unmodified
    actor m as Modified
    actor s as Staged/Index
    actor r as Repo

    opt 未跟踪新文件
      ut->>s: add 跟踪
      ut-->>um: 自动转为
      r-->>s: 放弃跟踪 restore --staged或rm --cached
      um-->>ut: 放弃跟踪后自动转为
    end

    opt 已跟踪
      opt 已跟踪编辑
        um->>m: 编辑
        s-->>um: 放弃编辑 restore或checkout
      end

      opt 提交到stage/index
        m->>s: add
        r-->>s: 放弃add restore --staged或reset
      end
      r-->>um: 放弃add和编辑 restore --staged --worktree或checkout head
    end
    
    opt 提交repo
      s->>r: commit
      r-->>s: 放弃commit restore --source=HEAD~1 --staged或reset head~1
    end
    r-->>um: 放弃commit和add和编辑 restore --source=HEAD~1 --staged --worktree或checkout head~1或reset --hard head~1

```

### 命令介绍

* git rm, 删除WorkDictory,Staged/Index的文件
  * 命令快照

  ```bash
  git rm [--cached] <pathspec>...
  ```

  * 带上--cached，则只删除Staged/Index,否则WorkDictory也删除

* restore,从指定源恢复
  * 命令快照

  ```sh
   git restore [<options>] [--source=<tree>] [--staged] [--worktree] [--] <pathspec>...
  ```

  * 没有带上--staged,则直接从Staged/Index恢复到WorkDictory
  * 带上--staged,则从repo(head或者source指定commit或tag)恢复到Staged/Index.如果同时要恢复WorkDictory,则带上--worktree
  * --source默认值为head
  * 命令是试验性的,行为可能会改变.THIS COMMAND IS EXPERIMENTAL. THE BEHAVIOR MAY CHANGE.

* reset,设置head,Reset current HEAD to the specified state
  * 命令快照-格式1

  ```sh
   git reset [-q] [<tree-ish>] [--] <pathspec>
  ```

  * 从指定的tree-ish恢复到staged/index,tree-ish不指定就采用head

  * 命令快照-格式2

  ```sh
   git reset [<mode>] [<commit>]
           This form resets the current branch head to <commit> and possibly updates the index (resetting it to the tree of <commit>) and the working tree depending on <mode>. If
           <mode> is omitted, defaults to --mixed. The <mode> must be one of the following:
  ```

  * 把head指向tree-ish
  * mode不同值不同含义
    * --soft,仅改动head
    * --mixed(默认值),改动head并且staged/index恢复为指定tree-ish里面,workdictory不改
    * --herd,改动head并且staged/index,workdictory恢复为指定tree-ish里面
  
* checkout,切换分支或恢复出指定文件
  * 命令快照-格式1

  ```sh
  git checkout [-f|--ours|--theirs|-m|--conflict=<style>] [<tree-ish>] [--] <pathspec>
  ```

  * 没有带上tree-ish,则直接从Staged/Index恢复到WorkDictory
  * 带上tree-ish,则从repo(tree-ish)恢复到Staged/Index和WorkDictory
  * tree-ish 通常是head,commit值或tag之类

  * 命令快照-格式2

  ```sh
  git checkout [-q] [-f] [-m] [[-b|-B|--orphan] <new_branch>]
  ```

  * 没有带上-b,则直接切换指定分支,分支必须存在
  * 带上-b,则创建新分支,并且立即切换过去

  * 命令快照-格式3

  ```sh
  #从远程仓库/分支,创建本地分支,分支名同远程分支一样,两者建立跟踪关系
  #切换到新分支,简化操作
  git checkout --track remoteRepo/repoBranch
  ```

* revert返祖,产生新的提交commit来返回过去的特定提交
  * 命令快照

  ```sh
   git revert [--[no-]edit] [-n] [-m parent-number] [-s] [-S[<keyid>]] <commit>
   git rever -m 1 head
  ```

```mermaid

flowchart LR
m1(commitXXXX) --commit--> m2(commitYYYY)
m2 --commit--> m3(commitZZZZ)
m3 --rever -m 1 head--> m4(commitNNNN,但内容和commitYYYY一样)

```

* 标签

  ```sh
  #列出标签
  git tag
  #查看指定标签
  git show vxxx
  #打轻量标签
  git tag v1.0
  #打附注标签
  git tag -a v2.0 -m "附加信息"
  #把标签vxxx推送到远程
  git push origin vxxx
  ```

* commit对象

```mermaid

flowchart LR
    subgraph commitXXXX
        direction TB
        cx(CommitXXXX)--包含-->tx(Tree对象)
        tx--包含-->bxa(Blob对象A)
        tx--包含-->bxb(Blob对象b)
        tx--包含-->bxc(Blob对象c)
    end
    subgraph commitYYYY
        direction TB
        cy(commitYYYY)--包含-->ty(Tree对象)
        ty--包含-->by1(Blob对象1)
        ty--包含-->by2(Blob对象2)
    end
    subgraph commitZZZZ
        direction TB
        cz(commitZZZZ)--包含-->tz(Tree对象)
        tz--包含-->bzl(Blob对象l)
        tz--包含-->bzm(Blob对象m)
        tz--包含-->bzn(Blob对象n)
        tz--包含-->bzo(Blob对象o)
    end
commitXXXX --父对象--> commitYYYY
commitYYYY --父对象--> commitZZZZ

```

* 分支

```bash
#列出分支
git branch
#查看分支详情
git branch -vv
#创建分支issue100
git branch issue100
#跳到分支issue100
git checkout issue100
#创建hotfix并且立即切过去
git checkout -b hotfix
#删除分支issue100
git branch -d issue100
#指定分支的跟踪远程分支
git branch --set-upstream-to=remote/branch branch
#基于远程分支创建新分支并设置跟踪关系
git checkout --trace -b feature origin/feature
#把hotfix分支合并到当前分支里
git merge hotfix
# 合并没有历史交并的分支
git merge gitee master --allow-unrelated-histories
#如果合并冲突,则编辑修改冲突文件,再提交
git commit -am "人工修改冲突"
#变基是改变-指定分支(不指出则采用当前分支)的起点,并且起点后的提交重播一次
#以hotfix分支为起点,本分支已有提交重播一次,达到合并目的
git rebase hotfix
#如果重播冲突,则编辑修改冲突文件,再提交
git commit -am "人工修改冲突"
#解决冲突后提交,再继续完成变基操作
git rebase --continue
```

![git_rebase](webp/git/git_rebase.webp)

* rebase变基原则
  * 只对尚未推送或分享给别人的本地修改执行变基操作清理历史.
  * 从不对已推送至别处的提交执行变基操作.

* 合并提交

```bash
git commit -am "first"
# 编辑修改...
git commit -am "second"
# 编辑修改...
git commit -am "three"
# 交互式合并最近三个提交,如下图所示
# 默认从上到下，从旧到新列出来,可以编辑顺序
# 合并时从上到下执行，第一个一般是pack(基础)，其他的为s(合并到基础去,pack改为s)
# 退出保存后,会继续编辑合并信息.
git rebase -i head~3
```

![git_rebase](webp/git/git_rebase_head.webp)

```bash
git commit
git branch dev
git checkout dev
git commit
git commit
git checkout master
git commit
git commit
git commit
git merge dev
```

```mermaid
gitGraph
  commit
  branch dev
  checkout dev
  commit
  commit
  # 默认master不存在,现在都采用main
  checkout main
  commit
  commit
  commit
  merge dev
```

* 远程仓库

```mermaid

flowchart LR
    subgraph 本地仓库前
      lm(master)
      ld(dev)
    end
    subgraph 远程仓库
      rm(master)
      rd(dev)
      rh(hotfix)
    end
    subgraph 本地仓库后
      am(master)
      ad(dev)

      arm(origin/master)
      ard(origin/dev)
      arh(origin/hotfix)
    end
本地仓库前 --remote add orgin--> 远程仓库
本地仓库前 --fetch origin--> 本地仓库后

```

```sh
#添加远程库
git remote add name url
# 如果远程库有意外提交,可以强行合并进来,再推上去
git pull origin master --allow-unrelated-histories
#拉取远程库内容
git fetch name
#查看远程分支日志
git log name/branch
#创建本地分支branch并且跟踪到远程分支
git checkout --track name/branch
#推送到远程
git push
#删除远程分支
git push name -d branch
#查看本地分支与远程分支设置
git branch -vv
```

* 集中式工作流程

```mermaid
sequenceDiagram
    actor da as 开发者A
    actor r as 仓库
    actor db as 开发者B

    da->>r: clone

    db->>r: clone

    da->>da: commit

    db->>db: commit

    da->>r: push

    db->>r: pull

    db->>r: push

```

* pull-request工作流程,同一个仓库用不同分支替代仓库,类似流程

```mermaid
sequenceDiagram
    actor da as 开发者A
    actor dar as 开发者A仓库
    actor r as 仓库
    actor rw as 仓库维护者
    actor db as 开发者B
    actor dbr as 开发者B仓库

    opt 开发者A流程
      da->>r: fork
      r-->>dar: 自动创建
      da->>dar: clone
      da->>da: commit
      da-->>dar: push
      dar-->>r: pull requestA
      dar-->>rw: 通知
    end

    opt 开发者B流程
      db->>r: fork
      r-->>dbr: 自动创建
      db->>dbr: clone
      db->>db: commit
      db-->>dbr: push
      dbr-->>r: pull requestB
      dbr-->>rw: 通知
    end

    opt 仓库维护者流程
      rw->>r: merge pull requestA
      rw->>r: merge pull requestB
    end

```

* 储存栈

```sh
#把workdirectory已跟踪修改+staged/index储存到一个栈上,
git stash
#可以在任何一个干净状态恢复出来,不一定需要原来保存的分支里
#不带上--index,则只恢复workdirectory已跟踪修改,
#带上--index,则staged/index也一起恢复
git stash apply [--index]
#apply可以多次重复
#删除就用drop
git stash drop
```

* 杂项

```sh
#配置本项目用户
git config user.name 'username'
git config user.email 'username@xx.com'

# 配置默认的分支名称
git config --global init.defaultBranch master   

#修改最近提交的author
#amend纠正最近一次提交
#此次也会提交stage/index内容,如果stage/index没有修改,则直修改提交信息
git commit --amend --reset-author

# 查看最近3次提交文件变化情况
git log -3 --stat

#查看指定文件提交记录
git log -p filename
# 查看该文件的相关commit
git log -- filename

# 查看指定提交特定文件的变化
git show commit_id filename
# 查看指定提交的变化
git show commit_id

#比较两次提交之间指定目录的区别
git diff 26be34b 934d76fd flow/proto_file

# 有时候git status显示有变化,但是git diff没有,可能是文件换行符及文件权限属性变化了
git diff --cached filename

#当前指定提交commit值
rem 'git rev-parse --short HEAD'

#记录本项目git版本,获取当前git版本值
Cgithash=`git rev-parse --short HEAD`
#获取当前时间
Ctime=`date '+%Y-%m-%d_%H:%M:%S'`

# 强制退回指定commit
#fa2850...是commit的hash值
git reset --hard fa285014d635190e74cd40fc798ce26243766a09

#带用户名及密码的git clone
git clone http://uer:pwd@xxx.git


# 本地修改不提交到远程仓库
git update-index --skip-worktree filePath

# post-receive钩子
# git pull引入$GIT_DIR变量,因此需要取消变量
unset $(git rev-parse --local-env-vars);
git pull


# 查看特定提交在哪里分支
git branch --contains xxxx -all

# 创建一个空分支,没有任何父节点
git checkout --orphan newBranch
git rm -rf .
# 如何没有任何文件提交，看不到新建的分支
git commit -am "newBranch"
```

### 积累

***

* **[官网](https://git-scm.com/)**

* Git gc一般情况不用手动,gc主要把无用的内部对象回收,一般都自动处理

* Git钩子都被存储在 Git 目录下的 hooks 子目录中.

* .git目录内容
![git_dir](webp/git/git_dir.webp)

* git引用
![git_refs](webp/git/git_refs.webp)

* 查看项目本地仓库,远程仓库,标签等

```sh
  tree .git/refs
```

![git_tree_refs](webp/git/git_tree_refs.webp)

* Git 可以使用四种不同的协议来传输资料：
  * 本地协议（Local）

  ```sh
  #本机clone,尽量采用不带file://前缀,加快速度
  git clone /srv/git/project.git
  git clone file:///srv/git/project.git
  ```

  * HTTP 协议，现在git一般采用智能 HTTP 协议

  ```sh
  git clone https://example.com/gitproject.git
  ```

  * SSH（Secure Shell）协议

  ```sh
  git clone ssh://[user@]server/project.git
  git clone [user@]server:project.git
  ```

  * Git 协议
    * Git里的一个特殊的守护进程,它监听在一个特定的端口（9418）
    * 速度最快的
    * 缺乏授权机制
    * git://

* 利用post-receive钩子自动更新

```sh
  #!/usr/bin/env bash

  # post-receive脚本代码
  cd ~
  target=xxx
  # 简单粗暴,删除旧目录
  if [ -d ${target} ]; then
      rm -rf ${target}
  fi
  # 重新建立,从git代码库目录
  git clone gogs-repositories/yyy/${target}.git
  # 杀死进程
  pkill ${target}
  cd ${target}
  # 后台运行进程
  nohup ./${target} >${target}.nohup 2>&1 &
```

* push碰到HTTP 413
  * 问题表现

  ```sh
  Git push error: error: RPC failed; HTTP 413 curl 22 the requested URL returned error: 413
  ```

  * 解决办法

  ```sh
  # 增加最大http长度
  git config –global http.postBuffer 524288000
  ```

  ```nginx
  location / {
    ...
    # 如果有nginx转发
    client_max_body_size 200M;
    ...
  }
  ```

### 多项目-一个项目(采用git管理)使用另一个项目(采用git管理)

***

* Git Submodule

  * 添加子目录

    ```sh
    # 默认在目录下建立repo子目录,并且克隆仓库,并且创建.gitmodules
    git submodule add  https://xxx/repo.git
    # 提交到仓库
    git commit -am "submodule"

    # 如果子项目有更新,直接取更新
    git submodule update --remote
    # 然后更新父目录,子项目引用到更新后的
    git commit -am "更新submodule"

    #可以直接在子目录修改提交,和正常git操作一样
    ```

  * 其他人使用

    ```sh
    # 一次性克隆项目及子项目
    git clone --recursive https://xxx/repo.git
    
    # 或者先克隆项目
    git clone  https://xxx.git
    # 手动更新子项目
    git submodule init
    git submodule update --remote

    #可以直接在子目录修改提交,和正常git操作一样
    ```

  * 子项目.git目录储存到父项目的.git/modules目录
  ![git_submodules](webp/git/git_submodules.webp)

  * 用引用方式,显式操作

* Git Subtree

  * 添加子目录，建立与git项目的关联

    ```sh
    #-f在添加远程仓库之后，立即执行fetch
    git remote add -f <子仓库名> <子仓库地址>
    
    #–squash意思是把subtree的改动合并成一次commit，不用拉取子项目完整的历史记录。
    #–prefix之后的=等号也可以用空格。
    git subtree add --prefix=<子目录名> <子仓库名> <分支> --squash
    ```

  * 从远程仓库更新子目录

    ```sh
    git fetch <远程仓库名> <分支>
    git subtree pull --prefix=<子目录名> <远程分支> <分支> --squash
    ```

  * 从子目录push到远程仓库（确认你有写权限）

    ```sh
    git subtree push --prefix=<子目录名> <远程分支名> 分支
    ```

  * 用复制方式,隐式操作

* GitSlave

### 清除大文件

* 采用工具

* 清理仓库大文件需要修改仓库的提交历史，git-filter-repo 是 Git 官方社区推荐的修改仓库提交历史的工具，本文介绍使用 git-filter-repo 来清理仓库大文件的方法。
[看他](https://help.aliyun.com/document_detail/369469.htm?spm=a2c4g.11186623.0.0.43d46980JHMUZq#topic-2156461)

  ```bash
    pip3 install git-filter-repo
  ```

* 手动执行

```bash

# 完全清除git中大文件提交
# 查看大文件
# 使用verify-pack命令查看, pack包里面的最大的10个文件对应的hash值
# 根据rev-list命令来查看, 最大的文件的文件名是什么
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail -10 | awk '{print$1}')"

# 删除大文件
git filter-branch --force --index-filter "git rm -rf --cached --ignore-unmatch linux_x86_64/zinc_upx" --prune-empty --tag-name-filter cat -- --all

# 回收空间，清理本地仓库不可达对象;
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
rm -rf .git/refs/original/
rm -rf .git/logs/
git reflog expire --expire=now --all
git gc --prune=now
git gc --aggressive --prune=now

# 强制推到远程
git push origin --force --all 
# git push origin –-force --tag
git remote prune origin 

# ！！清理完之后,每个人一定要删掉之前拉取的项目, 重新从git上拉项目。不要使用之前的项目了！否则会不降反升。
```

### 清除未跟踪文件

```bash
# 清除文件
git clean -f
# 连目录也一起清除文件
git clean -fd
```
