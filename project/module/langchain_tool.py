from langchain.tools import BaseTool
from langchain.agents import load_tools, initialize_agent,AgentType
class account_classification(BaseTool):
    name = "account_classification_tool"
    description = (
        """
        這是帳目分類器，請從使用者類別和使用者輸入找出下面的 parameter ["金額", "地點", "類別","時間"]
        """
    )

    def _run(self,
            金額: int = None,
            地點: str = None,
            類別: str = None,
            時間: str = None,
             ):
        if 金額 and 地點 and 類別:
            print(f"金額:{金額}，地點：{地點}，類別：{類別}，時間：{時間}")
        else:
            return "解析不出金額、地點、類別，請再試一次。"



