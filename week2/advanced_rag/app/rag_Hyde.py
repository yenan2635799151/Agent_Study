
from app.vector_store import build_vector_store
from app.query_transform_Hyde import Hyde
vectorstore = build_vector_store()

def rag_search_Hyde(query:str)->str:
    retriever = vectorstore.as_retriever(#检索器，里面使用相似度搜索
        search_kwargs={"k":3}
    )

    #生成多个查询
    Hyde_doc = Hyde(query)

    docs = retriever.invoke(Hyde_doc)

    #构造context
    context ="\n".join(
        doc.page_content for doc in docs
    )
    print("context",context)
    return context
