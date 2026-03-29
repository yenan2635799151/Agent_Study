from langchain_community.document_loaders import JSONLoader

loader = JSONLoader("data.json",
                     jq_schema=".[]",
                     text_content = False,# 告诉JSONLoader，我抽取内容不是字符串
)

docs = loader.load()

for doc in docs:
    print(doc,"\n")