# docx文件
<!-- toc --> 

## 概念

docx 文件本质上是一个包含多个 XML 文件的 ZIP 压缩包

### 1. 顶层结构：文档包（Package）
- **docx 逻辑结构**：整个 `.docx` 文件是一个「文档包」，包含所有组成文档的资源（XML 文件、图片、样式定义等），通过 ZIP 压缩格式存储。
- **python-docx 对应**：`Document` 对象  
  是操作的入口，代表整个文档。通过 `docx.Document()` 创建或打开文档，封装了对底层包的所有操作。


### 2. 内容容器：节（Section）
- **docx 逻辑结构**：文档包内的内容被划分为「节」（Section），每个节可以独立设置页面格式（如页边距、纸张大小、方向等）。默认情况下，文档至少包含 1 个节。
- **python-docx 对应**：`Section` 对象  
  通过 `doc.sections` 访问所有节（列表形式），例如 `doc.sections[0]` 获取第一个节。


### 3. 块级元素（Block-Level Elements）
节内包含的「块级元素」是文档的核心内容，按顺序排列，占据一整块区域（如段落、表格等）。

| docx 逻辑结构       | 说明                                  | python-docx 对应对象       | 访问方式示例                  |
|--------------------|---------------------------------------|---------------------------|-----------------------------|
| 段落（Paragraph）   | 文本内容的基本单元，可包含多个文本片段  | `Paragraph`               | `doc.paragraphs`（所有段落） |
| 表格（Table）       | 由行和列组成的结构化数据容器            | `Table`                   | `doc.tables`（所有表格）     |
| 图片（Picture）     | 嵌入文档的图像资源（本质上包含在段落中）| 无单独对象，通过段落插入   | `doc.add_picture()`         |
| 分页符（Page Break） | 强制分页的标记                        | 无单独对象，通过 Run 插入  | `run.add_break(WD_BREAK.PAGE)` |


### 4. 段落内部结构：运行（Run）
- **docx 逻辑结构**：段落（Paragraph）由一个或多个「运行」（Run）组成。每个 Run 是一段连续的、具有相同格式（字体、大小、颜色等）的文本。
- **python-docx 对应**：`Run` 对象  
  通过 `paragraph.runs` 访问段落内的所有 Run，例如 `para.runs[0]` 获取段落的第一个文本片段。


### 5. 表格内部结构
- **docx 逻辑结构**：表格（Table）由「行（Row）」和「单元格（Cell）」组成，单元格内可包含段落、文本等内容。
- **python-docx 对应**：
  - `Table`：表格对象，通过 `doc.add_table()` 创建。
  - `Row`：表格行对象，通过 `table.rows` 访问。
  - `Cell`：单元格对象，通过 `table.cell(row_idx, col_idx)` 或 `row.cells` 访问。  
    单元格内的内容通过 `cell.paragraphs` 访问（单元格本质上是段落的容器）。


### 6. 样式系统（Styles）
- **docx 逻辑结构**：包含「段落样式」「字符样式」等，用于统一文档格式，定义在 `styles.xml` 中。
- **python-docx 对应**：`Style` 对象  
  通过 `doc.styles` 访问所有样式（列表形式），例如 `doc.styles['Heading 1']` 获取一级标题样式。


### 7. 页眉页脚（Header/Footer）
- **docx 逻辑结构**：每个节（Section）可包含独立的「页眉」和「页脚」，定义在 `header.xml` 和 `footer.xml` 中，用于存放每页顶部/底部的固定内容（如页码、标题）。
- **python-docx 对应**：`Header` 和 `Footer` 对象  
  通过节对象访问：`section.header`（页眉）、`section.footer`（页脚），其内部内容通过 `header.paragraphs` 或 `footer.paragraphs` 操作。


### 8. 页面设置（Page Settings）
- **docx 逻辑结构**：定义节的页面属性（如页边距、纸张大小、方向等），存储在 `settings.xml` 中。
- **python-docx 对应**：`Section` 对象的属性  
  例如：`section.left_margin`（左页边距）、`section.page_width`（页面宽度）、`section.orientation`（页面方向）等。

## 代码

### 一、基础操作：创建与保存文档
```python
from docx import Document

# 1. 创建新文档
doc = Document()

# 2. 打开已有文档
doc = Document("existing.docx")  # 仅支持 .docx 格式

# 3. 保存文档
doc.save("output.docx")
```


### 二、文本内容操作
#### 1. 添加标题
```python
# 添加标题（level：0-9，0 为最高级标题，1-9 逐级降低）
doc.add_heading("主标题", level=0)
doc.add_heading("一级标题", level=1)
doc.add_heading("二级标题", level=2)
```

#### 2. 添加段落与文本片段
```python
# 添加普通段落
para = doc.add_paragraph("这是一个普通段落。")

# 向段落添加带格式的文本片段（Run）
para = doc.add_paragraph("我是")
run = para.add_run("加粗文本")
run.bold = True  # 加粗
para.add_run("，我是")
run = para.add_run("斜体文本")
run.italic = True  # 斜体
para.add_run("。")
```

