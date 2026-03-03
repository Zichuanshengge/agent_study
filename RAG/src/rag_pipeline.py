# src/rag_pipeline.py
from embedding_client import EmbeddingClient
from vector_store import VectorStore
from llm_client import LLMClient

class RAGPipeline:
    def __init__(self):
        self.emb_client = EmbeddingClient()
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
    
    def build_prompt(self, context: str, question: str) -> str:
        """
        构建 Prompt
        """
        prompt = f"""你是一个原神游戏攻略助手。
请根据以下【参考资料】回答用户问题。

回答要求：
1. 优先基于【参考资料】中的信息回答
2. 如果资料中没有直接答案，可以基于已有信息进行合理分析和推断
3. 如果确实无法回答，请说明原因，并给出可能的建议
4. 回答时请注明来源（角色名 - 章节名）
回答时请注明来源（角色名 - 章节名）。

【参考资料】：
{context}

用户问题：
{question}

回答：
"""
        return prompt
    
    def query(self, question: str, top_k=3):
        """
        完整 RAG 流程
        """
        print(f"🔍 用户问题：{question}\n")
        
        # 1. 问题向量化
        query_vector = self.emb_client.get_embedding(question)
        if not query_vector:
            return "Embedding 生成失败"
        
        # 2. 检索
        results = self.vector_store.search(query_vector, top_k=top_k)
        
        # 3. 构建上下文
        context_parts = []
        sources = []
        if results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                # 只取前 500 字，避免超出 LLM 上下文限制
                context_parts.append(f"[{meta['character']} - {meta['section']}]\n{doc[:500]}")
                sources.append(f"{meta['character']} - {meta['section']}")
        
        context = "\n\n".join(context_parts)
        
        if not context:
            return "未检索到相关资料"
        
        # 4. 生成答案
        prompt = self.build_prompt(context, question)
        answer = self.llm_client.get_response(prompt)
        
        # 5. 输出结果
        print(f"📚 参考来源：{', '.join(sources)}\n")
        print(f"🤖 AI 回答：\n{answer}\n")
        
        return answer

if __name__ == "__main__":
    pipeline = RAGPipeline()
    
    # 测试问题 1
    # pipeline.query("兹白适合什么队伍？")
    
    # 测试问题 2
    # pipeline.query("哥伦比娅用什么武器最好？")
    
    # 测试问题 3（边界测试，资料里没有的）
    pipeline.query("兹白和哥伦比娅谁更强？")