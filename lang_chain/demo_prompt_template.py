from dotenv import load_dotenv
import os

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_classic.prompts import MessagesPlaceholder
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate
# 加载环境变量
load_dotenv()

model = init_chat_model(
    model='qwen-plus',
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

print(f'模型已初始化：{type(model)}')


### 通用提示词模版 PromptTemplate
def test_prompt_template():
    # 定义模版，变量处用占位符
    prompt_template = PromptTemplate.from_template(
        '我的邻居姓{last_name}，刚生了个{gender}，帮我起一个名字，简单回答。'
    )
    
    # 链式调用（参数传递给第一个节点、执行结果再传递给第二个节点，依此类推）
    chain = prompt_template | model

    # input是一个字典，定义第一个节点调用时的参数，key为参数名，value为参数值
    # prompt_template.format(last_name='骆', gender='女儿')
    res = chain.invoke(input={'last_name': '骆', 'gender': '女儿'})
    print(f'test_prompt_template 模型调用结果：{res}')
    return


### 示例提示词模版 FewShotPromptTemplate
"""
prefix: 示例前的提示词
example_prompt：示例文本的格式化（PromptTemplate）
examples：填充的示例数据（list<dict>）
suffix：示例后的提示词
input_variables：提问时的格式化占位变量名
"""
def test_few_shot_prompt_template():
    example_prompt = PromptTemplate.from_template('{word}的反义词是{antonym}')
    example_data = [
        { 'word': '大', 'antonym': '小'},
        { 'word': '美丽', 'antonym': '丑陋'},
    ]

    template = FewShotPromptTemplate(
        prefix='判断一个词的反义词，有如下示例：',
        example_prompt=example_prompt,
        examples=example_data,
        suffix='基于示例帮我推断：{input_word}的反义词是什么？',
        input_variables=['input_word']
    )

    prompt = template.invoke(input={'input_word': '左'}).to_string()
    print(f'test_few_shot_prompt_template 提示词: \n{prompt}')
    return

### 聊天提示词模版 ChatPromptTemplate
'''
ChatPromptTemplate.from_messages()
    参数为消息列表

MessagesPlaceholder('hisotry_messages') 
    消息内容占位，hisotry_messages为自定义占位变量名

template.invoke(input={'history_messages': history_messages})
    在填充模版时填充占位数据（可变消息列表）
'''
def test_chat_prompt_template():
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage('系统提示词内容'),
            AIMessage('AI消息内容'),
            MessagesPlaceholder('history_messages'),
            HumanMessage('用户消息内容')
        ]
    )
    history_messages = [
        HumanMessage('...'),
        AIMessage('...')
    ]
    prompt_value = template.invoke(input={'history_messages': history_messages})
    print(f'聊天提示词：\n{prompt_value.to_string()}')
    return

print('开始测试...')
test_chat_prompt_template()
# test_few_shot_prompt_template()
# test_prompt_template()