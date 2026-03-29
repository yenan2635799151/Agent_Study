from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader,TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

loader  = TextLoader("docs.txt",encoding = "utf-8")
docs = loader.load()
print(docs)
print(type(docs))
print("="*20)

llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20
)

chunks = splitter.split_documents(docs)
print (type(chunks))

# vectorstore = InMemoryVectorStore(
#     embedding = HuggingFaceEmbeddings(
#         model_name = "/home/jiankunshi/.cache/huggingface/hub/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8",
#         model_kwargs = {"device":"cuda"}
#     )
# )
prompt = ChatPromptTemplate.from_messages(
    [
    ("system","你是一个有用的助手，帮助用户根据文档内容回答问题。参考资料{context}"),
    ("user","{input}")
    ]
)
parser = StrOutputParser()

vectorstore = InMemoryVectorStore(
    embedding = HuggingFaceEmbeddings(#嵌入模型
        model_name = "/home/jiankunshi/.cache/huggingface/hub/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8",
        model_kwargs = {"device":"cuda"}#指定数据存放的文件夹
    ),
    
)

#向量存储的新增删除检索
vectorstore.add_documents(
    documents=chunks,
) #新增

res = vectorstore.similarity_search("什么是RAG？",k=2)
res_text = [doc.page_content for doc in res]


def prompt_print(prompt):
    print(prompt.to_string())
    return prompt

chain =prompt | prompt_print |llm|parser

result = chain.invoke({
      "input":"什么是RAG？",
      "context":res_text
})

print(result)