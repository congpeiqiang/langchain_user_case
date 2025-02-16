import os

from langchain_openai import ChatOpenAI
# 为了支持异步调用
import asyncio
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话")
print(type(prompt), prompt)
model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()
chain = prompt | model | parser


async def async_stream():
    async for chunk in chain.astream({"topic": "鹦鹉"}):
        print(chunk, end="|", flush=True)


# 运行异步流处理
asyncio.run(async_stream())
