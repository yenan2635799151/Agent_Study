
from app.vector_store import build_vector_store
from app.query_transform_MQ import multi_query
from app.query_transform_Hyde import Hyde
from app.hybrid_retriever import hybrid_search
from app.reranker import rerank
vectorstore = build_vector_store()
mode = "multi"

def rag_search(query:str)->str:


    if mode =="multi":
    #生成多个查询
        queries = multi_query(query)
    elif mode =="hyde":
        query = Hyde(query)
        queries = [query]
    else:
        queries = [query]

    #多query进行检索
    docs = []
    for q in queries:
        print("q:",q)
        results =hybrid_search(q)
        docs.extend(results)

    #文档去重 因为多个 query 可能检索到 相同文档
    unique_docs={}

    for doc in docs:
        print("dos.content:",doc.page_content)
        unique_docs[doc.page_content] = doc
    docs = list(unique_docs.values())

    #构造context
    docs = rerank(query,docs,top_k=3)

    #构造context
    context ="\n".join(
        doc.page_content for doc in docs
    )
    print("context:",context)
    return context
