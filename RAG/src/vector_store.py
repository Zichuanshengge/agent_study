# src/vector_store.py
import chromadb
from chromadb.config import Settings
import json
import os

class VectorStore:
    def __init__(self, persist_directory="../data/chroma_db"):
        # 1. 初始化客户端（设置持久化路径）
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            is_persistent=True  # 确保数据保存
        ))
        
        # 2. 创建或获取 Collection
        # metadata 用于记录向量维度等信息
        self.collection = self.client.get_or_create_collection(
            name="genshin_guides",
            metadata={"embedding_function": "zhipu-embedding-2"} 
        )
    
    def add_chunks(self, chunks):
        """
        将分片数据存入向量库
        chunks 格式：[{'content': ..., 'metadata': {...}, 'vector': [...]}, ...]
        """
        # Chroma 需要分开传 ids, documents, metadatas, embeddings
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = [chunk['content'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        embeddings = [chunk['vector'] for chunk in chunks]
        
        # 清空旧数据（避免重复添加）
        results = self.collection.get()
        if results['ids']:
            self.collection.delete(ids=results['ids'])
        
        # 添加数据
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        print(f"✅ 已成功存入 {len(chunks)} 个向量片段")
    
    def search(self, query_vector, top_k=3):
        """
        相似度搜索
        返回：最相似的 top_k 个片段
        """
        results = self.collection.query(
            query_embeddings=[query_vector],  # 注意：需要嵌套列表
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        return results

if __name__ == "__main__":
    # 测试：加载数据并存入
    with open("../data/embedded_chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    
    store = VectorStore()
    store.add_chunks(chunks)
    print("向量库初始化完成！")