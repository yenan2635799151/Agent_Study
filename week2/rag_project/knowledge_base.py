#知识库
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
def check_md5(md5_str: str):
    #检查传入的md5字符串是否已经被处理过了
    #return False 表示未处理过，return True 表示已经处理过了
    if not os.path.exists(config.md5_path):
        #if进入表示文件不存现在。肯定没有处理过该值
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8') .readlines():
            line = line.strip()#处理字符串前后的空格和回车
            if line == md5_str:
                return True #已经处理过
            
        return False   
    

def save_md5(md5_str: str):
    #将传入的md5字符串保存到文件中
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str,encoding='utf-8'):
    #将传入的字符串转换为md5字符串
    #将字符串转换为bytes字节数组
    str_bytes =input_str.encode(encoding=encoding)
    #创建md5对象
    md5_obj = hashlib.md5()#获得MD5对象
    md5_obj.update(str_bytes)#更新内容（传入即将要转换的字节数组）
    md5hex = md5_obj.hexdigest()#得到MD5的十六进制字符串
    return md5hex

class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件夹不存在则创建，存在则跳过
        os.makedirs(config.persist_directory,exist_ok=True)
         #向量存储的实例Chroma向量库对象
        self.chroma = Chroma(
            collection_name = config.collection_name,
            embedding_function = HuggingFaceEmbeddings(
                model_name = "/home/jiankunshi/.cache/huggingface/hub/models--BAAI--bge-small-zh/snapshots/1d2363c5de6ce9ba9c890c8e23a4c72dce540ca8",
                model_kwargs={"device":  "cuda"}
            ),
            persist_directory=config.persist_directory
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators ,#自然段落划分的符号
            length_function = len
        ) #文本分割器实例RecursiveCharacterTextSplitter对象


    def upload_by_str(self, data,filename):
        #传入的字符串向量化，存入向量数据库中
        #1.计算字符串的MD5值
        md5_hex = get_string_md5(data)
        print (f"MD5值：{md5_hex}")
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        #2.如果MD5值未处理过，则进行文本分割和向量化存储
        if len(data)>config.max_split_char_number:
            knowledge_chunks: list[str] =self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "opertor":"admin"
        }    
        self.chroma.add_texts(#内容加载到向量库中
            #iterable [str] 迭代器 ： list tuple
            texts = knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)
        return "[成功]内容已经成功加载到知识库"

if __name__ == "__main__":
    service = KnowledgeBaseService()
