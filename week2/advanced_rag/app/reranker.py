from FlagEmbedding import FlagReranker

reranker = FlagReranker(
    "BAAI/bge-reranker-base",
    use_fp16=True
)

def rerank(query,docs,top_k=3):
    pairs = [
        [query,doc.page_content]
        for doc in docs
    ]

    scores = reranker.compute_score(pairs)

    ranked_docs = sorted(
        zip(docs,scores),
        key = lambda x:x[1],
        reverse=True
    )

    return [doc for doc , _ in ranked_docs[:top_k]]