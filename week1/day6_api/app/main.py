from fastapi import FastAPI
from pydantic import BaseModel# 请求体

from app.agent import create_agent

app = FastAPI()

agent = create_agent()

class Query(BaseModel):
    question:str

@app.post("/chat")
def chat(query:Query):
    result = agent.invoke(
        {"input":query.question}
    )

    return{
        "answer":result["output"]
    }