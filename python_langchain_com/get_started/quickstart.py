import os
from dotenv import load_dotenv

load_dotenv("E:\code_work_space\langchain_user_case\.env")
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
os.environ['OPENAI_API_BASE'] = os.environ.get('OPENAI_API_BASE')
print(os.environ['OPENAI_API_KEY'])

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    openai_api_key="sk-ks2Pwy2gt7aIvulGSHpyM05hjEirSISxkrpKFFutCtHZJye4",
    openai_api_base="https://api.chatanywhere.tech/v1"
)

respose = llm.invoke("介绍下黎明的基本情况")  # <class 'langchain_core.messages.ai.AIMessage'>
print(respose)
print(type(respose))

print("=============================")

# 指定输出格式为string
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])
from langchain_core.output_parsers import StrOutputParser

strOutputParser = StrOutputParser()
chain = prompt | llm | strOutputParser
respose = chain.invoke({"input": "介绍下黎明的基本情况?"})
print(respose)
print(type(respose))

# ============================检索链 Retrieval Chain============================
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
doc = loader.load()  # 将html页码转为Document
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter()
# split_documents,Document中包含page_content和metadata,split_documents将page_content拆分为多个chunk,每个chunk对于一个metedata,html、markdown等有不同split策略
documents = text_splitter.split_documents(doc)
vector = FAISS.from_documents(documents, embeddings)
from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")
document_chain = create_stuff_documents_chain(llm, prompt)
from langchain_core.documents import Document

document_chain_invoke = document_chain.invoke({
    "input": "how can langsmith help with testing?",
    "context": [Document(page_content="langsmith can let you visualize test results")]
})

print("基于指定context invoke:")
print(document_chain_invoke)

from langchain.chains import create_retrieval_chain

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
print("检索链输出:")
print(response["answer"])

"============================带有对话历史的检索链 Conversation Retrieval Chain====================================="
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# First we need a prompt that we can pass into an LLM to generate this search query

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up in order to get information relevant "
             "to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
from langchain_core.messages import HumanMessage, AIMessage

chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
response = retriever_chain.invoke({
    "chat_history": chat_history,
    "input": "Tell me how"
})
print("带有历史信息的检索链输出:")
print(response)
