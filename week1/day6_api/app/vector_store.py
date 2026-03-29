from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.loader import load_docs

def build_vector_store():
    docs = load_docs()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name = "/home/jiankunshi/.cache/huggingface/hub/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8",
        model_kwargs = {"device":"cuda"}
    )
    
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore