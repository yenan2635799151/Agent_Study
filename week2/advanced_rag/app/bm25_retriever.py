from rank_bm25 import BM25Okapi 
import jieba
class BM25Retriever():
    def __init__(self,docs):
        self.docs = docs#保存输入文档
        #停用词表，没有实际语义的词
        self.stopwords = {
            "的","是","了","一个","我们","你们",
            "这个","那个","什么","如何","怎么",
            "吗","呢","啊","吧","就"
        }
        
        #构建bm25预料
        corpus = [
           self.tokenize(doc.page_content)
           for doc in docs
        ]
        self.bm25 = BM25Okapi(corpus)#对文档建立bm25分数和索引用来查询，等于一个索引数据库

    def tokenize(self,text):
        words = jieba.cut(text)
        tokens = [
            w for w in words
            if w.strip()and w not in self.stopwords
        ]
        return tokens

    def retrieve(self,query,k=3):
        #输入的query进行分词
        tokenized_query = self.tokenize(query)
        #计算query和每个文档相对应的bm25分数
        scores = self.bm25.get_scores(tokenized_query)
        #对文档按照bm25分数进行排序
        ranked_docs = sorted(
            zip(self.docs,scores),#把文档和分数合并到一起成为一个元组作为排序对象
            key = lambda x: x[1],#key为排序依据值，后面意思取元组中的第二个值
            reverse = True #降序
        )
        res = []
        for doc,_ in ranked_docs[:k]:
            res.append(doc)
        
        return [doc for doc, _ in ranked_docs[:k]]