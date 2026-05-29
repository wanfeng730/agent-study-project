from dotenv import load_dotenv

from langchain.tools import tool
from langchain.agents import create_agent

# 加载环境变量
load_dotenv()

# 定义工具
@tool
def get_weather(location: str) -> str:
    """
    Get the weather in a given location
    Args:
        location: city name or coordinates
    """
    return f'Current weather in {location} is sunny'


# 创建智能体对象(模型名称、工具函数)
agent = create_agent(
    model='deepseek-v4-pro', 
    tools=[get_weather]
)
print('智能体对象已创建')

# 调用Agent
res = agent.invoke({
    "messages": [
        {"role": "user", "content": "杭州今天的天气如何？"}
    ]
})
print(f'智能体对象已调用 结果：{res}')