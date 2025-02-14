
import os
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['OPENAI_API_KEY'] = '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'

# "##################PromptTemplate###################"
# "====================================="
# from langchain import PromptTemplate #用于 PromptTemplate 为字符串提示创建模板。
# #默认情况下, PromptTemplate 使用 Python 的 str.format 语法进行模板化;但是可以使用其他模板语法（例如, jinja2 ）
# prompt_template = PromptTemplate.from_template(
#     "Tell me a {adjective} joke about {content}."
# )
# p=prompt_template.format(adjective="funny", content="chickens")
# print(p)
# '''
# Tell me a funny joke about chickens.
# '''
# "====================================="
#
#
# "====================================="
# from langchain import PromptTemplate
# prompt_template = PromptTemplate.from_template(
# "Tell me a joke"
# )
# p=prompt_template.format()#该模板支持任意数量的变量，包括无变量
# print(p)
# "====================================="
#
#
# "====================================="
# #聊天模型的提示是聊天消息列表。
# #每条聊天消息都与内容相关联，以及一个名为 role 的附加参数。例如，在 OpenAI 聊天完成 API 中，聊天消息可以与 AI 助手、人员或系统角色相关联。
# from langchain.prompts import ChatPromptTemplate
# #ChatPromptTemplate.from_messages 接受各种消息表示形式。
# template = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful AI bot. Your name is {name}."),
#     ("human", "Hello, how are you doing?"),
#     ("ai", "I'm doing well, thanks!"),
#     ("human", "{user_input}"),
# ])
#
# messages = template.format_messages(
#     name="Bob",
#     user_input="What is your name?"
# )
# print(messages)
# "====================================="
#
#
# "====================================="
# #除了使用上一个代码块中使用的（类型、内容）的 2 元组表示形式外，
# #您还可以传入 or BaseMessage 的 MessagePromptTemplate 实例。
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema.messages import SystemMessage
# from langchain.prompts.chat import HumanMessagePromptTemplate
# template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(
#             content=(
#                 "You are a helpful assistant that re-writes the user's text to "
#                 "sound more upbeat."
#             )
#         ),
#         HumanMessagePromptTemplate.from_template("{text}"),
#     ]
# )
#
# from langchain_openai import ChatOpenAI
#
# llm = ChatOpenAI()
# respose=llm(template.format_messages(text='i dont like eating tasty things.'))
#
# print(f"respose: {respose}")
# print(template.format(text='i dont like eating tasty things.'))
# "====================================="
# "====================================="
# # 您也可以只使用部分变量初始化提示，这在此工作流中通常更有意义。
# prompt = PromptTemplate(
#     template="Tell me a {adjective} joke about the day {date}",
#     input_variables=["adjective"],
#     partial_variables={"date": "20210-10-04"}
# )
# print(prompt.format(adjective="funny"))
# "====================================="


# "######################带有样例的提示词模板######################"
# "====================================="
# # 固定少量样本的提示词模板
# from langchain.prompts.few_shot import FewShotPromptTemplate
# from langchain.prompts.prompt import PromptTemplate
#
# #这里我们用字典来表示一个例子，每个示例都应该是一个字典，其中键是输入变量，值是这些输入变量的值。
# examples = [
#   {
#     "question": "Who lived longer, Muhammad Ali or Alan Turing?",
#     "answer":
# 		"""
# 		Are follow up questions needed here: Yes.
# 		"""
#   },
#   {
#     "question": "When was the founder of craigslist born?",
#     "answer":
# 		"""
# 		Are follow up questions needed here: Yes.n December 6, 1952.
# 		So the final answer is: December 6, 1952
# 		"""
#   }
# ]
# #配置一个格式化程序，该格式化程序将几个镜头示例格式化为字符串。此格式化程序应该是一个 PromptTemplate 对象。
# example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")
# print(example_prompt.format(question="Are follow up questions needed here: Yes.n December 6, 1952.", answer="Are follow up questions needed here: Yes."))
# #我们可以使用FewShotPromptTemplate来创建一个提示词模板，该模板将输入变量作为输入，并将其格式化为包含示例的提示词。
# prompt = FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=example_prompt,
#     suffix="Question: {input}",
#     input_variables=["input"]
# )
# print(prompt.format(input="Who was the father of Mary Ball Washington?"))
# "====================================="
#
# "====================================="
# "====================================="
# # 动态少量样本的提示词模板
# from langchain.prompts.few_shot import FewShotPromptTemplate
# from langchain.prompts.prompt import PromptTemplate
#
# #这里我们用字典来表示一个例子，每个示例都应该是一个字典，其中键是输入变量，值是这些输入变量的值。
# examples = [
#   {
#     "question": "Who lived longer, Muhammad Ali or Alan Turing?",
#     "answer":
# 		"""
# 		Are follow up questions needed here: Yes.
# 		"""
#   },
#   {
#     "question": "When was the founder of craigslist born?",
#     "answer":
# 		"""
# 		Are follow up questions needed here: Yes.n December 6, 1952.
# 		So the final answer is: December 6, 1952
# 		"""
#   }
# ]
# #配置一个格式化程序，该格式化程序将几个镜头示例格式化为字符串。此格式化程序应该是一个 PromptTemplate 对象。
# example_prompt = PromptTemplate(input_variables=["question", "answer"], template="Question: {question}\n{answer}")
# from langchain.prompts import SemanticSimilarityExampleSelector
# from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings
# example_selector = SemanticSimilarityExampleSelector(
#     vectorstore=vectorstore,
# 	OpenAIEmbeddings(),
# 	Chroma,
#     k=2,
# )
# #我们可以使用FewShotPromptTemplate来创建一个提示词模板，该模板将输入变量作为输入，并将其格式化为包含示例的提示词。
# prompt = FewShotPromptTemplate(
#     example_selector=examples,
#     example_prompt=example_prompt,
#     suffix="Question: {input}",
#     input_variables=["input"]
# )
# print(prompt.format(input="Who was the father of Mary Ball Washington?"))
# "====================================="



"####################序列化储存提示词#####################"
"======================================================"
#通常建议将提示存储为文件，而不是 python 代码。
# 这可以轻松共享、存储和版本提示。
# 本笔记本介绍了如何在 LangChain 中执行此操作，演练了所有不同类型的提示和不同的序列化选项。
# zh: 所有提示都是通过`load_prompt`函数加载的。
from langchain.prompts import load_prompt
#这显示了从 YAML 加载提示模板的示例。
prompt = load_prompt("promptstore/simple_prompt.yaml")
print(prompt.format(adjective="funny", content="chickens"))

#这显示了从 JSON 加载提示模板的示例。
prompt = load_prompt("promptstore/simple_prompt.json")
print(prompt.format(adjective="funny", content="chickens"))

#这显示了将模板存储在单独的文件中，然后在配置中引用它的示例。请注意，键从 template 更改为 template_path 。
prompt = load_prompt("promptstore/simple_prompt_with_template_file.json")
print(prompt.format(adjective="funny", content="chickens"))

#这显示了从 YAML 加载几个镜头示例的示例。
prompt = load_prompt("promptstore/few_shot_prompt.yaml")
print(prompt.format(adjective="funny"))

#如果您从 yaml 文件加载示例，这同样有效。
prompt = load_prompt("promptstore/few_shot_prompt_yaml_examples.yaml")
print(prompt.format(adjective="funny"))
"======================================================"