#### 3. 设置文本格式（字体、大小、颜色等）
```python
from docx.shared import Pt, RGBColor

para = doc.add_paragraph()
run = para.add_run("自定义格式文本")
run.font.name = "微软雅黑"  # 字体
run.font.size = Pt(14)  # 字号（14磅）
run.font.color.rgb = RGBColor(255, 0, 0)  # 红色（RGB值）
run.underline = True  # 下划线
run.font.bold = True  # 加粗
```


### 三、段落格式设置
```python
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches

para = doc.add_paragraph("设置段落格式的示例文本")

# 1. 对齐方式（左对齐、居中、右对齐、两端对齐）
para.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 居中对齐

# 2. 缩进（左缩进、右缩进、首行缩进）
para.paragraph_format.left_indent = Inches(0.5)  # 左缩进0.5英寸
para.paragraph_format.first_line_indent = Inches(0.3)  # 首行缩进0.3英寸

# 3. 行间距与段间距
para.paragraph_format.line_spacing = 1.5  # 1.5倍行间距
para.paragraph_format.space_before = Pt(12)  # 段前间距12磅
para.paragraph_format.space_after = Pt(6)  # 段后间距6磅
```


### 四、列表操作
```python
# 1. 无序列表（项目符号）
doc.add_paragraph("项目1", style="List Bullet")
doc.add_paragraph("项目2", style="List Bullet")

# 2. 有序列表（编号）
doc.add_paragraph("步骤1", style="List Number")
doc.add_paragraph("步骤2", style="List Number")

# 3. 嵌套列表（通过缩进实现）
para = doc.add_paragraph("主项目", style="List Bullet")
para = doc.add_paragraph("子项目", style="List Bullet 2")  # 二级列表
para.paragraph_format.left_indent = Inches(0.5)  # 缩进增强嵌套效果
```


### 五、表格操作
#### 1. 创建表格并填充内容
```python
# 创建3行2列的表格（可选指定样式）
table = doc.add_table(rows=3, cols=2, style="Table Grid")

# 填充表头
table.cell(0, 0).text = "姓名"
table.cell(0, 1).text = "年龄"

# 填充内容
table.cell(1, 0).text = "张三"
table.cell(1, 1).text = "25"
table.cell(2, 0).text = "李四"
table.cell(2, 1).text = "30"
```

#### 2. 表格进阶操作
```python
# 新增行/列
table.add_row()  # 末尾新增一行
table.add_column(Inches(1.5))  # 新增一列（指定宽度）

# 合并单元格（合并第一行前两列）
cell1 = table.cell(0, 0)
cell2 = table.cell(0, 1)
cell1.merge(cell2)

# 单元格内设置文本格式（通过段落和Run）
cell = table.cell(1, 0)
run = cell.paragraphs[0].add_run("带格式的单元格文本")
run.bold = True
run.font.color.rgb = RGBColor(0, 0, 255)  # 蓝色
```


### 六、插入图片
```python
from docx.shared import Inches, Cm

# 插入图片（指定路径，可选宽度/高度，避免变形）
doc.add_picture("image.png", width=Inches(3))  # 宽度3英寸（高度自动按比例）
doc.add_picture("photo.jpg", height=Cm(5))  # 高度5厘米（宽度自动按比例）
```


### 七、页面设置
```python
from docx.enum.section import WD_ORIENT
from docx.shared import Inches

# 获取第一个节（默认文档至少有一个节）
section = doc.sections[0]

# 1. 页边距（上、下、左、右）
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.left_margin = Inches(1.25)
section.right_margin = Inches(1.25)

# 2. 纸张大小（例如：A4纸 21cm×29.7cm）
section.page_width = Inches(8.27)  # A4宽度（约8.27英寸）
section.page_height = Inches(11.69)  # A4高度（约11.69英寸）

# 3. 页面方向（横向/纵向）
section.orientation = WD_ORIENT.LANDSCAPE  # 横向（默认纵向：PORTRAIT）
```


### 八、页眉页脚与页码
```python
# 获取页眉/页脚（基于当前节）
header = section.header
footer = section.footer

# 页眉添加内容
header.paragraphs[0].text = "这是文档页眉 - 机密"

# 页脚添加页码（使用域代码）
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

p = footer.add_paragraph()
run = p.add_run()
fldChar = OxmlElement('w:fldChar')  # 域字符
fldChar.set(qn('w:fldCharType'), 'begin')
run._r.append(fldChar)

instrText = OxmlElement('w:instrText')
instrText.text = 'PAGE'  # 页码域代码
run._r.append(instrText)

fldChar = OxmlElement('w:fldChar')
fldChar.set(qn('w:fldCharType'), 'end')
run._r.append(fldChar)

p.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 页码居中
```


### 九、处理已有文档
```python
# 1. 读取文档内容（遍历段落）
doc = Document("existing.docx")
for para in doc.paragraphs:
    print(para.text)  # 打印所有段落文本

# 2. 修改已有段落
if len(doc.paragraphs) > 0:
    doc.paragraphs[0].text = "修改后的第一段内容"  # 替换第一段文本

# 3. 读取表格内容
for table in doc.tables:
    for row in table.rows:
        row_text = [cell.text for cell in row.cells]
        print("行内容：", row_text)
```
