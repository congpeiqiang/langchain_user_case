from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import StrOutputParser

load_dotenv("../../.env")
print(os.environ["OPENAI_API_KEY"])

llm = ChatOpenAI()

docs = [
    Document(page_content="Jesse loves red but not yellow"),
    Document(page_content="Jamal loves green but not as much as he loves orange")
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitter = text_splitter.split_documents(docs)
vectore = Chroma.from_documents(splitter, embedding=OpenAIEmbeddings())
retriever = vectore.as_retriever()

prompt = ChatPromptTemplate.from_messages(
    [("system", "What are everyone's favorite colors:\n\n{context}"),
     ("user", "{input}")]
)

chain = (
        {"context": retriever, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

print("===========chain.first==================")
print(chain.first)
print("===============chain.middle===========")
print(chain.middle)
print("===============chain.last============")
print(chain.last)
