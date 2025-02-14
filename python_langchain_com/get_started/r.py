# -*- coding: utf-8 -*-
# @Time    : 2024/11/9 下午3:03
# @Author  : CongPeiQiang
# @File    : r.py
# @Software: PyCharm

from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-ks2Pwy2gt7aIvulGSHpyM05hjEirSISxkrpKFFutCtHZJye4",
    base_url="https://api.chatanywhere.tech/v1"
    # base_url="https://api.chatanywhere.org/v1"
)
res = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "你好，我是谁？"}
    ],
)
print(res.choices[0].message.content)
