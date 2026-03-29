from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
def multi_query(question):

    llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    ) 
        
    prompt = ChatPromptTemplate.from_template(
        """
    请将用户的问题用中文改写为3个不同的搜索查询：
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
    
    queries = result.content.split('\n')
    n_queries = []
    for q in queries:
        if q.strip():
            n_queries.append(q.strip())
    return n_queries
