import os ,hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader,PyPDFLoader
#获取文件的md5的十六进制字符串
def get_file_md5_hex(filepath:str):
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件{filepath}不存在")
        return 
    
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]文件{filepath}不是文件")
        return 
    
    md5_obj = hashlib.md5()

    chunk_size = 4096 #4KB分片，避免文件内存过大

    try:
        with open(filepath,"rb")as f: #计算文件的md5 必须二进制读取rb
            while chunk :=f.read(chunk_size):
                md5_obj.update(chunk)
            """
            chunk = f.read(chunk_size)
            while chunk:
                md5_obj.update(chunk)
                chunk = f.read(chunk_size)
            """        
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5计算]文件{filepath}计算md5时发生错误: {str(e)}")
        return




#返回文件夹内的文件列表，过滤掉非文本文件
def listdir_with_allowed_type(path:str,allowed_types:tuple[str]):
    files = []
    
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allowed_types
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path,f))
    return tuple(files)

def pdf_loader(filepath:str,passdw = None)->list[Document]:
    return PyPDFLoader(filepath,passdw).load()

def txt_loader(filepath:str,encoding:str="utf-8")->list[Document]:
    return TextLoader(filepath,encoding).load()
    