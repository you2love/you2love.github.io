# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

# sk-ed1c3042cc5f46ccae2b152f45c3830c
client = OpenAI(
    api_key="sk-ed1c3042cc5f46ccae2b152f45c3830c",
    base_url="https://api.deepseek.com",
)

# OpenAI API中支持的role类型包括：
# system: 设定背景、上下文或模型角色。
# user: 代表用户的输入。
# assistant: 代表模型的回复。

# 常见system指令的应用场景
# 设定角色：
# {"role": "system", "content": "你是一个医药行业专家，擅长分析疫苗相关问题。"}
# 定义任务：
# {"role": "system", "content": "请从药品原理、市场利益和国家政策角度分析问题。"}
# 调整风格：
# {"role": "system", "content": "请用简洁的语言回答，避免使用专业术语。"}
# 提供背景信息：
# {"role": "system", "content": "这是一次关于疫苗的讨论，请专注于疫苗的技术和市场方面。"}
#
response = client.chat.completions.create(
    # model="deepseek-chat",
    model="deepseek-reasoner",
    messages=[
        {
            "role": "system",
            "content": "假设你是一个医药行业专家,帮忙分析一下原因.从药品原理,利益,国家政策等方面分析",
        },
        {"role": "user", "content": "安在时乙肝疫苗，国内为什么没有"},
    ],
    stream=False,
)

print(response.choices[0].message.content)
