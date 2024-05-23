from langchain.tools import BaseTool
from langchain.agents import load_tools, initialize_agent,AgentType
class category_classification(BaseTool):
    name = "account_classification_tool"
    description = (
        """
        這是帳目分類器，請從使用者類別和使用者輸入找出下面的 parameter ["金額","地點","類別"]
        "類別"：一定要輸出一個類別，只能由使用者類別中做選擇，請盡量用category_description做判斷
        "地點"：若無法判斷則輸出空字串
        "金額"：若無法判斷則輸出0
        """
    )

    def _run(self,
            金額: int = None,
            地點: str = None,
            類別: str = None,
             ):

        return(f"金額:{金額}，地點：{地點}，類別：{類別}，請把這些文字轉成JSON格式")


def get_category_classification_tool(llm):
    tools = [category_classification()]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True)



def create_item_name_tool(llm):
    tools = [create_item_name()]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True)

class create_item_name(BaseTool):
    name = "create_item_name_tool"
    description = (
        """
        這是帳目名稱生成器，請根據使用者輸入，生成合適的帳目名稱，盡量簡潔且涵蓋所有帳目需要的資訊
        """
    )

    def _run(self):

        return(f"金額:{金額}，地點：{地點}，類別：{類別}，請把這些文字轉成JSON格式")