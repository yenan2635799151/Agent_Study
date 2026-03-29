from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import os

llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    ) 

@tool
def get_weather()->str:
    """
    查询明天西安的天气
    """
    str = "明天西安的天气是雨天，温度10-15度，建议带伞出门。"
    return str

agent = create_agent(
    model = llm,
    tools = [get_weather],
    system_prompt = "你是一个智能AI助手，需要使用工具回答用户的问题" #传参数为str或者systemMessage对象
)

res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"明天西安的天气怎么样？"}
        ]
    }
)

for msg in res["messages"]:
    print(type(msg).__name__,msg.content)