from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
#加载文档
loader = TextLoader("docs.txt")
docs = loader.load()

llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)

#文本切分
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,  #每段长度
    chunk_overlap = 20 #重叠部分 避免语义割裂
)

chunks = splitter.split_documents(docs)

#Embedding
embedding = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-zh",
    model_kwargs = {"device":"cuda"}
)

#向量数据库FAISS
vectorstore = FAISS.from_documents(
    chunks,
    embedding
)

#检索器retriever
retriever = vectorstore.as_retriever()

#prompt
prompt = ChatPromptTemplate.from_template(
    """请根据以下内容回答问题：
    {context}
    问题：
    {question}
    """
)

#RAG
question = "LangChain是什么？"

docs = retriever.invoke(question)
context = "\n".join([doc.page_content for doc in docs])

final_prompt = prompt.invoke(
    {
        "context":context,
        "question":question
                }
)

response = llm.invoke(final_prompt)

print(response.content)



