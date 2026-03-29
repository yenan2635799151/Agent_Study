from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
def Hyde(question):

    llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    ) 
        
    prompt = ChatPromptTemplate.from_template(
        """
    请根据用户问题生成一段可能出现在知识库中的中文回答，用于向量检索。
    问题：
    {question}
"""
    )
    chain = prompt | llm

    result = chain.invoke(
        {
            "question":question
        }
    )
    
    print ("Hyde生成的内容：",result.content)
    return result.content
