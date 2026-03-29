from langchain_community.document_loaders import CSVLoader


loader = CSVLoader("data.csv",
                   csv_args = {
                        "delimiter":",",#指定分隔符，默认逗号
                        "quotechar":'"',#指定带有分隔符文本包围的引号是单引号还是双引号
                         #"fieldnames":["name","age","city"]# 如果数据原本没用表头，可以设定表头
                   },
                   encoding = "utf-8")

docs = loader.load(
   
)

for doc in docs:
    print(doc,"\n")