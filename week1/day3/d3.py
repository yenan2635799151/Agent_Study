from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

store = {}

def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

llm = ChatOpenAI(
    model = "deepseek-v3.1", 
    base_url = "https://api-ai.gitcode.com/v1",
    api_key = "tz-k44gc38zjW7zNzkmCHpQe",
    temperature = 0.6
)

#from_messages 是完整聊天结构模板
#from_template 是单轮对话模板

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个AI助手，帮助用户解答问题。"),
        MessagesPlaceholder(variable_name="history"),
        ("user","{input}")
    ]
)

paser = StrOutputParser()

chain = prompt | llm | paser



chatbot = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key = "input",
    history_messages_key = "history",
   
)

print("欢迎来到AI聊天机器人！输入 'exit' 退出聊天。")

while True:
    user_input = input("user:")
    if user_input == "exit":
        break

    response = chatbot.invoke(
        {"input": user_input},
        config ={"configurable":{"session_id":"user1"}}
    )
    print("AI:", response)