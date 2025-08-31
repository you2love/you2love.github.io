# svn

## svn命令

1. 下载

```bash
svn checkout svn://host/svn/IOS/remote_dir (svn项目全路径）project_dir（本地目录全路径) --username 用户名 --password 密码
```

> svn checkout 简写：svn co

2. 添加新文件

```bash
svn add file（文件名）
svn add *.php(添加当前目录下所有的php文件)
```

3. 提交到版本库

```bash
svn commit -m "LogMessage" PATH
svn commit -m “提交当前目录下的全部在版本控制下的文件“ * （ *表示全部文件 ）
```

> svn commit 简写：svn ci

4. 更新文件

```bash
svn　update
svn　update　文件名
```

> 提交的时候提示过期冲突，需要先 update 修改文件
>
> 然后清除svn resolved，最后再提交commit。
>
> svn　update 间写： svn up

5. 查看文件或者目录状态

```bash
svn status [-v] path（目录下的文件和子目录的状态，正常状态不显示）
```

> ?：不在svn的控制中；
>
> M：内容被修改；
>
> C：发生冲突；
>
> A：预定加入到版本库；
>
> K：被锁定
>
> D:文件、目录或是符号链item预定从版本库中删除。
>
> I:忽略
>
> svn status 简写：svn st

6. 查看日志（显示文件的所有修改记录，及其版本号的变化）

```bash
# 查看最近3条日志
svn log [path] -l 3 
```

7. 解决冲突

```bash
# 手工解决冲突后,移除工作副本的目录或文件的“冲突”状态,再提交
svn resolved PATH
```

8. 删除文件

```bash
# 本地先删,再提交
svn delete test.php 
svn ci -m 'delete test file‘
```

9. 恢复本地修改

```bash
# 用法: revert PATH...
svn revert: 恢复原始未改变的工作副本文件 (恢复大部份的本地修改)。
```

> 注意: 本子命令不会存取网络，并且会解除冲突的状况。但是它不会恢复被删除的目录

```bash
# 丢弃对一个文件的修改
svn revert foo.c
# 恢复一整个目录的文件，. 为当前目录
svn revert --recursive . 
```

10. 版本库下的文件和目录列表

```bash
svn list [path]
```

11. 忽略目录

```bash
# 注意没有目录斜杠
svn propset svn:ignore .idea .
```

12. 查看文件详细信息

```bash
# svn info path
svn info test.php
```

13. 比较差异

```bash
# svn diff path(将修改的文件与基础版本比较)
svn diff test.php

# svn diff -r m:n path(对版本m和版本n比较差异)
svn diff -r 200:201 test.php
```

> svn diff 简写：svn di

14. SVN 帮助

```bash
svn help 全部功能选项
svn help ci 具体功能的说明
```

15. 上传

```bash
svn import project_dir（本地项目全路径） http://host/svn/IOS/Ben/remote_dir（svn项目全路径） -m "必填, 不填此命令执行不会成功."
```

> 服务器上remote_dir若不存在, 会自动创建;
>
> 只会上传project_dir目录下的文件到remote_dir的目录下
>
> import之后, project_dir并没有自动转化为工作目录, 需要重新checkout(后面会用到)
