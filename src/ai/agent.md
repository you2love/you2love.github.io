# 智能体=大模型+SKILL+MCP

如果把智能体（Agent）比作一个**“活生生的人”**，那么你的这个等式可以完美拆解为：

*   **大模型 (LLM) = 大脑（思考与决策）**
*   **SKILL = 本事（会开车、会做饭、会修电脑）**
*   **MCP = 神经系统（连接大脑与手脚的通道）**

### 1. 大模型 (LLM)：大脑
这是智能体的**“认知核心”**。
*   **它负责什么：** 理解用户说的话（自然语言理解）、思考怎么解决问题（推理规划）、决定下一步该调用哪个技能（决策）。
*   **没有大脑会怎样：** 就像植物人，虽然有手有脚（有技能），但动不了。

### 2. SKILL：本事/手脚
这是智能体的**“能力单元”**。
*   **它负责什么：** 真正去“干活”。比如“发邮件”是一个 Skill，“画图”是一个 Skill，“查天气”也是一个 Skill。
*   **没有 Skill 会怎样：** 就像一个只会夸夸其谈的书呆子。你问它“帮我订张机票”，它只能说“好的，正在为您查询...”，但实际根本动不了手。**Skill 是具体执行动作的实体。**

### 3. MCP：神经系统/USB接口
这是智能体的**“连接标准”**。
*   **它负责什么：** 建立大模型和 Skill 之间的通信。它告诉大模型：“外面有这些 Skill 可以用”，并且负责把大模型的指令（“我要用这个 Skill”）翻译成 Skill 能听懂的代码格式（API 调用），再把 Skill 执行的结果传回给大模型。
*   **没有 MCP 会怎样：** 大脑想动脚，但神经断了，脚根本收不到信号。或者就像你有一个 Type-C 接口的手机（Skill），但充电器是老式圆孔的（不兼容），插不上，没法用。

---

### 🚀 举个例子：点外卖

假设用户的指令是：**“饿了，帮我点一份麦当劳，送到工位。”**

1.  **大脑（大模型）** 开始思考：
    *   “用户饿了，需要食物。”
    *   “我需要调用‘点外卖’这个能力。”
    *   “但我还需要知道他的地址和手机号。”（可能会先调用“获取个人信息”的Skill）

2.  **神经系统（MCP）** 开始工作：
    *   大脑通过 MCP 协议喊话：“谁有‘点外卖’这个 Skill？”
    *   MCP 发现有一个“美团外卖”的 Skill 接在系统上。
    *   MCP 建立连接通道。

3.  **本事（SKILL）** 开始执行：
    *   “点外卖 Skill” 接收到参数（麦当劳、地址）。
    *   它自动运行代码，打开浏览器，登录账号，搜索店铺，下单支付。

4.  **反馈：**
    *   Skill 把“下单成功”的消息通过 MCP 传回给大脑。
    *   大脑对你说：“老板，饭点好了，预计20分钟后到。”

### 总结

公式 **`智能体 = 大模型 + SKILL + MCP`** 完美概括了现代 AI 智能体的架构：

*   **大模型** 负责 **“想”** （策略）
*   **SKILL** 负责 **“做”** （执行）
*   **MCP** 负责 **“连”** （通信）

有了这三样，AI 才从一个**“聊天机器人”**（只能动嘴），进化成了一个**“数字员工”**（能动手、能跑腿）。

### 最简单的智能体

> 用 Python 实现一个“最简单”的智能体，核心其实就是搭建一个**“大脑循环”**。这个循环非常精简，只做一件事：**规划 -> 决策（选动作） -> 执行 -> 输出**。
> 用一个**“懒人点餐助手”**为例。这个智能体有两个核心能力（技能）：**搜索**（查餐厅）和 **Finish**（给出最终回答）。

