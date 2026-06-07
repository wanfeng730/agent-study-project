from dotenv import load_dotenv
import os
load_dotenv()

from langchain.chat_models import BaseChatModel, init_chat_model


def model_qwen_plus() -> BaseChatModel:
    return init_chat_model(
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


def model_deepseek_v4_pro() -> BaseChatModel:
    return init_chat_model(
        model='deepseek-v4-pro', 
        # ----- 透传参数 **kwargs -----
        temperature=1.5,      
        max_tokens=4096,
        top_p=0.9,
        timeout=60,
        max_retries=2,
        extra_body={"thinking": {"type": "disabled"}} # DeepSeek模型禁用思考模式
    )

def model_kimi_k2_6() -> BaseChatModel:
    return init_chat_model(
        model='kimi-k2.6',
        model_provider='openai',
        base_url='https://api.moonshot.cn/v1',
        api_key=os.getenv('API_KEY_KIMI'),

        temperature=1.5,      
        max_tokens=4096,
        top_p=0.9,
        timeout=60,
        max_retries=2,
    )