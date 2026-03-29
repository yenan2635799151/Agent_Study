from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from typing import Sequence, List
import os ,json
from langchain_core.messages import messages_from_dict,message_to_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
#message_to_dict:单个消息对象（BaseMessage类实例）转换为字典
#messages_from_dict:[字典，字典。。。。]转为[消息，消息，  ]
#各种Message都是BaseMessage的子类

class FileChatMessageHistorhy(BaseChatMessageHistory):
    
    def __init__(self,session_id,storage_path):
        self.session_id = session_id #会话id
        self.storage_path = storage_path #不同会话id的存储文件所在的文件夹路径
        #完整的文件路径
        self.file_path = os.path.join(self.storage_path,self.session_id)
        #确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self,messages:List[BaseMessage])->None:
            #Sequence 序列类似list tuple
            all_messages = list(self.messages) #已有的消息列表
            all_messages.extend(messages) #将新消息添加到列表中融合成一个list

            #将数据同步写入本地文件中
            #类型对象写入文件-》一堆二进制
            #将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
            #官方message_todict:单个消息对象(BaseMessage实例)->字典
            # new_messages = []
            # for message in all_messages:
            #     d = message_to_dict(message)
            #     new_messages.append(d)
            
            new_messages = [ message_to_dict(message) for message in all_messages]
            #将数据写入文件
            with open(self.file_path,"w",encoding= "utf-8")as f:
                json.dump(new_messages,f)    

    @property #装饰器将messages方法变为成员属性
    def messages(self)->List[BaseMessage]:
        #当前文件内 list[字典] 转换为BaseMessage

        try:
            with open (self.file_path,"r",encoding="utf-8")as f:
                messages_data =json.load(f) #list[字典] 
                return messages_from_dict(messages_data)#list[BaseMessage]
        except FileNotFoundError:
             return []
        
    def clear(self)->None:
             with open(self.file_path,"w",encoding="utf-8")as f:
                json.dump([],f)


llm = ChatOpenAI(
    model = "deepseek-chat", 
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    temperature = 0.6
)

prompt =ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史回应用户问题。对话历史："),
        MessagesPlaceholder("chat_history"),
        ("user","请回答问题{input}")
    ]
)

def print_prompt(prompt_value):
    print("="*20,prompt_value.to_string(),"="*20)
    return prompt_value

str_parser = StrOutputParser()

base_chain = prompt|print_prompt| llm |str_parser



def get_history(session_id):
    return FileChatMessageHistorhy(session_id,"./chat_history")



#创建新的链，对原有的增强功能，自动附加历史消息
history_chain =RunnableWithMessageHistory(
    base_chain,#被增强的链
    get_history,#通过会话id获取InMemoryChatMessageHistory对象
    input_messages_key = "input",#用户输入在模板中的占位符
    history_messages_key = "chat_history"#历史会话在模板中的占位符

)


# res = history_chain.invoke({"input":"小明有两只猫" },
#         config ={"configurable":{"session_id":"user1"}})
# print("第一轮",res)
res = history_chain.invoke({"input":"小明有几个宠物" },
        config ={"configurable":{"session_id":"user1"}})
print("第二轮",res)