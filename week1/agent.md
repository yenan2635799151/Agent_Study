# rag+agent+langchain相关知识
## langchan
### 大模型api调用
### 提示词模板
要求输入是字典dict{}
PromptValue对象
#### PromptTemplate
通用提示词模板，支持动态注入
#### FewShotPromptTemplate

支持基于模板注入任意数量的示例信息
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

#### ChatPromptTemplate
支持注入任意数量的历史会话信息

利用MessagesPlaceholder当作占位符，在它所在的位置插入需要插入的信息，比如历史会话


from_template 只能接入一条消息

from_messages 可以接入一个list的消息

chat_template= ChatPromptTemplate.from_messages(
    ("system",""),
    ("ai",""),
    ("MessagesPlaceholder","history"),
    ("human")
)

history_data=[
    ("system","")
    .....
]

prompt_value = chat_template.invoke({"histiory":history_data})

### Chain链
上一个组件的输出作为下一个组件的输入

chain = prompt | llm 

只有Runnable子类对象才能接入链

### 输出解析器
#### StrOutputParser字符串输出解析器
模型输出结果为AIMessage，不能再作为模型的输入
简单字符串解析器，可以将AIMessage解析为简单字符串，符合模型invoke方法的要求
是Runnable接口的子类-->可以加入链
chain = prompt|llm|parser|llm
parser = StrOutParser()


#### JsonOutputParser
将模型输出结果转换为json对象
输入一个AIMessage 输出为dict
提示词模板需要输入：要求是字典格式的输出


#### 自定义chain函数
利用RunnableLambda（函数对象活lambdam匿名函数）
将普通函数转换为Rubbable接口实力，方便自定义函数加入chain
from langchain_core.rubbalbes import RunnableLambda


### history功能
#### RubbableWithMessageHistory 
在**原有链的基础上创建带有历史记录功能的新链**，新runnable实例
from langchain_core.runnalbes.history import RunnableWithMessageHistory

full_chain = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key ="",
    history_meaasges_key = ""
)
定义一个字典存储history
store={}
def get_history(session_id):
    if session_id not in store:
        store["session_id"]=InMemoryChatMessageHistory
    retrun store["session_id]


#### InMemoryChatMessageHistory
内存中存储，运行结束记忆丢失
为历史记录提供内存存储（临时使用）
from langchain_core.chat_history import InMemoryChatMessageHistory

定义函数来获取history
定义一个字典存储history
store={}
def get_history(session_id):
    if session_id not in store:
        store["session_id"]=InMemoryChatMessageHistory
    retrun store["session_id]

要在prompt 中使用MessagesPlaceholder 占位，来指出history占用的地方

最后在chain.invoke()
中需要加入一个参数指出session_id
config ={"configurable":{"session_id":"user1"}}


#### memory长期会话记忆 file

**FileChatMessageHistory类的实现**
核心思路：
基于文件存储会话记录，以session_id为文件名，不哦那个session_id有不同的文件存储消息

集成BaseChatMessageHistory实现如下3方法：
add_messages:同步模式，添加消息
messages：同步模式，获取消息
clear：同步模式，清楚消息


### Document laders 文档加载器
将不同来源数据读取为langchain的文档格式。
基于BaseLoader接口实现

**Class Document**是langchain文档的统一载体
索引文档架子阿强最终返回此类实例

from langchain_core.documents import Document

document = Document{
    page_content="",metadata={"":""}
}
page_content:文档内容
metadata：文档元数据。字典

不同加载器不同参数，实现了统一接口
**load()**一次性加载全部文档
**lazy_load()**延迟流式传输文档，大型数据集避免内存溢出

#### CSVLoader
loader = CSVLoader("data.csv",
                   csv_args = {
                        "delimiter":",",#指定分隔符，默认逗号
                        "quotechar":'"',#指定带有分隔符文本包围的引号是单引号还是双引号
                         #"fieldnames":["name","age","city"]# 如果数据原本没用表头，可以设定表头
                   },
                   encoding = "utf-8")

docs = loader.load()

#### JSONLoader

loader = JSONLoader("data.json",
                     jq_schema=".[]",
                     text_content = False,# 告诉JSONLoader，我抽取内容不是字符串
)

#### TextLoader
读取文本文件.txt。将全部内容放进一个Document对象中去
**字符文本分割器**RecursiveCharacterTextSplitter

### Vector stores 向量存储
创建向量存储，存删检索

#### 内置向量存储使用
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings

#### 外部向量存储使用chrom数据库
from langchain_chroma

vector_store = Chroma(
    collection_name = "",
    embedding_function= 
    persist_directory = "./"
)


### streamlit 
简易网页编写

**当web页面元素发生变化则代码重新执行一遍**
**这会导致运行状态丢失**

#基于streadmlit完成WEB网页上传服务
import streamlit as st

#添加网页标题
st.title("知识库更新服务")

#file_uploader
uploaded_file=st.file_uploader(
    "请上传txt文件",
    type=['txt'],
    accept_multiple_files=False,#表示仅接受一个文件上传
)

if uploaded_file is not None:
    #提取文件信息
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size/1024 #KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type}，大小{file_size:.2f}KB")

    #get_value
    text = uploaded_file.getvalue().decode("utf-8")
    st.write(text)


## Agent
执行流程动态，根据任务和结构自主调整
工具选择由LLM思考觉得
适合复杂多步骤需要决策的任务

大模型+工具+决策逻辑

新的langchain里已经修改agents里的内容
创建agent的函数只有
create_agent
没有create_tool_calling_agent
和AgentExecutor了

agent = create_agent(
    model = llm, 模型
    tools = [],  工具
    system_prompt = "你是一个智能AI助手，需要使用工具回答用户的问题" #传参数为str或者systemMessage对象
)

### ReAct框架
智能体的核心思考与行动框架
Reasoning+Action 推理+行动
让Agent像人一样 思考问题 -制定策略-执行行动-验证结果  的关键逻辑

**ReAct范式**
1.思考Reasoning 分析问题，判断现有信息是否足够明确下一步
2.行动Action：执行思考阶段指定的策略
基于模型决策结果，调用工具获取信息
3.观察observation：获取行动结果，提前有效信息
根据获取工具返回值判断工具是否正常工作，为下一轮思考提供信息
