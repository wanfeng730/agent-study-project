# langchain 文档加载器

from langchain_classic.document_loaders import PyPDFLoader, TextLoader
from langchain_community.document_loaders import CSVLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
不同的文档加载器都实现了统一的接口
    load() -> list[Document]：一次性加载文件所有内容
    lazy_load() -> Iterator[Document]：延迟流式传输文档，对大型数据集很有用，避免内存溢出
"""

### csv文件加载器
"""
CSVLoader
    file_path: 文件路径
    csv_args：读取csv数据的参数
        delimiter：分隔符
        quotechar：指定字符串的包裹字符
        fieldnames：字段列表（没有表头时指定，作为缺省值）
"""
def test_csv_loader():
    csv_loader = CSVLoader(
        file_path='resources/stu.csv',
        csv_args={
            'delimiter': ',',
            'quotechar': '"',
            'fieldnames': ['name', 'age'],
        }
    )
    print(f'csv_loader: {csv_loader}')

    csv_data = csv_loader.load()
    print(f'csv_data：{csv_data}')

    for document in csv_loader.lazy_load():
        print(f'csv_data(lazy): {document}')
    return

### json文件加载器
"""
需要jq依赖：uv add jq

JSONLoader
    file_path：文件路径
    jq_schema：读取的结构（jq语法）
    text_content：读取内容是否为字符串
    json_lines：文件的一行是否为一个独立的json对象
"""
def test_json_loader():
    json_loader = JSONLoader(
        file_path='resources/stu.json',
        jq_schema='.',
        text_content=False,
        json_lines=False
    )
    print(f'json_loader: {json_loader}')
    data = json_loader.load()
    print(f'data: {data}')

    json_loader = JSONLoader(
        file_path='resources/stu_arr.json',
        jq_schema='.[]',
        text_content=False,
        json_lines=False
    )
    print(f'json_loader: {json_loader}')
    data = json_loader.load()
    print(f'data: {data}')
    return

### txt文档加载器、文本分段分割器
"""
TextLoader
    file_path: 文件路径
    encoding: 编码

RecursiveCharacterTextSplitter
    chunk_size：分段的最大字符数
    chunk_overlap： 允许分段之间重叠的字符数
    separators：段落分割符号
    length_function：用于统计字符的依据函数（一般使用len函数即可）
"""
def test_text_loader_splitter():
    loader = TextLoader(
        file_path='resources/Teyvathis.md',
        encoding='utf-8',
    )
    data = loader.load()
    print(f'data: {data}')

    # 文档分段分割器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=['\n\n', '\n', '。', '！', '？', ".", "!", "?", " "],
        length_function=len
    )

    docs = splitter.split_documents(data)
    for doc in docs:
        print(f'{doc}')
        print()
    return

### pdf文件加载器
"""
需要pypdf依赖：uv add pypdf

PyPDFLoader
    file_path: 文件路径
    mode：读取模式
        - single：单个document
        - page: 按页划分，多个document
    password：文件密码
"""
def test_pdf_loader():
    pdf_loader = PyPDFLoader(
        file_path="resources/RMRB-20240126.pdf",
        mode="page",
        password=None
    )
    print(f'pdf_loader: {pdf_loader}')

    docs = pdf_loader.lazy_load()
    for doc in docs:
        print()
        print(f'doc: {doc}')
    return

# test_text_loader_splitter()
test_pdf_loader()