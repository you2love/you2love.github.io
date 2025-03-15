# docker

code-server：远程开发神器
让你在任何设备的浏览器中都能访问完整的VS Code开发环境，无需本地安装和配置。

当你需要在平板、笔记本或其他设备间切换时，所有的代码、插件和设置都保持同步，彻底解决了"换台电脑又要重新配环境"的痛点。

```sh
docker run -d \
  --name code-server \
  -p 8080:8080 \
  -v "$HOME/.config:/home/coder/.config" \
  -v "$PWD:/home/coder/project" \
  codercom/code-server:latest
```

```yml
version: "3"
services:
  code-server:
    image: codercom/code-server:latest
    ports:
      - "8080:8080"
    volumes:
      - ~/.config:/home/coder/.config
      - .:/home/coder/project
    environment:
      - PASSWORD=yourpassword
```

CloudBeaver：数据库管理
CloudBeaver 是一个基于Web的数据库管理工具，它让你可以在浏览器中轻松管理各种数据库。

特点：

多数据库支持：支持MySQL、PostgreSQL、SQLite等多种数据库。
Web界面：界面清爽，用起来顺手。

```sh
docker run -d \
  --name cloudbeaver \
  -p 8978:8978 \
  dbeaver/cloudbeaver:latest
```

```yml
version: "3"
services:
  cloudbeaver:
    image: dbeaver/cloudbeaver:latest
    ports:
      - "8978:8978"
    volumes:
      - ./workspace:/opt/cloudbeaver/workspace
```

 📁 Filebrowser：在线文件管理器
一个轻量级的文件管理器。

特别适合那些需要远程访问和管理文件但又不想安装复杂软件的用户。

它支持文件的上传、下载、编辑以及权限管理，更适用于个人或小团队。

```sh
ocker run -d \
  --name filebrowser \
  -v $PWD/filebrowser:/srv \
  -p 80:80 \
  filebrowser/filebrowser
```

```yml
version: "3.8"
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - $PWD/filebrowser:/srv # 设置你的文件目录
      - $PWD/filebrowser.db:/database # 设置你的数据库目录
```
