from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['OPENAI_API_KEY'] = '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'

"====================================="
# llm = OpenAI()
# chat_model = ChatOpenAI()
# print(chat_model.predict("hi!"))
# print(llm.predict("hi!"))
"====================================="

from langchain.schema import HumanMessage
chat_model = ChatOpenAI()
text = "What would be a good company name for a company that makes colorful socks?"
messages = [HumanMessage(content=text)]
respose=chat_model.invoke(messages, temperature=0)
print(respose)
llm = OpenAI()
respose=llm.invoke(messages, temperature=0)
print(respose)
"====================================="

"====================================="