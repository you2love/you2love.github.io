> 开发一个 MCP Skill 其实就是**编写一个能够响应 MCP 协议请求的程序**

### 第一步：环境准备

你需要安装 MCP 的官方 Python 库。

```bash
# 创建项目目录
mkdir mcp-smart-home-skill
cd mcp-smart-home-skill

# 推荐使用虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装核心库
pip install mcp
```

### 第二步：编写 Skill 代码

创建一个 Skill，让它具备“获取天气”和“控制灯光”的能力。

1.  **创建文件**：新建一个文件 `smart_home_skill.py`。

2.  **编写代码**：

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ImageContent
import requests
import json

# 初始化 MCP Server (也就是你的 Skill)
mcp = FastMCP("SmartHome Skill")

# ==========================================
# Skill 1: 获取天气 (外部 API 调用)
# ==========================================
@mcp.tool()
def get_weather(location: str) -> TextContent:
    """
    获取指定城市的天气情况。
    注意：这里使用的是模拟数据，实际使用需接入高德/和风等真实API。
    """
    # 这里是模拟逻辑，实际开发请替换为真实的 API 调用
    # 示例：调用高德地图天气API
    # url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={location}&key=你的KEY"
    
    weather_data = {
        "city": location,
        "weather": "晴",
        "temperature": "25°C",
        "wind": "微风"
    }
    result_text = f"【{location}天气】天气：{weather_data['weather']}，气温：{weather_data['temperature']}，风力：{weather_data['wind']}"
    
    return TextContent(type="text", text=result_text)

# ==========================================
# Skill 2: 控制智能灯 (模拟)
# ==========================================
# 假设我们有一个简单的状态存储
light_status = {"客厅": "关", "卧室": "关"}

@mcp.tool()
def control_light(room: str, action: str) -> TextContent:
    """
    控制指定房间的灯光开关。
    """
    if room not in light_status:
        return TextContent(type="text", text=f"错误：不支持{room}的灯光控制")
    
    # 执行控制逻辑（这里可以替换为发送 MQTT 指令）
    if action in ["开", "打开", "on"]:
        light_status[room] = "开"
        response = f"✅ 已为您打开{room}的灯"
    elif action in ["关", "关闭", "off"]:
        light_status[room] = "关"
        response = f"✅ 已为您关闭{room}的灯"
    else:
        response = f"❌ 指令错误，不支持的操作：{action}"
    
    # 打印状态用于调试
    print(f"灯光状态更新: {light_status}")
    return TextContent(type="text", text=response)

# ==========================================
# Skill 3: 查询设备状态
# ==========================================
@mcp.tool()
def get_device_status() -> TextContent:
    """
    获取当前所有智能设备的状态。
    """
    status_str = "🏠 当前设备状态：\n"
    for room, status in light_status.items():
        status_str += f"  {room}灯：{status}\n"
    
    return TextContent(type="text", text=status_str)

# ==========================================
# 启动入口
# ==========================================
if __name__ == "__main__":
    # 运行 MCP Server，等待客户端（如 Cursor）连接
    mcp.run(transport='stdio')
```

### 第三步：代码解析（Skill 的核心结构）

1.  **Server 初始化**：
    `mcp = FastMCP("SmartHome Skill")`：这行代码定义了你的 Skill 名字。AI 会通过这个名字来识别它能找谁帮忙。

2.  **Tool 定义（核心能力）**：
    使用 `@mcp.tool()` 装饰器来标记一个函数。**每一个被装饰的函数就是一个 Skill**。
    *   **函数名**：建议使用英文，代表 Skill 的唯一标识。
    *   **函数文档字符串 (Docstring)**：**极其重要**。AI 不读代码，只读注释。它决定了 AI 什么时候会调用这个 Skill。
    *   **参数**：定义好参数类型（str, int），AI 会自动帮你从自然语言中提取参数。

3.  **返回值格式**：
    MCP 协议要求返回特定的格式（如 `TextContent` 或 `ImageContent`），这样客户端才能正确解析并展示给用户。

### 第四步：在 Cursor 中配置并测试

1.  **启动服务**：
    在终端运行：
    ```bash
    python smart_home_skill.py
    ```
    *保持这个终端窗口打开。*

2.  **配置 Cursor**：
    打开 Cursor 设置 -> MCP Servers -> Add Server。
    *   **Name**: `SmartHome Skill`
    *   **Command**: `python`
    *   **Arguments**: `/path/to/your/smart_home_skill.py` (替换为你的实际路径)

3.  **测试对话**：
    在 Cursor 聊天框中输入：
    > “打开客厅的灯，然后查一下北京的天气。”

    **预期效果**：
    AI 会自动拆解任务，先调用 `control_light` Skill，再调用 `get_weather` Skill，最后把结果整合回复给你。

### 进阶：Skill 的工程化

如果Skill 变得很复杂（比如包含多个文件、配置文件、甚至前端界面），你可以参考以下结构：

```bash
my-mcp-skill/
├── main.py              # 入口文件 (启动 Server)
├── skills/             # 技能包
│   ├── __init__.py
│   ├── weather.py      # 天气技能模块
│   ├── light.py        # 灯光技能模块
│   └── database.py     # 数据库查询技能
├── config.py           # 配置文件 (API Keys)
├── pyproject.toml      # 打包配置
└── README.md
```

### 总结

开发一个 MCP Skill 的本质就是：
1.  **写函数**：想让 AI 做的事情写成 Python 函数。
2.  **写注释**：告诉 AI 这个函数是干什么的、什么时候用。
3.  **加装饰器**：加上 `@mcp.tool()`，把它暴露给 AI。
4.  **跑起来**：配置好客户端，让 AI 来调用它。
