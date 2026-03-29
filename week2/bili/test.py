from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
prompt =ChatPromptTemplate.from_messages(
    [
        ("system","你是一个诗人，可以作诗"),
        MessagesPlaceholder("history"),
        ("human","请再写一首诗"),
   
    ]
)

history_data=[
    ("human","你来写一首唐诗"),
    ("ai","床前明月光"),
    ("human","请再来一首诗"),
    ("ai","锄禾日当午"),
]



llm = ChatOpenAI(
   model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)

parser = StrOutputParser()
#print(prompt,type(prompt))

chain = prompt | llm|parser
print(type(chain))

# res  = chain.invoke({
#     "history":history_data,
#     "input":"请再写一首诗"
# })

# for chunk in chain.stream({
#     "history":history_data }):
#     print(chunk.content,flush=True,end="")
res = chain.invoke({"history":history_data})
print(type(res))
print(res)