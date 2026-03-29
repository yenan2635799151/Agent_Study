这个文档记录我学习agent的学习过程

# 第一周：

后端基础: 
FastAPI 路由 Pydantic 数据校验
LangChain 核心: LLM, Prompt Templates, Output Parsers, LCEL
Naive RAG 流程: Document Loaders, Text Splitters, Embeddings, Vector Stores
向量数据库: FAISS 

代码小项目:
FastAPI 搭建 "Hello, World" API 服务
 LangChain LCEL 编写第一个 LLM Chain
建立了一个完整的 Naive RAG + agent的API 应用（在day6的文件夹中，使用uvicorn main：app --reload --port 800x 运行，然后再127.0.0.1.800x来调试运行）



# 第二周：
对 langchain 和rag内容的进一步学习

# 第三周：
完成week3中的agent_project项目的v1版本一个初始的只能扫地机器人客服问答系统
基于langchain + rag + chroma小型数据库

# 第四周：
在v1的基础上进行改进出v2，代码为week3/agent_project
1.增加了真实的tools:
  a.利用ip获取用户所在地区
  b.利用所在地区调用api获取天气信息
2.实现bm25+相似度检索的hybrid+reranker两阶段检索
3.利用vibe coding 生成了一个基于next.js+chatUI的类chatgpt前端界面
4.利用RAGAS对RAG进行评估，评估结果：
在当前情境下，普通语义相似度检索结果比两阶段检索效果更好

# 第五周：
在v2的基础上继续改进：
1.增加真实的生产级向量数据库Milvus
2.提升rag的复杂数据解析能力（表格等）

