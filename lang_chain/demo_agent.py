import base64
from re import M
from typing import Literal, cast
from attr import field
from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
import langchain

from langchain_core.globals import set_debug
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_community.chat_models.tongyi import ChatTongyi
from pydantic_core import to_json
from torch.cuda import temperature

# 读取文件内容
def read_file_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content;

# 开启langchain调试模式，会在控制台打印完整的 API 请求体
# set_debug(True)

# 加载环境变量
load_dotenv()

### 一、初始化模型
"""
三种方式
（1）根据模型名称自动判断模型并设定base_url，从环境变量中获取api_key
（2）如果langchain没有集成但是兼容了OpenAI的规范，则需要手动设置参数（伪装）
（3）从langchain的社区包中寻找模型类，例如通义千问（官方文档：https://reference.langchain.com/python/langchain-community/chat-models）

模型参数设置
    temperature：控制生成文本的随机性，值越大范围越大（一般为0~2的小数）
    max_tokens: 控制生成文本的最大token数
    top_p: 控制生成文本的多样性,值越小越多样，值越大越确定
    timeout：控制生成文本的超时时间
    max_retries: 控制生成文本的最大重试次数
    ...
"""
# model = init_chat_model(model='deepseek-v4-pro')
model = init_chat_model(
    model='deepseek-v4-pro', 
    # ----- 透传参数 **kwargs -----
    temperature=1.5,      
    max_tokens=4096,
    top_p=0.9,
    timeout=60,
    max_retries=2,
    extra_body={"thinking": {"type": "disabled"}} # DeepSeek模型禁用思考模式
)
# model = init_chat_model(
#     model='kimi-k2.6',
#     model_provider='openai',
#     base_url='https://api.moonshot.cn/v1',
#     api_key=os.getenv('API_KEY_KIMI'),
# )
# model = ChatTongyi(model='qwen-max')
print(f'模型已初始化：{type(model)}')




### 二、定义工具函数
"""
自定义工具函数
    函数名需直接指明作用，以便模型推理
    函数的doc注释详细描述作用，参数说明
    
    （1）根据docstring描述函数用途
    （2）使用pydantic描述函数用途
        Field：字段说明
        Literal：限定取值枚举

LangChain内置工具
    官方文档：https://docs.langchain.com/oss/python/integrations/tools
    （1）内置工具可能包含大量未使用的参数描述，造成token浪费。解决：可以使用自定义的tool封装内置工具调用，减少参数描述
"""
@tool
def get_weather(location: str) -> str:
    """根据地区名获取当前天气描述

    Args:
        location (str): 地区名

    Returns:
        str: 天气描述
    """
    print(f'调用工具 get_weather location={location}')
    return f'Current weather in {location} is sunny'

# 使用pydantic描述定义函数参数信息
class WeatherInfo(BaseModel):
    location: str = Field(description="地区名")
    temperature_unit: Literal["摄氏度","华氏度"] = Field(description='温度单位', default="摄氏度")
    is_include_humidity: bool = Field(description='是否查询湿度', default=False)

# 在tool函数中绑定定义的函数参数信息
@tool(args_schema=WeatherInfo)
def get_weather_better(location: str, temperature_unit: str = "摄氏度", is_include_humidity: bool = False) -> str:
    """获取某个地区的详细信息
    """
    tem = 28 if temperature_unit == '摄氏度' else 78
    result = f'{location} 现在的天气是晴天, 温度为{tem}{temperature_unit}'
    if is_include_humidity:
        result += ', 湿度为67%'
    return result;

# langchain内置工具 Tavily网页搜索
search_tool = TavilySearch(
    max_results=5,
    topic="general",
)
    
        



### 三、创建智能体对象
"""
Args：
    model           已初始化的模型对象 / langchain兼容的模型名称
    tools           可用的工具函数
    system_prompt   设定Agent统一使用的系统提示词，在调用时会将提示词发送给模型（SystemMessage）
    response_format 结构化输出的类
        - 若设定了此参数，langchain调用模型时会添加参数 tool_choice: "required"，可能会与模型的思考模式冲突
"""
class GlbyAnswerInfo(BaseModel):
    date: str
    weather: str
    feeling: int
    content: str

