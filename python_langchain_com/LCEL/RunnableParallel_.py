import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core import prompts
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv("../../.env")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


prompt = PromptTemplate.from_template("{context}, {question}")

# rag_chain_with_source = RunnableParallel(
#     {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
# ).assign(answer=prompt)
'''
此种方式, 输出值包含context、question、answer三个key-values。
{'context': ('context', 'question'), 'question': ('context', 'question'), 'answer': StringPromptValue(text="('context', 'question'), ('context', 'question')")}
=================rag_chain_with_source===================
first={
  context: RunnablePassthrough(),
  question: RunnablePassthrough()
} last=RunnableAssign(mapper={
  answer: PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
})


'''
rag_chain_with_source = (
        RunnableParallel(
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        )
        | prompt
)
'''
text="('context', 'question'), ('context', 'question')"
=================rag_chain_with_source===================
first={
  context: RunnablePassthrough(),
  question: RunnablePassthrough()
} last=PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
'''

# 多个assign()  pick()
rag_chain_with_source = RunnableParallel(
    {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
).assign(answer_1=prompt).assign(answer_2=prompt)
'''
==================rag_chain_with_source.invoke(('context', 'question'))===============
{'context': ('context', 'question'), 'question': ('context', 'question'), 'answer_1': StringPromptValue(text="('context', 'question'), ('context', 'question')"), 'answer_2': StringPromptValue(text="('context', 'question'), ('context', 'question')")}
=================rag_chain_with_source===================
first={
  context: RunnablePassthrough(),
  question: RunnablePassthrough()
} middle=[RunnableAssign(mapper={
  answer_1: PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
})] last=RunnableAssign(mapper={
  answer_2: PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
})
================rag_chain_with_source.last================
mapper={
  answer_2: PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
}

'''

rag_chain_with_source = RunnableParallel(
    {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
).assign(answer_1=prompt).assign(answer_2=prompt).pick(["question", "answer_2"])  # pick 筛选输出内容
'''
==================rag_chain_with_source.invoke(('context', 'question'))===============
text="('context', 'question'), ('context', 'question')"
=================rag_chain_with_source===================
first={
  context: RunnablePassthrough(),
  question: RunnablePassthrough()
} middle=[RunnableAssign(mapper={
  answer_1: PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
}), RunnableAssign(mapper={
  answer_2: PromptTemplate(input_variables=['context', 'question'], template='{context}, {question}')
})] last=RunnablePick(keys='answer_1')
================rag_chain_with_source.last================
keys='answer_1'

'''

print("==================rag_chain_with_source.invoke(('context', 'question'))===============")
print(rag_chain_with_source.invoke(("context", "question")))
print("=================rag_chain_with_source===================")
print(rag_chain_with_source)
print("================rag_chain_with_source.last================")
print(rag_chain_with_source.last)
