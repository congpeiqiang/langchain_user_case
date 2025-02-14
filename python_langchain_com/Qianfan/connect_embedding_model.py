# -*- coding: utf-8 -*-
# @Time    : 2024/11/5 上午11:05
# @Author  : CongPeiQiang
# @File    : connect_embedding_model.py
# @Software: PyCharm

"""For basic init and call"""
import os

from langchain_community.embeddings import QianfanEmbeddingsEndpoint

os.environ["QIANFAN_AK"] = "L7aNz2gt2f24vImTAiXbvCCK"
os.environ["QIANFAN_SK"] = "9sHyjNal7gOxdYbXmbaYU6bW1sDUh9Dy"

embed = QianfanEmbeddingsEndpoint(model="bge_large_zh", endpoint="bge_large_zh")

res = embed.embed_documents(["hi", "world"])
for r in res:
    print(r[:8])
