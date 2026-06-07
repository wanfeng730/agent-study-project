# chain 链式调用、parser 格式转换器

from typing import Any, Dict

from dotenv import load_dotenv

from fsspec.config import conf
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AIMessageChunk, HumanMessage, SystemMessage
from langchain_classic.prompts import MessagesPlaceholder
from langchain_classic.schema import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory

from init_chat_models import *

model = model_qwen_plus()
print(f'初始化模型：{model}')

### 链式调用、格式转换
"""
    StrOutputParser：简单字符串解析器，可以作为组件将AIMessage转为str
    JsonOutputParser：json解析器，可以作为组件将AIMessage转为dict
"""
def test_chain():
    prompt_template = PromptTemplate.from_template(
        '我姓{last_name}，刚生了个{gender}，帮我起3个名字，只返回名字并用逗号分隔。'
    )

    # 
    parser = StrOutputParser()
    # 是langchain内置的
    chain = prompt_template | model | parser | model

    # input是一个字典，定义第一个节点调用时的参数，key为参数名，value为参数值
    # prompt_template.format(last_name='骆', gender='女儿')
    res = chain.invoke(input={'last_name': '骆', 'gender': '女儿'})
    print(f'test_chain 调用结果\n{res}')





# 将模型返回的结果处理成自定义的dict
def process_name_to_json(message: AIMessage) -> dict:
    print(f'执行process_name_to_json message={message}');
    return {
        'input_names': message.content
    }

# 自定义类继承BaseOutputParser方法
class ProcessNameOutputParser(BaseOutputParser[Dict[str, Any]]):
    # 实现parse方法（text是模型结果的content内容，有langchain自动提取）
    def parse(self, text) -> Dict[str, Any]:
        return {
            'input_names': text
        }

### 链式调用、自定义格式转换
"""
实现自定义格式转换的方法
    1. RunnableLambda(function)
        自定义一个function，将AIMessage转换成想要的类型，并用RunnableLambda封装成链的一个节点
    2. class CustomOutputParser(BaseOutputParser[T])
        继承BaseOutputParser类，重写parse方法
        T为泛型，指定返回的类型

"""
def test_chain_fill_prompt_template():
    prompt_template = PromptTemplate.from_template(
        '我姓{last_name}，刚生了个{gender}，帮我起3个名字，只返回名字并用逗号分隔。'
    )

    # RunnableLambda封装自定义函数组件，可以实现链式调用中的模版填充
    process_name_runnable = RunnableLambda(process_name_to_json)

    prompt_template2 = PromptTemplate.from_template(
        '帮我分析“{input_names}”这几个名字怎么样，从多个角度分析'
    )
    # chain = prompt_template | model | process_name_runnable | prompt_template2 | model
    chain = prompt_template | model | ProcessNameOutputParser() | prompt_template2 | model

    # res = chain.invoke(input={'last_name': '骆', 'gender': '女儿'})
    # print(f'test_chain_fill_prompt_template 调用结果\n{res}')

    res = chain.stream(input={'last_name': '骆', 'gender': '女儿'})
    print('test_chain_fill_prompt_template 调用结果')
    for message in res:
        if message.content:
            print(message.content, end='', flush=True)

    return




chain_historys = {}

def get_chain_history_in_memory(session_id: str):
    if session_id not in chain_historys:
        chain_historys[session_id] = InMemoryChatMessageHistory()
    return chain_historys[session_id]


### 链式调用、带历史记录
"""
RunnableWithMessageHistory 参数说明
    runnable：原链
    get_session_history：获取会话历史记录的函数
    input_messages_key：用户输入的占位符名称
    history_messages_key：填充历史消息的占位符名称
"""
def test_chain_with_history():
    prompt_template = PromptTemplate.from_template(
        '你需要根据对话历史回答用户问题。对话历史：{history_messages}。用户问题：{user_query}。回答要简洁'
    )
    # 链
    chain = prompt_template | model | StrOutputParser()
    # 封装成带有历史记录功能的链
    conversation_chain = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_chain_history_in_memory,
        input_messages_key='user_query',
        history_messages_key='history_messages'
    )
    # 定义会话id
    config = { 'configurable': { 'session_id': 'user001' }}

    res = conversation_chain.invoke({"user_query": '帮我的女儿起一个好听的名字，姓氏为骆，只回答名字和简要含义即可'}, config=config)
    print(f'test_chain_with_history 模型返回：{res}')
    res = conversation_chain.invoke({"user_query": '再想一个其他风格的名字'}, config=config)
    print(f'test_chain_with_history 模型返回：{res}')
    res = conversation_chain.invoke({"user_query": '对比一下这两个名字'}, config=config)
    print(f'test_chain_with_history 模型返回：{res}')

    return


print('开始测试')
# test_chain()
# test_chain_fill_prompt_template()
test_chain_with_history()