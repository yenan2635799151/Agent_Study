#langchain学习
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate

'''
llm = ChatOpenAI(
    model = "deepseek-v3.1",
    base_url = "https://api-ai.gitcode.com/v1",
    api_key ="DLb4beEzQ-YpagyW9B4JS3yx",
    temperature = 0.6
)

prompt = PromptTemplate.from_template(
    "请用最简单的语言解释:{topic}"
)

chain = prompt | llm

result = chain.invoke({
   "topic":"langchain"
})

print(result.content)


'''

llm =ChatOpenAI(
    model = "deepseek-v3.1",
    base_url = "https://api-ai.gitcode.com/v1",
    api_key ="DLb4beEzQ-YpagyW9B4JS3yx",
    temperature = 0.6
)

prompt = PromptTemplate.from_template(
    "你是一个AI助手，请回答我的问题：{question}"
)

chain = prompt | llm

while  True :
    question  = input("用户：")
    result = chain.invoke({
        "question":question
    })
    print("AI:",result.content)