# paddleocr示例
<!-- toc --> 

### [百度开源Paddle](https://www.paddlepaddle.org.cn/)

* 安装框架

```bash
python3 -m pip install paddlepaddle==2.4.2 -i https://mirror.baidu.com/pypi/simple
```

* 安装ocr

```bash
pip3 install "paddleocr>=2.0.1" -i https://mirror.baidu.com/pypi/simple
```

* [m1芯片特别安装](https://github.com/PaddlePaddle/PaddleOCR/issues/6720)
  * Download source code locally
  * In requirements.txt, update to opencv-contrib-python==4.6.0.66
  * Pip install - r requirements.txt
  * python setup.py install
  * ppadleocr 安装在/opt/homebrew/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin
  * 第一次运行会下载训练好的模型到~/.paddleocr目录
  * ln -s /opt/homebrew/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin/paddleocr paddleocr

* 安装paddleocrlabel

* [m1芯片源码安装]

  * 下载源码

  ```bash
  git clone git@github.com:PaddlePaddle/PaddleOCR.git
  cd PPOCRLabel
  python setup.py install
  # 如果出现安装pyqt5失败,则采用brew install pyqt5
  Installing PPOCRLabel script to /opt/homebrew/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin
  cd /opt/homebrew/bin
  ln -s /opt/homebrew/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin/PPOCRLabel PPOCRLabel


  # 运行,第一运行会下载必要东西~/.paddleocr目录
  PPOCRLabel --lang ch
  # 针对特别业务,可以事先处理图片,再传入自动标注
  ```

```bash
# applie m1 芯片安装,会有问题，因为没有直接aarch64.whl,需要重头编译,但目前没有办法成功
pip3 install pyqt5

# 幸好brew可以帮忙编译
brew install pyqt5
```

* 模型结构可视化VisualDL

```bash
python3 -m pip install visualdl -i https://mirror.baidu.com/pypi/simple
# Running VisualDL at http://localhost:8040/ (Press CTRL+C to quit)
./visualdl
# 网络结构-静态，把模型文件拖进去<https://www.paddlepaddle.org.cn/inference/master/guides/export_model/visual_model.html>
```

```python
#!python3
import re
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# need to run only once to download and load model into memory
ocr = PaddleOCR(use_angle_cls=False, lang="ch", show_log=False)
img_path = '01.jpg'
result = ocr.ocr(img_path, cls=False)
# for line in result:
#     for box in line:
#         print(type(box), box)
#     break

result = result[0]
# 显示结果

image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
boxes = [result[0]]
txts = [result[1][0]]
scores = [result[1][1]]
im_show = draw_ocr(image, boxes, txts, scores, font_path='simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
```

### [运行 Dynamic shape](https://www.paddlepaddle.org.cn/inference/master/guides/nv_gpu_infer/gpu_trt_infer.html)

>当模型的输入 shape 不固定的话（如 OCR，NLP 的相关模型），需要推理框架提供动态 shape 的支持。
从1.8 版本开始， Paddle Inference 对 TensorRT 子图进行了 Dynamic shape 的支持。 使用接口如下：

```python
 config.enable_tensorrt_engine(
  workspace_size = 1<<30,
  max_batch_size=1, min_subgraph_size=5,
  precision_mode=paddle_infer.PrecisionType.Float32,
  use_static=False, use_calib_mode=False)

 min_input_shape = {"image":[1,3, 10, 10]}
 max_input_shape = {"image":[1,3, 224, 224]}
 opt_input_shape = {"image":[1,3, 100, 100]}

 config.set_trt_dynamic_shape_info(min_input_shape, max_input_shape, opt_input_shape)
```

> 从上述使用方式来看，在 config.enable_tensorrt_engine 接口的基础上，新加了一个 config.set_trt_dynamic_shape_info 的接口。
“image” 对应模型文件中输入的名称。
该接口用来设置模型输入的最小、最大、以及最优的输入 shape。
其中，最优的 shape 处于最小最大 shape 之间，在推理初始化期间，会根据opt shape对 Op 选择最优的 Kernel 。
调用了 config.set_trt_dynamic_shape_info 接口，推理器会运行 TensorRT 子图的动态输入模式，运行期间可以接受最小、最大 shape 间的任意 shape 的输入数据。
