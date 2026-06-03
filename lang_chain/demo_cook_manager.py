# AI私厨管家案例    
# 自动识别图片中的食材，根据食材联网搜索相关食谱推荐给用户
# 需要存储对话记忆吗？

import base64
import sqlite3
import logging as log
from typing import Any, Literal, cast
from dotenv import load_dotenv
import os, sys

from langchain.messages import HumanMessage, ImageContentBlock

# 添加项目根目录（python_base 的父目录）到 Python 路径  os.path.dirname(...) 获取上级目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model

# 自定义模块
from python_base import init_logging, image_to_base64_url

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
    model='kimi-k2.6',
    model_provider='openai',
    base_url='https://api.moonshot.cn/v1',
    api_key=os.getenv('API_KEY_KIMI'),
)
log.info(f'模型已初始化：{type(model)}')

# 工具：Tavily网页搜索
search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

# 初始化sqlite连接  check_same_thread=False：关闭同一线程检查防止报错
# sqlite_connection = sqlite3.connect('resources/db/demo_cook_manager.db', check_same_thread=False)
# sqlite_checkpointer = SqliteSaver(sqlite_connection)
# sqlite_checkpointer.setup()

# 系统提示词
system_prompt = read_file_content('resources/prompt_cook_manager.md')
log.info(f'读取系统提示词 len={len(system_prompt)}')

# 智能体
agent = create_agent( 
    model=model, 
    system_prompt=system_prompt,
    tools=[
        search_tool
    ],
)
log.info(f'智能体已创建: {type(agent)}')


# 调用测试
user_query = '我现在冰箱里有豆腐、紫菜、鸡蛋、黄瓜、皮蛋，还有半盒牛奶、一小瓶老干妈辣椒酱'
image_url = image_to_base64_url('')

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

agent.invoke({
    'messages': [
        human_message
    ]
})