from app.vector_store import build_vector_store
from app.bm25_retriever import BM25Retriever
from app.loader import load_docs

vectorstore = build_vector_store()

docs = load_docs()

bm25 = BM25Retriever(docs)

def hybrid_search(query):
    #vector search
    vector_docs = vectorstore.similarity_search(query)
    
    #bm25_search
    bm25_docs = bm25.retrieve(query,k=3)

    docs = vector_docs + bm25_docs

    return docs