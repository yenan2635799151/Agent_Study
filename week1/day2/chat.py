from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

#模型定义
llm =ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    temperature = 0.6
)

#定义prompt提示词模板
#system：设定ai角色
#user：用户输入
example_prompt = PromptTemplate.from_template(
"单词：{word}，反义词：{antonym}"
)
example_data=[
    {"word":"大","antonym":"小"},
    {"word":"上","antonym":"下"}
]

prompt=FewShotPromptTemplate(
    examples = example_data,
    example_prompt = example_prompt,
    prefix = "给出给定词的反义词，有如下示例",
    suffix = " 基于示例告诉我:{input_word}的反义词是什么",
    input_variables = ['input_word']
)
prompt_text = prompt.invoke(input = {"input_word":"左"}).to_string
print(prompt_text)

#定义输出解释器 output_parser：将模型输出的文本进行解析，提取出我们需要的部分
parser = StrOutputParser()

#构建chain 
# 流程：输入字典 -> 填充 Prompt -> 发给 LLM -> 解析输出

chain = prompt | llm | parser

#调用chain
#concept = "langchain"
#print (f"正在解释概念：{concept}(流式输出)...\n")


#for chunk in chain.stream({"concept":"递归神经网络"}):
 #   print(chunk,end="",flush=True)\

res = chain.invoke({"input_word":"左"})
print(res)