```python
import os
import json
import requests

# ============ 配置区 ============
# 替换为你的 API Key
API_KEY = "your-api-key-here"
BASE_URL = "https://api.deepseek.com" # DeepSeek 的接口地址

# ============ 工具定义 (你的 Skill 库) ============
# 这是智能体的“技能包”，告诉模型它能做什么
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_restaurant",
            "description": "根据用户需求搜索附近的餐厅",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户想吃的菜系或餐厅名，例如 '川菜'、'火锅'"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "final_response",
            "description": "当信息收集完毕，用来给用户最终回复",
            "parameters": {
                "type": "object",
                "properties": {
                    "final_message": {
                        "type": "string",
                        "description": "给用户的最终回复内容"
                    }
                },
                "required": ["final_message"]
            }
        }
    }
]

# ============ 工具函数 (真正干活的代码) ============
def search_restaurant(query):
    """模拟搜索餐厅的函数"""
    print(f"\n[工具调用] 正在搜索: {query}...")
    # 这里可以接入真实的高德/美团API，这里用模拟数据
    return f"为您找到以下餐厅：1. 老王川菜馆(评分4.8) 2. 麻辣江湖(评分4.6) 3. 川味一绝(评分4.5)"

def final_response(final_message):
    """输出最终结果"""
    print(f"\n[结束] 智能体说: {final_message}")
    return "任务完成"

# ============ 智能体核心循环 ============
def run_agent(user_input):
    # 1. 初始化消息历史
    messages = [{"role": "user", "content": user_input}]
    
    print(f"[输入] 用户说: {user_input}")
    
    while True:
        try:
            # 2. 调用大模型 (大脑)
            response = requests.post(
                f"{BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat", # 使用 DeepSeek 模型
                    "messages": messages,
                    "tools": TOOLS, # 告诉模型有哪些技能
                    "tool_choice": "auto" # 自动选择技能
                }
            )
            
            # 3. 解析模型返回
            resp_json = response.json()
            message = resp_json.choices[0].message
            
            # 4. 判断模型是否想调用工具
            if message.tool_calls:
                # --- 决策：模型选择了某个 Skill ---
                tool_call = message.tool_calls[0]
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"[思考] 嗯...我需要调用 '{tool_name}' 这个技能来解决。")
                
                # 把模型的回复加到历史里（记录它的思考）
                messages.append(message)
                
                # --- 执行：运行具体的 Skill 代码 ---
                if tool_name == "search_restaurant":
                    tool_result = search_restaurant(tool_args["query"])
                elif tool_name == "final_response":
                    final_response(tool_args["final_message"])
                    break # 结束循环
                
                # --- 反馈：把工具执行的结果告诉模型 ---
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result
                })
                
            else:
                # 模型直接给出了答案（没有调用工具）
                print(f"[结束] 智能体说: {message.content}")
                break
                
        except Exception as e:
            print(f"发生错误: {e}")
            break

# ============ 运行测试 ============
if __name__ == "__main__":
    # 测试：用户输入
    run_agent("我想吃火锅，帮我推荐几家附近的。")
```

### 第三步：代码解析（智能体的四大要素）

运行这段代码，发现它其实就包含了智能体的所有核心要素：

1.  **大脑（LLM）**：
    *   `requests.post(...)` 这一部分就是调用大模型。
    *   它负责**思考**：是直接回答，还是去查餐厅？

2.  **技能（Skills/Tools）**：
    *   `TOOLS` 列表定义了智能体能做什么。
    *   `search_restaurant` 是一个 Skill（查餐厅）。
    *   `final_response` 是另一个 Skill（结束对话）。

3.  **规划与决策（The Loop）**：
    *   `while True` 循环就是智能体的“心跳”。
    *   它不断检查：“我需要调用工具吗？” -> “调用哪个？” -> “执行结果是什么？” -> “下一步怎么做？”。

4.  **执行（Function Call）**：
    *   `if tool_name == ...` 这一段就是真正执行代码的地方。

### 运行效果

当你运行代码时，输出大概是这样的：

```bash
[输入] 用户说: 我想吃火锅，帮我推荐几家附近的。
[思考] 嗯...我需要调用 'search_restaurant' 这个技能来解决。

[工具调用] 正在搜索: 火锅...
[思考] 嗯...我需要调用 'final_response' 这个技能来解决。

[结束] 智能体说: 为您找到以下餐厅：1. 老王川菜馆... (省略)
```
