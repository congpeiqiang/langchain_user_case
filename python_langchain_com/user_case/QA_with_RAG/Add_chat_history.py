from dotenv import load_dotenv
import os
import bs4
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.runnables import RunnablePassthrough

load_dotenv("../../../.env")
print(os.environ["OPENAI_API_KEY"])

# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)

docs = loader.load()

llm_chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 建议retriever
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitter = text_splitter.split_documents(docs)
vectore = Chroma.from_documents(splitter, embedding=OpenAIEmbeddings())
retriever = vectore.as_retriever()

prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


print("=====================prompt=======================")
print(prompt)

rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_chat
        | StrOutputParser()
)

pre = rag_chain.invoke("请自我介绍")
print(f"=========================pre=========================")
print(pre)


from langchain.chains import create_history_aware_retriever, LLMChain #
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
p1 = contextualize_q_prompt.format_messages(input="请自我介绍", chat_history=[]) # Format the chat template into a list of finalized messages
p2 = contextualize_q_prompt.format_prompt(input="请自我介绍", chat_history=[]) # Format prompt. Should return a PromptValue.
p3 = contextualize_q_prompt.format(input="请自我介绍", chat_history=[]) # Format the chat template into a string

print("============format_messages================")
print(p1)
print(type(p1))
print("============format_prompt================")
print(p2)
print(type(p2))
print("==========format_prompt to_messages()=============")
print(p2.to_messages())
print(type(p2.to_messages()))
print("==========format_prompt to_string()=============")
print(p2.to_string())
print(type(p2.to_string()))
print("============format================")
print(p3)
print(type(p3))
print("=================contextualize_q_prompt=================")
print(contextualize_q_prompt)
history_aware_retriever = create_history_aware_retriever(llm_chat, retriever, contextualize_q_prompt)

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm_chat, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

from langchain_core.messages import HumanMessage

chat_history = []

question = "What is Task Decomposition?"
ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})
print(ai_msg_1)
chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

second_question = "What are common ways of doing it?"
ai_msg_2 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})

print(ai_msg_2["answer"])