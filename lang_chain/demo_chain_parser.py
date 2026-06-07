# chain 链式调用、parser 格式转换器

from typing import Any, Dict

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AIMessageChunk, HumanMessage, SystemMessage
from langchain_classic.prompts import MessagesPlaceholder
from langchain_classic.schema import StrOutputParser
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from init_chat_models import *

model = model_qwen_plus()
print(f'初始化模型：{model}')


def test_chain():
    prompt_template = PromptTemplate.from_template(
        '我姓{last_name}，刚生了个{gender}，帮我起3个名字，只返回名字并用逗号分隔。'
    )

    # StrOutputParser是langchain内置的简单字符串解析器，可以作为组件将AIMessage转为str
    parser = StrOutputParser()
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
    


print('开始测试')
# test_chain()
test_chain_fill_prompt_template()