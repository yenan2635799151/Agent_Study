#基于streadmlit完成WEB网页上传服务
import streamlit as st
from knowledge_base import KnowledgeBaseService

#添加网页标题
st.title("知识库更新服务")

#file_uploader
uploaded_file=st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False,#表示仅接受一个文件上传
)

service = KnowledgeBaseService()
##session_state是一个字典
if"service"not in st.session_state:
    st.session_state["service"]=KnowledgeBaseService()

if uploaded_file is not None:
    #提取文件信息
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size/1024 #KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type}，大小{file_size:.2f}KB")

    #get_value
    text = uploaded_file.getvalue().decode("utf-8")

    result = st.session_state["service"].upload_by_str(text,file_name)
    
    st.write(result)
