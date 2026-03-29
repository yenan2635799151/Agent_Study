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
def get_weight()->int:
    """
    获取体重，单位千克
    """
    return 80

@tool 
def get_height()->int:
    """
    获取身高，单位厘米
    """
    return 175

agent = create_agent(
    model = llm,
    tools = [get_height,get_weight],
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按照[思考->行动->观察->再思考]的流程来解决问题，
    且**每轮仅能思考并调用1个工具**，禁止单词调用多个工具。
    并告诉我你的思考过程，工具的调用原因，按思考、行动、观察三个结果告诉我
"""
)

for chunk in  agent.stream(
    
        {"messages":[{
            "role":"user",
            "content":"计算我的BMI。"
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


