from langchain.agents import  create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    ) 

@tool
def get_price(name:str)->str:
    """
    查询股票的价格,传入股票名称，返回价格信息
    """
    return f"股票{name}的架构为20元"

@tool 
def get_info(name:str)->str:
    """
    查询股票的相关信息，传入股票名称，返回相关信息
    """
    return f"股票{name},是一加A股上市的公司，专注于互联网行业"

agent = create_agent(
    model = llm,
    tools = [get_price,get_info],
    system_prompt="你是一个ai股票助手，需要使用工具来回答用户的问题,请告诉我思考过程，让我知道你为什么调用这个工具。"
)

for chunk in  agent.stream(
    
        {"messages":[{
            "role":"user",
            "content":"请告诉我字节跳动股价多少，并介绍一下该公司。"
        }]},
        stream_mode = "values"
):
    latest_messages = chunk['messages'][-1]
    if latest_messages.content:
        print(type(latest_messages).__name__,latest_messages.content)
    try:
        if latest_messages.tool_calls:
            print(f"工具调用：{[tc['name']for tc in latest_messages.tool_calls]}")
    except AttributeError as e:
        pass


