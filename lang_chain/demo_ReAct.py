# Desc  : demo_ReAct.
# Time  : 2026/6/12 16:28
# Author: wanfeng
import sqlite3

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.checkpoint.sqlite import SqliteSaver

from lang_chain.demo_agent import WeatherInfo
from lang_chain.init_chat_models import model_qwen_plus
from lang_chain.utils import read_file_content
from python_base.date_util import get_current_date_time

# 加载环境变量
load_dotenv()


model = model_qwen_plus()

@tool(args_schema=WeatherInfo)
def get_weather_better(location: str, temperature_unit: str = "摄氏度", is_include_humidity: bool = False) -> str:
    """获取某个地区的详细信息
    """
    tem = 28 if temperature_unit == '摄氏度' else 78
    result = f'{location} 现在的天气是晴天, 温度为{tem}{temperature_unit}'
    if is_include_humidity:
        result += ', 湿度为67%'
    return result;


system_prompt = read_file_content('resources/prompt_ReAct.md')
print(f'读取系统提示词 len={len(system_prompt)}')

# 初始化sqlite连接
sqlite_connection = sqlite3.connect('db/demo_ReAct.db', check_same_thread=False)
sqlite_checkpointer = SqliteSaver(sqlite_connection)
sqlite_checkpointer.setup()

# 总结摘要中间件    trigger 触发条件、keep 需要保持的状态
middleware = SummarizationMiddleware(
    model=model,
    trigger=('tokens', 1000),
    keep=('messages', 20)
)

# agent = create_agent(model='deepseek-v4-pro', tools=[get_weather])
agent = create_agent(
    model=model,
    system_prompt=system_prompt,
    tools=[
        get_weather_better
    ],
    checkpointer=sqlite_checkpointer,
    middleware=[
        middleware
    ]
)

def test_agent_ReAct():
    invoke_config = RunnableConfig(configurable={
        "thread_id": get_current_date_time()
    })
    res = agent.stream(
        {"messages": [ HumanMessage("根据天气帮我推荐一下今天合适的穿搭，地点是杭州")] },
        config=invoke_config,
        stream_mode="values"
    )
    for data in res:
        # print(f"chunk({type(data)}): {data}")

        # 消息内容（包含本次会话历史消息）
        messages = data['messages']
        # 最近一条消息
        latest_message = data['messages'][-1]
        print(f"lastest_message({type(latest_message)}): {latest_message}")

        # if isinstance(latest_message, AIMessage):
        #     print(f"【content】\n{latest_message.content}")
        #     print(f"【tool_calls】\n{latest_message.tool_calls or None}")
        # elif isinstance(latest_message, ToolMessage):
        #     print(f"【content】\n{latest_message.content}")
        #     print(f"【name】\n{latest_message.name}")
        # elif isinstance(latest_message, HumanMessage):
        #     print(f"【content】\n{latest_message.content}")
        # else:
        #     print("未知类型")


        print("-----------------------------------")

    return


if __name__ == '__main__':
    test_agent_ReAct()