system_prompt = read_file_content('resources/prompt_glby.md')
print(f'系统提示词：\n{system_prompt}\n')
# agent = create_agent(model='deepseek-v4-pro', tools=[get_weather])
agent = create_agent(
    model=model, 
    system_prompt=system_prompt,
    response_format=GlbyAnswerInfo,
    tools=[
        get_weather_better
    ]
)
print(f'智能体对象已创建: {type(agent)}')



### 四、调用Agent
"""
（1）invoke(input) 阻塞式返回
（2）stream(input, stream_mode) 流式返回

可以使用BaseMessage的子类来封装传递不同角色的消息内容：AIMessage, HumanMessage, SystemMessage
"""
def test_invoke1():
    res = agent.invoke({
        "messages": [
            {"role": "user", "content": "你是谁?"}
        ]
    })
    print(f'智能体对象已调用 结果：{res}')

def test_stream():
    res = agent.stream({
        "messages": [
            {"role": "user", "content": "你是谁?"}
        ]
    }, stream_mode='messages')
    print(f'模型调用返回：{type(res)}')
    for token, metadata in res:
        if token.content:
            print(token.content, end='', flush=True)

def test_stream(query: str):
    res = agent.stream({
        "messages": [
            {"role": "user", "content": query}
        ]
    }, stream_mode='messages')
    print(f'模型调用返回：{type(res)}')
    for token, metadata in res:
        if token.content:
            print(token.content, end='', flush=True)

def test_invoke2():
    res = agent.invoke({
        "messages":[
            SystemMessage('请使用工具来获取天气信息'),
            HumanMessage('你好我是晚风'),
            AIMessage('你好，晚风，很高兴认识你'),
            HumanMessage('请介绍一下你自己，并帮我看下杭州今天的天气如何')
        ]
    })
    for message in res['messages']:
        message.pretty_print()

def test_invoke_image():
    # 多模态消息：图片（需要模型支持多模态，以kimi模型为例，官方文档：https://platform.kimi.com/docs/guide/kimi-k2-6-quickstart）
    image_path = 'resources/shot1.jpg';
    with open(image_path, "rb") as f:
        image_data = f.read()
    # 使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
    image_url = f"data:image/{os.path.splitext(image_path)[1].lstrip('.')};base64,{base64.b64encode(image_data).decode('utf-8')}"
    # print(f'读取图片转换的url：{image_url}')
    image_message = HumanMessage(content=[
        {
            "type": "image_url", # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
            "image_url": {
                "url": image_url,
            },
        },
        {
            "type": "text",
            "text": "请描述图片的内容。", # <-- 使用 text 类型来提供文字指令，例如"描述图片内容"
        },
    ])
    res = agent.stream(
        { "messages": [image_message]},
        stream_mode='messages'
    )
    for token, metadata in res:
        if token.content:
            print(token.content, end='', flush=True)

def test_invoke_structured_response_glby(query: str):

    res = agent.invoke({
        "messages":[
            HumanMessage(query)
        ]
    })
    for message in res['messages']:
        message.pretty_print()
    print()
    # answer = res['structured_response']
    # 可以使用强制转换定义类型
    answer = cast(GlbyAnswerInfo, res['structured_response'])
    print(f'已解析模型结构化输出: \n  当前心情值为{answer.feeling}\n  她说：{answer.content}')


def test_stream_memory(query: str):
    res = agent.stream({
        "messages": [
            {"role": "user", "content": query}
        ]
    }, stream_mode='messages')
    # print(f'模型调用返回：{type(res)}')
    # 流式输出回答
    for token, metadata in res:
        if token.content:
            print(token.content, end='', flush=True)


print('开始智能体对象调用...')
# test_invoke_structured_response_glby('我今天心情不好，你今天过得怎么样')
# print(f'搜索工具测试：{search_tool.invoke("凑企鹅是什么梗？")}')

test_invoke_structured_response_glby('咕咕嘎嘎这个梗是什么意思？')


