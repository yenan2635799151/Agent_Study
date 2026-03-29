from fastapi import FastAPI
from pydantic import BaseModel
from agent.react_agent import ReactAgent
from fastapi.responses import StreamingResponse

app =FastAPI()
#初始化agent为全局变量，避免每次请求都重新创建agent实例
agent = ReactAgent()

#请求体
class ChatRequest(BaseModel):
    query:str


#流式生成器 
def stream_response(query:str):
    for chunk in agent.execute_stream(query):
        #每个chunk是一个字符串，使用yield逐个返回给客户端
        yield chunk

@app.post("/chat")
async def chat(req:ChatRequest):
    return StreamingResponse(
        stream_response(req.query),
        media_type="text/plain"
    )
