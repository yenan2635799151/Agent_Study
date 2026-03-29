from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from langchain_core.prompts import ChatPromptTemplate

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent




llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
   
)

@tool
def multiply(a:int,b:int)-> int:
    """计算两个整数的乘积"""
    return a * b

@tool
def add(a:int,b:int)-> int:
    """计算两个整数的和"""
    return a + b

tools = [multiply,add]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个数学助手"),
        ("user","{input}"),
        ("placeholder","{agent_scratchpad}")
    ]
)


#创建agent

agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent = agent,
    tools = tools,
    verbose = True
)

respose = agent_executor.invoke(
    {
        "input":"3乘以5再加上2等于多少？"
    }
)
print(respose)