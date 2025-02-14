
"#################输出解析器####################"
"==================================="
# import os
# os.environ['OPENAI_API_KEY'] = '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'
#
# #这段代码的主要目的是使用一个预训练的语言模型从OpenAI来生成并验证一个笑话。
# # 导入必要的模块和类
# from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
# from langchain_community.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.output_parsers import PydanticOutputParser
# from pydantic import BaseModel, Field, field_validator
# from typing import List
#
# # 定义模型名称和温度（影响模型的随机性）
# temperature = 0.0
#
# # 初始化OpenAI模型
# model = OpenAI(temperature=temperature)
#
# # 定义想要的数据结构，这里是一个笑话的结构，包含设置和冷笑话
# class Joke(BaseModel):
#     setup: str = Field(description="question to set up a joke")  # 笑话的设置部分
#     punchline: str = Field(description="answer to resolve the joke")  # 笑话的冷笑话部分
#
#     # 使用Pydantic添加自定义验证逻辑，确保设置部分以问号结束
#     @field_validator('setup')
#     def question_ends_with_question_mark(cls, field):
#         if field[-1] != '？':
#             raise ValueError("Badly formed question!")
#         return field
#
# # 设置一个解析器，并将指令注入到提示模板中
# parser = PydanticOutputParser(pydantic_object=Joke)
#
# # 定义提示模板
# prompt = PromptTemplate(
#     template="Answer the user query.\n{format_instructions}\n{query}\n",
#     input_variables=["query"],
#     partial_variables={"format_instructions": parser.get_format_instructions()}
# )
#
# # 定义一个查询，目的是提示语言模型填充上述数据结构
# joke_query = "给我用中文讲个笑话."
#
# # 格式化提示
# _input = prompt.format_prompt(query=joke_query)
#
# # 使用模型生成输出
# output = model(_input.to_string())
# print(output)
# # 使用解析器解析输出
# p=parser.parse(output)
# print(p)
"==================================="

# 列表解析器
# 当您想要返回逗号分隔项的列表时，可以使用此输出分析器
# 导入必要的模块和类
import os
os.environ['OPENAI_API_KEY'] = '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'
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

# 初始化一个解析由逗号分隔的列表的解析器
output_parser = CommaSeparatedListOutputParser()

# 获取解析器的格式指令
format_instructions = output_parser.get_format_instructions()

# 定义提示模板，用于生成关于特定主题的由逗号分隔的列表
prompt = PromptTemplate(
    template="List five {subject}.\n{format_instructions}",
    input_variables=["subject"],
    partial_variables={"format_instructions": format_instructions}
)

# 初始化OpenAI模型，温度设置为0（生成的回答将更加确定，少有随机性）
model = OpenAI(temperature=0)

# 格式化提示，这里的主题是“ice cream flavors”（冰淇淋口味）
_input = prompt.format(subject="冰淇淋口味")

# 使用模型生成输出
output = model(_input)
print(output)
# 使用解析器解析输出
p=output_parser.parse(output)
print(p)