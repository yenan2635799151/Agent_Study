from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
import os

#创建模型
llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    temperature = 0.6
)
#创建解析器
str_parser= StrOutputParser()
Json_parser = JsonOutputParser()

#函数入参：AIMessage -》 转换为dict{}
my_func = RunnableLambda(lambda ai_misg:{"name":ai_misg.content})
#提示词模板
# first_prompt = PromptTemplate.from_template(
#     "我邻居姓:{lastname},刚生了{gender},请帮忙取名，并封装为JSON格式返回给我"
#     "要求key是name，value就是你起的名字，严格遵守格式要求。"
# )   

first_prompt = PromptTemplate.from_template(
    "我邻居姓:{lastname},刚生了{gender},请帮忙取名，仅告诉我名字，不要额外的信息"

)   

second_prompt = PromptTemplate.from_template(
    "姓名：{name}，请帮我解析含义。"
)

chain = first_prompt | llm | my_func | second_prompt | llm | str_parser


for chunk in chain.stream({"lastname":"张","gender":"女儿"}):
    print(chunk,end="",flush=True)

