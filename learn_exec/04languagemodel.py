
#大型语言模型（LLM）是LangChain的核心组件。LangChain不提供自己的LLM，而是提供了一个标准接口，用于与许多不同的LLM进行交互。
# https://python.langchain.com/docs/modules/model_io/models/llms/

# import os
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ['OPENAI_API_KEY'] = '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'
#
# from langchain_openai import OpenAI
# llm = OpenAI()
#
# #可以直接调用
# re=llm.invoke("给我讲一个笑话")
# print(re)
#
# #enerate: 批量调用，输出更丰富
# llm_result = llm.generate(["给我讲个笑话", "给我讲个诗词"]*2)
# print(len(llm_result.generations))
# print(llm_result.generations[0])
#
# #您还可以访问返回的提供程序特定信息。此信息在提供商之间没有标准化。
# print(llm_result.llm_output)

# 异步接口
'''
LangChain通过利用asyncio库为LLM提供异步支持。 异步支持对于同时调用多个 LLM 特别有用，因为这些调用是网络绑定的。
目前、 OpenAI PromptLayerOpenAI ChatOpenAI 、 Anthropic 和 Cohere 受支持，但对其他 LLM 的异步支持已在路线图上。
您可以使用该方法 agenerate 异步调用 OpenAI LLM。
'''
# import openai
# import os
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ['OPENAI_API_KEY'] = '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'
# # 导入所需的模块
# import time  # 用于计时
# import asyncio  # 用于处理异步编程
#
# from langchain.llms import OpenAI  # 从langchain.llms库导入OpenAI类
#
# # 定义一个串行（同步）方式生成文本的函数
# def generate_serially():
#     llm = OpenAI(temperature=0.9)  # 创建OpenAI对象，并设置temperature参数为0.9
#     for _ in range(10):  # 循环10次
#         resp = llm.generate(["Hello, how are you?"])  # 调用generate方法生成文本
#         print(resp.generations[0][0].text)  # 打印生成的文本
#
# # 定义一个异步生成文本的函数
# async def async_generate(llm):
#     resp = await llm.agenerate(["Hello, how are you?"])  # 异步调用agenerate方法生成文本
#     print(resp.generations[0][0].text)  # 打印生成的文本
#
# # 定义一个并发（异步）方式生成文本的函数
# async def generate_concurrently():
#     llm = OpenAI(temperature=0.9)  # 创建OpenAI对象，并设置temperature参数为0.9
#     tasks = [async_generate(llm) for _ in range(10)]  # 创建10个异步任务
#     await asyncio.gather(*tasks)  # 使用asyncio.gather等待所有异步任务完成
#
# # 记录当前时间点
# s = time.perf_counter()
# # 使用异步方式并发执行生成文本的任务
# # 如果在Jupyter以外运行此代码，使用 asyncio.run(generate_concurrently())
# generate_concurrently()
# # 计算并发执行所花费的时间
# elapsed = time.perf_counter() - s
# print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." + "\033[0m")
#
# # 记录当前时间点
# s = time.perf_counter()
# # 使用同步方式串行执行生成文本的任务
# generate_serially()
# # 计算串行执行所花费的时间
# elapsed = time.perf_counter() - s
# print("\033[1m" + f"Serial executed in {elapsed:0.2f} seconds." + "\033[0m")




"#################大语言模型的序列化配置###################"
# import os
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ['OPENAI_API_KEY'] = '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'
# from langchain.llms import OpenAI
# from langchain.llms.loading import load_llm
# llm = load_llm("llmstore/llm.json")
# print(llm)
#
# llm = load_llm("llmstore/llm.yaml")
# print(llm)
#
# # Saving
# llm.save("llmsave.json")
# llm.save("llmsave.yaml")


"##################大语言模型的流式处理响应###################"
# import os
# os.environ['OPENAI_API_KEY'] = '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'
# from langchain.llms import OpenAI
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#
#
# llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
# resp = llm("Write me a song about sparkling water.")
# print(resp)
#
# resp1 = llm.generate(["Write me a song about sparkling water."])
# print(resp1)


"##################大语言模型的跟踪令牌使用情况#######################"
"======================================"
import os
os.environ['OPENAI_API_KEY'] = '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'
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
llm = OpenAI(n=2, best_of=2,cache = None)

with get_openai_callback() as cb:
    result = llm("讲个笑话")
    print(cb)
"======================================"
# 如果使用具有多个步骤的链或代理，它将跟踪所有这些步骤。
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
llm = OpenAI(temperature=0)
tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)
with get_openai_callback() as cb:
    response = agent.run(
        "王菲现在的年龄是多少？"
    )
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
"======================================"