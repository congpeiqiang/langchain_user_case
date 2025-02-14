from langchain.llms import OpenAI

# #设置代理
# import os
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ['OPENAI_API_KEY'] = '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'
# from langchain.document_loaders import WebBaseLoader
# from langchain.indexes import VectorstoreIndexCreator
# llm = OpenAI(openai_api_key="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")#这里需要填入你的openai api key，这个api已经不可用
# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
# index = VectorstoreIndexCreator().from_loaders([loader])
# respose=index.query("What is Task Decomposition?")
# print(respose)

"==========================================================================================="
#设置代理
import os
from langchain.document_loaders import WebBaseLoader
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['OPENAI_API_KEY'] = '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'
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")

#  load data
data = loader.load()
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 切分
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)
print(all_splits[0])

# 存储
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
question = "What are the approaches to Task Decomposition?"
docs = vectorstore.similarity_search(question)
print(len(docs))
print(docs[0])

# 问答
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever())
print(qa_chain({"query": question}))

# 添加记忆功能
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
from langchain.chains import ConversationalRetrievalChain
retriever = vectorstore.as_retriever()
chat = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
result = chat({"question": "What are some of the main ideas in self-reflection?"})
print(result['answer'])

result = chat({"question": "How does the Reflexion paper handle it?"})
print(result['answer'])

"=================================================================================================="