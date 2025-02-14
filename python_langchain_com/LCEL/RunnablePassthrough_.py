# 学习视频 https://www.bilibili.com/video/BV1MH4y1V7Hh/?p=2&spm_id_from=pageDriver
# https://blog.csdn.net/qq_56591814/article/details/134602985

# RunnablePassthrough相当于占位符

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

runnable = RunnableParallel(
    passed=RunnablePassthrough(),
    extra=RunnablePassthrough.assign(mult=lambda x: x["num"] * 3),
    modified=lambda x: x["num"] + 1,
)
print("=========runnable============")
print(runnable.invoke({"num": 1, "c": "C"}))  # invoke() 入参可以是dict, 也可以是str、int等
'''
{'passed': {'num': 1}, 'extra': {'num': 1, 'mult': 3}, 'modified': 2}
'''


def ll(x):
    return lambda x: x["num"] * 3


runnable_1 = RunnableParallel(
    passed=RunnablePassthrough(),
    extra=RunnableLambda(ll),
    modified=lambda x: x["num"] + 1,
)
print("=========runnable_1============")
print(runnable_1.invoke({"num": 1}))

runnable_2 = RunnableParallel(
    passed=RunnablePassthrough(),
    extra=RunnablePassthrough(),
    modified=RunnablePassthrough(),
)
print("=========runnable_2============")
print(runnable_2.invoke(1))  # invoke() 入参可以是dict, 也可以是str、int等
'''
{'passed': 1, 'extra': 1, 'modified': 1}
'''

# 传递两个RunnablePassthrough
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv("../../.env")

llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_template("tell me a jok about {topic1} and {topic2}")
runable = (
        {"topic1": RunnablePassthrough(), "topic2": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)
print(runable.invoke(("dog", "cat")))
print("============stream===========")
for chunk in runable.stream(("dog", "cat")):
    print(chunk)

# batch()
prompt = ChatPromptTemplate.from_template("tell me a jok about {topic}")
chain = prompt | llm | StrOutputParser()
print(chain.batch([{"topic": "cat"}, {"topic": "dog"}]))

# chain并行
from langchain_core.runnables import RunnableParallel

chain1 = ChatPromptTemplate.from_template("tell me a joke about {topic}") | llm
chain2 = (
        ChatPromptTemplate.from_template("write a short (2 line) poem about {topic}")
        | llm
)
combined = RunnableParallel(joke=chain1, poem=chain2)
print(combined.invoke({"topic": "bears"}))
print(combined.batch([{"topic": "bears"}, {"topic": "cats"}]))

# RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
joke_chain = ChatPromptTemplate.from_template("讲一个笑话关于 {topic} 主题") | model
poem_chain = (ChatPromptTemplate.from_template("写两行诗关于 {topic} 主题") | model)
map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)
response = map_chain.invoke({"topic": "椅子"})
print(response)
'''
注意 RunnableParallel(joke=joke_chain, poem=poem_chain) 中的key值为 joke 和 poem，返回的结果中会以这两个值作为每个Chain的key值组织结果。返回结果如下：
{'joke': AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!"),
 'poem': AIMessage(content="In the wild's embrace, bear roams free,\nStrength and grace, a majestic decree.")}
'''
