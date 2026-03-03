# src/embedding_client.py
import os
from zai import ZhipuAiClient
from dotenv import load_dotenv

load_dotenv()

class EmbeddingClient:
    def __init__(self):
        self.client = ZhipuAiClient(api_key=os.getenv("ZHIPU_API_KEY"))
        self.model_name = os.getenv("ZHIPU_EMBEDDING_MODEL", "embedding-2")

    def get_embedding(self, text: str) -> list:
        """
        获取文本向量
        返回：float 列表（1024 维）
        """
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text
            )
            # 智谱官方 SDK 返回结构
            return response.data[0].embedding
        except Exception as e:
            print(f"Embedding 调用失败：{e}")
            return []

    def get_batch_embeddings(self, texts: list) -> list:
        """
        批量获取向量（可选优化）
        一次最多传 256 条文本
        """
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"批量 Embedding 调用失败：{e}")
            return []