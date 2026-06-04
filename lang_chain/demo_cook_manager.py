# AI私厨管家案例    
# 自动识别图片中的食材，根据食材联网搜索相关食谱推荐给用户
# 需要存储对话记忆吗？

import base64
import sqlite3
import logging as log
from typing import Any, Literal, cast
from dotenv import load_dotenv
import os, sys

from langchain.tools import tool
from langchain.messages import AIMessageChunk, HumanMessage, ImageContentBlock
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.agents.middleware import SummarizationMiddleware

# 添加项目根目录（python_base 的父目录）到 Python 路径  os.path.dirname(...) 获取上级目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model

# 自定义模块
from python_base import init_logging, image_to_base64_url
from python_base.date_util import *

# 读取文件内容
def read_file_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content;

# 加载环境变量
load_dotenv()
# 初始化日志配置
log = init_logging(log_file='logs/demo_cook_manager.log')


# 初始化模型
model = init_chat_model(
    model='qwen3.7-plus',
    model_provider='openai',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    api_key=os.getenv('DASHSCOPE_API_KEY'),

    temperature=1.5,
    max_tokens=4096,
    top_p=0.9,
    timeout=60,
    max_retries=2,
    extra_body={
        'enable_thinking': False
    }
)
log.info(f'模型已初始化：{model}')

# 工具：Tavily网页搜索
search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

# 工具：获取当前时间
@tool
def current_time() -> str:
    """获取当前时间（北京时间）

    Returns:
        str: 年月日时分秒
    """
    return get_current_date_time_cn()
    

# 总结摘要中间件    trigger 触发条件、keep 需要保持的状态
summarization_middileware = SummarizationMiddleware(
    model=model,
    trigger=('tokens', 600),
    keep=('messages', 20)
)

# 初始化sqlite连接  check_same_thread=False：关闭同一线程检查防止报错
sqlite_connection = sqlite3.connect('resources/db/demo_cook_manager.db', check_same_thread=False)
sqlite_checkpointer = SqliteSaver(sqlite_connection)
sqlite_checkpointer.setup()

# 系统提示词
system_prompt = read_file_content('resources/prompt_cook_manager.md')
log.info(f'读取系统提示词 len={len(system_prompt)}')



# 智能体
agent = create_agent( 
    model=model, 
    system_prompt=system_prompt,
    tools=[ search_tool, current_time ],
    checkpointer=sqlite_checkpointer,
    middleware=[summarization_middileware]
)
log.info(f'智能体已创建: {agent}')


# 配置会话id
invoke_config = {"configurable": {"thread_id": "06021017"}}

# 调用测试
def test_stream_has_image(user_query: str, image_path: str):
    image_url = image_to_base64_url(image_path)

    human_message = HumanMessage(content=[
        {
            "type": "image_url", # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
            "image_url": {"url": image_url},
        },
        {
            "type": "text",
            "text": user_query, # <-- 使用 text 类型来提供文字指令，例如"描述图片内容"
        },
    ])

    res = agent.stream({
        'messages': [
            human_message
        ]
    }, stream_mode='messages', config=invoke_config)

    log.info('test_stream_has_image 智能体调用返回')
    for data in res:
        # chunk 通常是 (AIMessageChunk, metadata) 元组
        chunk: AIMessageChunk = data[0]
        metadata = data[1]
        # 模型返回内容
        content = str(chunk.content) if chunk.content else ''

        # 空字符串
        if not content:
            continue
        # json数据，工具调用结果
        if content.startswith('{') and content.endswith('}'):
            log.info(f'智能体工具调用\n{content}')
            continue
        # 模型回答结果
        print(content, end='', flush=True)
    
    return

def test_invoke(user_query: str, image_path: str | None = None):
    human_message = HumanMessage(content=user_query)
    if image_path:
        image_url = image_to_base64_url(image_path)
        human_message = HumanMessage(content=[
            {
                "type": "image_url", # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
                "image_url": {"url": image_url},
            },
            {
                "type": "text",
                "text": user_query, # <-- 使用 text 类型来提供文字指令，例如"描述图片内容"
            },
        ])

    res = agent.invoke({
        'messages': [
            human_message
        ]
    }, config=invoke_config)

    log.info('test_invoke_has_image 智能体调用返回')
    for message in res['messages']:
        message.pretty_print()
    
    return


# test_invoke_has_image('帮我推荐几个简单好吃的食谱', 'resources/cook_manager_2.jpg')
test_invoke('我喜欢第2道菜，帮我搜索一下它的参考图并提供链接')