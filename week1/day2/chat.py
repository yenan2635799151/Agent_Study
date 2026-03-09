from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


#模型定义
llm =ChatOpenAI(
    model = "deepseek-v3.1",
    base_url = "https://api-ai.gitcode.com/v1",
    api_key ="tz-k44gc38zjW7zNzkmCHpQe",
    temperature = 0.6
)

#定义prompt提示词模板
#system：设定ai角色
#user：用户输入
prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个AI领域的专家，擅长用通俗易懂的语言解释复杂的AI概念。你的解释应该包含一个比喻"),
    ("user","{concept}")
]
)

#定义输出解释器 output_parser：将模型输出的文本进行解析，提取出我们需要的部分
parser = StrOutputParser()

#构建chain 
# 流程：输入字典 -> 填充 Prompt -> 发给 LLM -> 解析输出

chain = prompt | llm | parser

#调用chain
concept = "langchain"
print (f"正在解释概念：{concept}(流式输出)...\n")

for chunk in chain.stream({"concept":"递归神经网络"}):
    print(chunk,end="",flush=True)