# Kimi 大模型API调用

# uv add openai

from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载.env文件到环境变量中
load_dotenv()

# 获取环境变量
base_url = 'https://api.moonshot.cn/v1'
api_key = os.getenv('API_KEY_KIMI')

client = OpenAI(api_key=api_key, base_url=base_url)

completion = client.chat.completions.create(
    model='kimi-k2.6',
    messages=[
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，我是晚风，一名Agent开发工程师，你是什么模型？"}
    ]
)

print(completion.choices[0].message.content)