from operator import itemgetter
from dotenv import load_dotenv

load_dotenv("../../.env")

ls = [1, 2, 3, 4]
print(itemgetter(0)(ls))  # 1
print(itemgetter(3, 0, 1)(ls))

solider = dict(a="1", b=2)
print(itemgetter("a")(solider))

# itemgetter 与 RunnableLambda结合的高级用法
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from operator import itemgetter

def length_function(text):
    return len(text)


def _multiple_length_function(text1, text2):
    return len(text1) * len(text2)


def multiple_length_function(dict):
    return _multiple_length_function(dict["text1"], dict["text2"])


prompt = ChatPromptTemplate.from_template("what is (a) + (b)")
print("=========prompt===========")
print(prompt)
model = ChatOpenAI()

chain = (
        {
            "a": itemgetter("foo") | RunnableLambda(length_function),
            "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")} | RunnableLambda(multiple_length_function)
        }
        | prompt
        | model
)

print(chain.invoke({"foo": "bar", "bar": "gah"}))
