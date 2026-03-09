from app.rag import rag_search
from langchain_openai import ChatOpenAI
import os
from langchain.agents import AgentExecutor,create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

@tool
def rag_tool(query:str)->str:
    """
    Search information about LangChain from local documents
    """
    return rag_search(query)


tools =[rag_tool]

def create_agent():
    llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    ) 

    #agent prompt
    agent_prompt = ChatPromptTemplate(
        [
            ("system","你是一个智能AI助手，可以使用工具回答用户的问题"),
            ("user","{input}"),
            ("placeholder","{agent_scratchpad}")
        ]
    )

    #创建agent
    agent  = create_tool_calling_agent(
        llm,
        tools,
        agent_prompt
    )

    agent_executor = AgentExecutor(
        agent = agent,
        tools = tools,
        verbose = True
    )

    return agent_executor