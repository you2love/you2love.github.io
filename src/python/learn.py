# import paddle

# # print('飞桨框架内置模型：', paddle.vision.models.__all__)

# # 模型组网并初始化网络
# lenet = paddle.vision.models.LeNet(num_classes=10)

# for name, param in lenet.named_parameters():
#     print(f"Layer: {name} | Size: {param.shape}")

# # 可视化模型组网结构和参数
# paddle.summary(lenet, (1, 1, 28, 28))

import numpy

# 引用 paddle inference 预测库
import paddle.inference as paddle_infer

model_dir = '/Users/junjunyi/.paddleocr/whl/det/ch/ch_PP-OCRv3_det_infer'
import os

pdm_file = os.path.join(model_dir, "inference.pdmodel")
pdi_file = os.path.join(model_dir, "inference.pdiparams")
# 创建 config
config = paddle_infer.Config(pdm_file, pdi_file)

# 根据 config 创建 predictor
predictor = paddle_infer.create_predictor(config)

print('predictor', predictor, dir(predictor))

# 获取输入 Tensor
input_names = predictor.get_input_names()
print('input_names', input_names)

input_tensor = predictor.get_input_handle(input_names[0])
print('input_tensor', dir(input_tensor), input_tensor.shape(),
      input_tensor.type())

# 从 CPU 获取数据，设置到 Tensor 内部
# fake_input = numpy.random.randn(1, 3, 224, 224).astype("float32")
# input_tensor.copy_from_cpu(fake_input)

# # 执行预测
# predictor.run()

# # 获取输出 Tensor
# output_names = predictor.get_output_names()
# output_tensor = predictor.get_output_handle(output_names[0])

# # 释放中间 Tensor
# predictor.clear_intermediate_tensor()

# # 释放内存池中的所有临时 Tensor
# predictor.try_shrink_memory()
