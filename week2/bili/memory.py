from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
import os
llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    temperature = 0.6
)

prompt =ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("user","请回答问题{input}")
    ]
)

def print_prompt(prompt_value):
    print("="*20,prompt_value.to_string(),"="*20)
    return prompt_value

str_parser = StrOutputParser()

base_chain = prompt|print_prompt| llm |str_parser


store = {} #key为senssion_id value是InMemoryChatMessageHistory类对象
#实现通过会话id获取InMemoryChatMessageHistory对象
def get_history(session_id):
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]



#创建新的链，对原有的增强功能，自动附加历史消息
history_chain =RunnableWithMessageHistory(
    base_chain,#被增强的链
    get_history,#通过会话id获取InMemoryChatMessageHistory对象
    input_messages_key = "input",#用户输入在模板中的占位符
    history_messages_key = "chat_history"#历史会话在模板中的占位符

)


res = history_chain.invoke({"input":"小明有两只猫" },
        config ={"configurable":{"session_id":"user1"}})
print("第一轮",res)
res = history_chain.invoke({"input":"小明有几个宠物" },
        config ={"configurable":{"session_id":"user1"}})
print("第二轮",res)