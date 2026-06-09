import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "120"


from typing import List
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import chromadb

# 加载embedding模型
embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese");

# 向量数据库(在内存中)
db_client = chromadb.EphemeralClient();
db_collection = db_client.get_or_create_collection(name="default");

# CrossEncoder模型
cross_encoder = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-V1')

# 分片
def split_chunks(doc_file_path: str) -> List[str]:
    with open(doc_file_path, 'r') as file:
            content = file.read()
    return [chunk for chunk in content.split("\n\n")]

# 索引：计算片段的向量值
def to_vector(chunk: str) -> List[float]:
    embed_vectors = embedding_model.encode(chunk)
    return embed_vectors.tolist()

# 保存到向量数据库
def save_vector_to_db(chunks: List[str], vectors: List[List[float]]) -> None:
    ids = [str(i) for i in range(len(chunks))]
    db_collection.add(documents=chunks, embeddings=vectors, ids=ids)

# 召回，寻找与用户提示词匹配度高的片段
def retrive(user_prompt: str, max_count: int) -> List[str]:
    user_prompt_vector = to_vector(user_prompt)
    match_results = db_collection.query(query_embeddings=[user_prompt_vector], n_results=max_count)
    return match_results['documents'][0]

# 重排
def rerank(user_prompt: str, retrive_chunks: List[str], max_count: int) -> List[str]:
    # 列表中的元素为用户提问和每一个片段
    match_list = [(user_prompt, chunk) for chunk in retrive_chunks]
    # 使用模型计算为每一个提问片段组合打分（提问和片段的相似度）
    scores = cross_encoder.predict(match_list)
    # 组合片段对应的分数
    chunk_scores = [(chunk, score) for chunk, score in zip(retrive_chunks, scores)]
    # 按分数倒序排序
    chunk_scores.sort(key = lambda item: item[1], reverse=True)
    # 取前max_count个结果
    return [chunk for chunk, score in chunk_scores][:max_count];


       

def main():

    # 对内容分片
    chunks = split_chunks("resources/news_1.md")
    # 计算向量
    chunk_vectors = [to_vector(chunk) for chunk in chunks];
    # 保存向量到数据库
    save_vector_to_db(chunks, chunk_vectors);

    # 用户提问
    user_query = '本次中俄会晤中，俄方出席了哪些人员？'
    # 查询匹配度高的5个片段
    retrive_chunks = retrive(user_query, 5)

    rerank_chunks = rerank(user_query, retrive_chunks, 2)

    for i, chunk in enumerate(rerank_chunks):
        print(f"[{i}] {chunk}\n")
        

    



if __name__ == "__main__":
    main()








