# ai

### 国内较出名的AI助手

* <https://tongyi.aliyun.com/lingma/> 阿里通义

* <https://comate.baidu.com/zh/> baidu的ai代码助手

* <https://iflycode.xfyun.cn/> 科大讯飞ai代码助手

* <https://codegeex.cn/> 智谱的ai代码助手

### Finetuning

Fine tuning的原理就是利用已知的网络结构和已知的网络参数，修改output层为我们自己的层，微调最后一层前的所有层的参数，加大最后一层的学习率，因为最后一层我们需要重新学习，所以与其它层相比要有相对较大的学习率，这样就有效利用了深度神经网络强大的泛化能力，又免去了设计复杂的模型以及耗时良久的训练，所以fine tuning是当数据量不足时的一个比较合适的选择。

### Input type (torch.cuda.FloatTensor) and weight type (torch.FloatTensor) should be the

规解决方案
从报错问题描述中可以找到错误原因

输入的数据类型为torch.cuda.FloatTensor，说明输入数据在GPU中
模型参数的数据类型为torch.FloatTensor，说明模型还在CPU
问题原因搞清楚了，模型没加载到CPU，在代码中加一行语句就可以了

model = model.cuda()
model = model.to('cuda')
model.cuda()
model.to('cuda')
上面四行任选一，还有其他未列出的表述方法，都可以将模型加载到GPU。

反之Input type (torch.FloatTensor) and weight type (torch.cuda.FloatTensor) should be the问题来源是输入数据没有加载到GPU，解决方法为

tensor = tensor.cuda()
tensor = tensor.to('cuda')
任选任选
