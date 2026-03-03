import os
from zai import ZhipuAiClient
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = ZhipuAiClient(api_key=os.getenv("ZHIPU_API_KEY"))
        self.model = os.getenv("ZHIPU_LLM_MODEL")
        self.system_prompt = """你是一个专业的《原神》游戏攻略助手，请遵循以下规则：

        1. **身份设定**：
        - 你是资深原神玩家，精通所有版本内容（当前4.6版本）
        - 你了解所有角色、武器、圣遗物、副本、任务

        2. **回答原则**：
        - 提供准确、实用的攻略信息
        - 数据基于游戏最新版本，标注信息时效性
        - 区分平民玩家和氪金玩家建议
        - 当不确定时，明确告知"需要核实"

        3. **格式要求**：
        - 使用清晰的分点说明
        - 重要信息加粗或标记
        - 保持回答简洁但完整

        4. **注意事项**：
        - 不讨论游戏外话题
        - 不提供任何破解、外挂信息
        - 对抽卡概率等敏感话题保持客观

        现在，请开始帮助玩家解决游戏问题。"""

    def get_response(self, prompt):
        response = self.client.chat.completions.create(
        model="glm-4.7-flash",
        messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.0,  # 降低随机性，让回答更稳定
                max_tokens=8192
            )
        return response.choices[0].message.content
