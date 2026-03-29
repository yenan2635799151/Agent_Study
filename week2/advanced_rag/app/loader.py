from langchain_community.document_loaders import TextLoader

def load_docs():
    loader = TextLoader("data/docs.txt",encoding = "utf-8")
    docs = loader.load()
    return docs

