from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
loader = TextLoader("docs.txt", encoding="utf-8")

docs  =loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap=20,
    separators =["\n\n","\n",".","!","?"," ", ""],#分隔符，用来当分割的依据
    length_function =len,
)
 
docs_split = splitter.split_documents(docs)

for doc in docs_split:
    print(doc.page_content)