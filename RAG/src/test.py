# src/test_retrieval.py
from embedding_client import EmbeddingClient
from vector_store import VectorStore
import json

def test_retrieval(query_text):
    # 1. 初始化
    emb_client = EmbeddingClient()
    store = VectorStore()
    
    # 2. 将用户问题转化为向量
    print(f"用户问题：{query_text}")
    query_vector = emb_client.get_embedding(query_text)
    
    if not query_vector:
        print("Embedding 生成失败")
        return
    
    # 3. 检索最相似的 3 个片段
    results = store.search(query_vector, top_k=3)
    
    # 4. 打印结果
    print(f"\n🔍 找到 {len(results['documents'][0])} 个相关片段：\n")
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        dist = results['distances'][0][i]
        print(f"--- 片段 {i+1} (距离：{dist:.4f}) ---")
        print(f"来源：{meta['character']} - {meta['section']}")
        print(f"内容：{doc[:100]}...\n")

if __name__ == "__main__":
    # 测试问题 1：关于哥伦比娅的武器
    test_retrieval("哥伦比娅用什么武器最好？")
    
    # 测试问题 2：关于兹白的配队
    test_retrieval("兹白适合什么队伍？")