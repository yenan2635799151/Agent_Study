
from app.vector_store import build_vector_store

vectorstore = build_vector_store()

def rag_search(query:str)->str:
    retriever = vectorstore.as_retriever(#检索器，里面使用相似度搜索
        search_kwargds={"k":3}
    )

    docs = retriever.invoke(query)

    context ="\n".join(
        doc.page_content for doc in docs
    )

    return context
