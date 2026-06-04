# AI私厨管家案例 LangSmith部署

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
web_search_tool = TavilySearch(
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

# 系统提示词
system_prompt = read_file_content('resources/prompt_cook_manager.md')
log.info(f'读取系统提示词 len={len(system_prompt)}')

# 智能体
# LangSmith 自动提供checkpointer，不要自己指定
personal_chief_agent = create_agent( 
    model=model, 
    system_prompt=system_prompt,
    tools=[ web_search_tool, current_time ],
)
log.info(f'智能体已创建: {personal_chief_agent}')
