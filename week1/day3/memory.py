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

conversation = ConversationChain(
    llm = llm,
    memory = memory,
    verbose = True
)

while True:
    user_input = input("user: ")
    if user_input =="exit":
        break

    response = conversation.predict(input = user_input)
    print("AI:",response)
