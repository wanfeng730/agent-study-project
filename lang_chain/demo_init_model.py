# 加载环境变量
from dotenv import load_dotenv
import os
load_dotenv()


from langchain.chat_models import init_chat_model
from langchain_community.chat_models.tongyi import ChatTongyi

# （1）根据模型名称自动判断模型并设定base_url，从环境变量中获取api_key
model = init_chat_model(model='deepseek-v4-pro')

# （2）如果langchain没有集成但是兼容了OpenAI的规范，则需要手动设置参数（伪装）
# model = init_chat_model(
#     model='kimi-k2.6',
#     model_provider='openai',
#     base_url='https://api.moonshot.cn/v1',
#     api_key=os.getenv('API_KEY_KIMI')
# )

# （3）从langchain的社区包中寻找模型类，例如通义千问
# 官方文档：https://reference.langchain.com/python/langchain-community/chat-models
# model = ChatTongyi(model='qwen-max')

"""
模型参数设置
    temperature：控制生成文本的随机性，值越大范围越大（一般为0~2的小数）
    max_tokens: 控制生成文本的最大token数
    top_p: 控制生成文本的多样性,值越小越多样，值越大越确定
    timeout：控制生成文本的超时时间
    max_retries: 控制生成文本的最大重试次数
    ...
"""
print(f'模型已初始化：{type(model)}')
