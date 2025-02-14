from langchain import hub
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain.chains import history_aware_retriever
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from langchain.tools import BaseTool, StructuredTool, tool

load_dotenv("../../../.env")
print(os.environ["OPENAI_API_KEY"])

contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),

    ]
)
print("=================contextualize_q_prompt=================")
print(contextualize_q_prompt)

llm = ChatOpenAI()

docs = [
    Document(page_content="Jesse loves red but not yellow"),
    Document(page_content="Jamal loves green but not as much as he loves orange")
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitter = text_splitter.split_documents(docs)
vectore = Chroma.from_documents(splitter, embedding=OpenAIEmbeddings())
retriever = vectore.as_retriever()

history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

print(history_aware_retriever)

try:
    history_aware_retriever.invoke({"input1": "Jesse loves red but not yellow"})
except Exception as e:
    print(e)
