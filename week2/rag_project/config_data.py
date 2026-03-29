md5_path = "./md5.txt"

#chroma
collection_name = "RAG"
persist_directory ="./chroma_db"
#splitter
chunk_size = 1000
chunk_overlap = 200
separators = ["\n\n","\n","\r\n",".","!","?",",","，","。","！","？"]
max_split_char_number = 1000

#
similarty_thrshold =1

embedding_model_name = "/home/jiankunshi/.cache/huggingface/hub/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8"  

chat_model_name = "deepseek-chat"
model_url = "https://api.deepseek.com"


session_config= {
    "configurable":{
        "session_id":"user1"
    }
}