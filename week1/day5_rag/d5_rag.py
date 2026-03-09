import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent,AgentExecutor

#加载文档
loader = TextLoader("docs.txt")
docs = loader.load()

#LLM
llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)

#文本切分
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20
)

chunks = splitter.split_documents(docs)

#Embedding
embedding = HuggingFaceEmbeddings(
    model_name = "/home/jiankunshi/.cache/huggingface/hub/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8",
    model_kwargs = {"device":"cuda"}
)

#向量数据库FAISS
vectorstore = FAISS.from_documents(
    chunks,
    embedding
)

#检索器retriever
retriever = vectorstore.as_retriever(search_kwargs={"k":2})

#RAG prompt

rag_prompt = ChatPromptTemplate.from_template(
    """
请根据以下内容回答问题：
{context}

问题：
{question}
"""
)

#RAG Tool

@tool
def rag_search(question:str) ->str:
    """
    Search relevant information from the vector database using RAG.
    """

    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = rag_prompt.invoke(
        {
            "context":context,
            "question":question
        }
    )
    response = llm.invoke(final_prompt)
    return response.content

#agent prompt
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个智能AI助手，可以使用工具回答用户的问题"),
        ("user","{input}"),
        ("placeholder","{agent_scratchpad}")
    ]
)

#创建Agent

tools = [rag_search]

agent = create_tool_calling_agent(
    llm,
    tools,
    agent_prompt
)

agent_executor = AgentExecutor(
    agent = agent,
    tools = tools,
    verbose = True
)

#测试
response = agent_executor.invoke(
    {
    "input":"什么是LangChain？"
    }
)
print(response["output"])


