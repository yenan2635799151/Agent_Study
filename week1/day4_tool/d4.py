from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    temperature = 0.6
)

@tool
def multiply(a:int,b:int)-> int:
    """计算两个整数的乘积"""
    return a * b

llm_with_tool = llm.bind_tools([multiply])

response = llm_with_tool.invoke("3乘以5是多少")

print(response)
print(type(response))