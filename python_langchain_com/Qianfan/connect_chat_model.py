# -*- coding: utf-8 -*-
# @Time    : 2024/10/31 下午4:07
# @Author  : CongPeiQiang
# @File    : connect_model.py
# @Software: PyCharm
"""For basic init and call"""
import os

from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.language_models.chat_models import HumanMessage

os.environ["QIANFAN_AK"] = "L7aNz2gt2f24vImTAiXbvCCK"
os.environ["QIANFAN_SK"] = "9sHyjNal7gOxdYbXmbaYU6bW1sDUh9Dy"

chatBot = QianfanChatEndpoint(
    streaming=True,
    model="ERNIE-4.0-8K",
)

messages = [HumanMessage(content="Hello")]
out = chatBot.invoke(messages)
print(out)

# 批量推理
out = chatBot.batch([messages])
print(out)

# 流式推理
try:
    for chunk in chatBot.stream(messages):
        print(chunk.content, end="", flush=True)
except TypeError as e:
    print("")