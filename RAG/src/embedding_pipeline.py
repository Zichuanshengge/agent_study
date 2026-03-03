# src/embedding_pipeline.py
from embedding_client import EmbeddingClient
from chunking import split_by_sections
from dataloader import load_data
import json
import time

def embed_all_documents():
    # 1. 初始化
    client = EmbeddingClient()
    all_chunks = []
    
    # 2. 加载数据
    docs = load_data("../data/genshin_impact_characters")
    
    print(f"开始处理 {len(docs)} 个文档...")
    
    # 3. 遍历文档
    for doc in docs:
        # 分片
        chunks = split_by_sections(doc['content'], doc['name'])
        print(f"文档 {doc['name']} 分成 {len(chunks)} 个章节")
        
        # 遍历每个 chunk 生成向量
        for chunk in chunks:
            print(f"  正在向量化：{chunk['metadata']['section']}...")
            
            # 调用 API
            vector = client.get_embedding(chunk['content'])
            
            if vector:
                # 验证向量维度
                if len(vector) != 1024:
                    print(f"  ⚠️ 警告：向量维度异常，实际为 {len(vector)} 维")
                chunk['vector'] = vector
                all_chunks.append(chunk)
            else:
                print("  跳过失败片段")
            
            # 避免触发频率限制
            time.sleep(0.3) 
    
    # 4. 保存结果
    with open("../data/embedded_chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 完成！共生成 {len(all_chunks)} 个向量片段，已保存。")

if __name__ == "__main__":
    embed_all_documents()