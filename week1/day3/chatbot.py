from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(
    model = "deepseek-v3.1",
    base_url = "https://api-ai.gitcode.com/v1",
    api_key ="tz-k44gc38zjW7zNzkmCHpQe",
    temperature = 0.6
)

memory = ConversationBufferMemory()

chatbot = ConversationChain(
    llm = llm,
    memory = memory,
    verbose = True
)

print ("欢迎来到AI聊天机器人！输入 'exit' 退出聊天。")

while True:
    user_input = input("用户: ")
    if user_input == "exit":
        break
    response = chatbot.predict(input = user_input)

    print("AI:",response)