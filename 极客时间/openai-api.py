import openai
import os
from dotenv import load_dotenv

load_dotenv("../.env")
openai.api_key = os.environ["OPENAI_API_KEY"]
# os.environ["http_proxy"] = "http://localhost:7890"
# os.environ["https_proxy"] = "http://localhost:7890"

# 查询openai model 列表
print(openai.Model.list())

# 获取模型具体信息
print(openai.Model.retrieve("gpt-3.5-turbo"))

