# langchain 实现RAG

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


### 一、初始化转换向量的模型
# """
#     embed_query: 转换单个文本
#     embed_documents: 转换多个文本
# """

# 阿里云千问embedding向量模型（api_key环境变量：DASHSCOPE_API_KEY）
embedding_model = DashScopeEmbeddings()

# Ollama本地部署模型 https://ollama.com/
# embedding_model = OllamaEmbeddings(model="qwen3-embedding:4b")

print(f"embedding_model: {embedding_model}")

# vector = embedding_model.embed_query("我喜欢你")
# print(f"vector: (向量维度={len(vector)}) {vector}")
#
# print((embedding_model.embed_documents(["我喜欢你", "wanfeng"])))

### 二、获取文档数据（Document类）
text_file = 'resources/Teyvathis.md';
text_loader = TextLoader(file_path=text_file, encoding='utf-8')
data = text_loader.load()
print(f'已读取文件: {text_file}')

# 分段
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=['\n\n', '\n', '。', '！', '？', ".", "!", "?", " "],
    length_function=len
)

docs = splitter.split_documents(data)
print(f'已分割段落：{len(docs)}')

### 二、初始化向量存储

# 初始化存储对象（内存）
# vector_store = InMemoryVectorStore(embedding=embedding_model)
# 初始化存储对象（chroma）
# Chroma
#   collection_name：指定名称
#   embedding_function: 使用的向量模型
#   persist_directory：存放文件夹
vector_store = Chroma(
    collection_name="Teyvathis",
    embedding_function=embedding_model,
    persist_directory="db/Teyvathis"
)

# 添加文档内容
#   ids：字符串数组，记录每个Document保存的id
#   documents: 文档数据（Document类型）
doc_ids = [str(index) for index, doc in enumerate(docs)]
print(f'doc_ids: {doc_ids}')
vector_store.add_documents(ids=doc_ids, documents=docs)

# 删除文档内容
delete_ids = ["1", "3"]
vector_store.delete(delete_ids)

# 检索文档（根据向量相似度匹配）
# similarity_search() -> list[Document]
#   query: 查询的文本
#   k：匹配数量
#   filter: 过滤Document中元数据的条件，搜索结果只返回符合条件的Document
search_res = vector_store.similarity_search(
    query="法涅斯",
    k=3,
    filter={ "source": 'resources/Teyvathis.md' }
)
print(f"检索结果：{search_res}")




