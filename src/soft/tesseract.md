# tesseract

### 安装

```sh
# 多半已安装过了,最新版本为5.xx
brew install tesseract

# This formula contains only the "eng", "osd", and "snum" language data files.
# If you need any other supported languages, run `brew install tesseract-lang`

# 本质是下载github所有训练完好的模型数据,放在/opt/homebrew/share/tessdata,供tesseract调用
brew install tesseract-lang
```

### 使用

```bash
# 获取帮助
tesseract --help-extra

# 告诉tesseract 源文件chinese.png -l 表示中文 stdout输出到标准库
tesseract chinese.png stdout -l chi_sim

# 类似数字识别
tesseract digit.png stdout -l snum

# 类似英文识别
tesseract english.png stdout -l eng

# 单行文本识别率非常不错,多行错误率非常高
```
