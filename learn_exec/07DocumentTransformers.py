
"##################################"
# CodeTextSplitter 允许您使用多种语言支持拆分代码。导入枚举 Language 并指定语言。
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
# 支持拆分的语言
print([e.value for e in Language])
"['cpp', 'go', 'java', 'kotlin', 'js', 'ts', 'php', 'proto', 'python', 'rst', 'ruby', 'rust', 'scala', 'swift', 'markdown', 'latex', 'html', 'sol', 'csharp', 'cobol']"

# You can also see the separators used for a given language
print(RecursiveCharacterTextSplitter.get_separators_for_language(Language.PYTHON))

#下面是一个使用 PythonTextSplitter 的示例
PYTHON_CODE = """
def hello_world():
    print("Hello, World!")

# Call the function
hello_world()
"""
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=50, chunk_overlap=0
)
python_docs = python_splitter.create_documents([PYTHON_CODE])
print(python_docs)

"==========================================================="
# This is a long document we can split up.
with open('documentstore/state_of_the_union.txt') as f:
    state_of_the_union = f.read()

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 100,
    chunk_overlap  = 20,
    length_function = len,
    add_start_index = True,
)
texts = text_splitter.create_documents([state_of_the_union])
print(texts[0])
print(texts[1])
"==========================================================="

#下面是使用 Markdown 文本拆分器的示例。
markdown_text = """
# 🦜️🔗 LangChain

⚡ Building applications with LLMs through composability ⚡

## Quick Install

```bash
# Hopefully this code block isn't split
pip install langchain
```

As an open source project in a rapidly developing field, we are extremely open to contributions.
"""
md_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN, chunk_size=60, chunk_overlap=0
)
md_docs = md_splitter.create_documents([markdown_text])
print(md_docs)

"==========================================================="
# 文档相关性检索
# 导入必要的库和模块
import os
import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_transformers import LongContextReorder
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# 获取预训练的词嵌入
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 定义一组文本文档
texts = [
    "Basquetball is a great sport.",
    "Fly me to the moon is one of my favourite songs.",
    "The Celtics are my favourite team.",
    "This is a document about the Boston Celtics",
    "I simply love going to the movies",
    "The Boston Celtics won the game by 20 points",
    "This is just a random text.",
    "Elden Ring is one of the best games in the last 15 years.",
    "L. Kornet is one of the best Celtics players.",
    "Larry Bird was an iconic NBA player.",
]

# 使用这些文本文档和预训练的词嵌入创建一个检索器
retriever = Chroma.from_texts(texts, embedding=embeddings).as_retriever(
    search_kwargs={"k": 10}
)

# 定义一个查询
query = "What can you tell me about the Celtics?"

# 基于这个查询检索相关的文档，并按相关性分数排序
docs = retriever.get_relevant_documents(query)
print(docs)
