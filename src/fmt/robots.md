# robots.txt
<!-- toc --> 

## 简介

- 网站告知搜索引擎爬虫哪些页面可以抓取、哪些页面禁止抓取的协议文件

- 放网站的根目录下

- 纯文本形式编写,每行一条指令，不区分大小写

- 主要部分:
  - **用户代理（User - agent）**
  - **允许指令（Allow）**
  - **禁止指令（Disallow）**
  - **站点地图（Sitemap）**

## User - agent（用户代理）
- **作用**：指定该规则适用的搜索引擎爬虫（如百度蜘蛛、谷歌爬虫等）。
- **格式**：`User - agent: [爬虫名称]`
- **说明**：
  - 若使用 `User - agent: *`，表示该规则适用于所有未被单独指定的爬虫。
  - 常见爬虫名称：`Baiduspider`（百度）、`Googlebot`（谷歌）、`360spider`（360）等。

  **示例**：
  ```
  User - agent: Baiduspider  # 仅适用于百度爬虫
  User - agent: *            # 适用于其他所有爬虫
  ```

## Disallow（禁止抓取）
- **作用**：指定禁止爬虫抓取的URL路径。
- **格式**：`Disallow: [路径]`
- **说明**：
  - 路径支持通配符（部分爬虫支持，如谷歌）：`*` 代表任意字符，`$` 代表URL结尾。
  - 若 `Disallow: /`，表示禁止抓取网站所有内容；若 `Disallow:`（空值），表示允许抓取所有内容。

  **示例**：
  ```
  Disallow: /admin/    # 禁止抓取/admin/目录下的所有内容
  Disallow: /private$  # 禁止抓取以/private结尾的URL（如https://example.com/private）
  Disallow: /*.pdf$    # 禁止抓取所有PDF文件（部分爬虫支持）
  ```

## Allow（允许抓取）
- **作用**：在 `Disallow` 的基础上，指定允许抓取的子路径（优先级高于 `Disallow`）。
- **格式**：`Allow: [路径]`
- **示例**：
  ```
  User - agent: *
  Disallow: /admin/    # 禁止抓取/admin/目录
  Allow: /admin/public/ # 但允许抓取/admin/public/子目录
  ```

## Sitemap（站点地图）
- **作用**：告知爬虫网站的站点地图（sitemap）位置，帮助爬虫更高效地抓取内容。
- **格式**：`Sitemap: [sitemap的URL]`
- **示例**：
  ```
  Sitemap: https://example.com/sitemap.xml
  Sitemap: https://example.com/sitemap_news.xml  # 可指定多个站点地图
  ```


## 完整示例
```
# 禁止百度爬虫抓取/admin/和/user/目录
User - agent: Baiduspider
Disallow: /admin/
Disallow: /user/

# 允许谷歌爬虫抓取所有内容，但禁止PDF文件
User - agent: Googlebot
Allow: /
Disallow: /*.pdf$

# 对其他所有爬虫，仅禁止抓取/private/目录
User - agent: *
Disallow: /private/

# 站点地图位置
Sitemap: https://example.com/sitemap.xml
```


## 四、注意事项
1. **优先级**：同一 `User - agent` 下，`Allow` 指令优先级高于 `Disallow`；不同 `User - agent` 规则独立生效。
2. **通配符支持**：并非所有爬虫都支持 `*` 和 `$`（如百度对通配符支持有限），需参考对应搜索引擎的文档。
3. **注释**：以 `#` 开头的内容为注释，不影响规则执行。
4. **权限限制**：robots.txt 仅为“协议”，恶意爬虫可能无视规则，敏感内容需通过登录验证等方式保护。


## 五、常见错误格式
- 错误使用大小写混合（如 `User - Agent: *`，虽不报错，但不规范）。
- 路径格式错误（如遗漏 `/`，`Disallow: admin` 可能被解析为禁止抓取包含“admin”字符的任意URL）。
- 多个 `User - agent` 共用同一组规则时未正确分组（需每组规则前单独指定 `User - agent`）。