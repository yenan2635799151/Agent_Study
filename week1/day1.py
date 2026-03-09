from fastapi import FastAPI

#创建应用
app = FastAPI()
#定义接口
@app.get("/")
def home():
    return {"msg":"hello agent"}

#query string参数
@app.get("/hello")
def hello(name:str):
    return {"msg":f"hello {name}"}

#响应数据，返回json数据
@app.get("/add")
def add(a:int,b:int):
    return{"result":a+b}

@app.get("/time")
def get_time():
    import time
    return {"time":time.time()}

#path参数
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return{
        "item_id":item_id
    }

#Post请求
from pydantic import BaseModel
#利用pydantic模型定义请求体，包含多个字段，其中一些有默认值

class Question(BaseModel):
    question: str

class Item(BaseModel):
    name:str
    description:str = None
    price:float
    tax:float = None

@app.post("/items")
def create_item(item: Item):
    return item

@app.post("/ask")
def ask_qusetion(q:Question):
    return {
        "question":q.question
    }
class Chat(BaseModel):
    question:str

@app.post("/chat")
def chat(req:Chat):
    answer =f"你问的问题是:{req.question}"
    return{
    "answer":answer
    }