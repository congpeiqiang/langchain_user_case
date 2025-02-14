# from langchain.chat_models import ChatOpenAI
# import os
#
# os.environ['OPENAI_API_KEY'] = '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'
#
# #导入消息模版
# from langchain.prompts import (
#     ChatPromptTemplate,
#     MessagesPlaceholder,
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate,
# )
# #导入chains模块，这里用conversationChain
# from langchain.chains import ConversationChain
# #导入memory模块，这里用ConversationBufferMemory
# from langchain.memory import ConversationBufferMemory
# # LLM
# llm = ChatOpenAI()
# # Prompt
# prompt = ChatPromptTemplate.from_messages([
#         SystemMessagePromptTemplate.from_template("You are a nice chatbot having a conversation with a human."),
#  # 这里的`variable_name` 必须和下面的`memory_key`一致
#         MessagesPlaceholder(variable_name="chat_history"),
#         HumanMessagePromptTemplate.from_template("{input}")
#     ]
# )
# #这里用CoversationBufferMemory
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# conversation = ConversationChain(
#     llm=llm,
#     prompt=prompt,
#     verbose=True,
#     memory=memory)
# respose=conversation.run({"input": "hi, nice to meet you"})
# print(respose)



"#######################################################3333"
#设置代理
import os
os.environ['OPENAI_API_KEY'] = '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'
# 首先，让我们加载将用于控制代理的语言模型。
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 接下来，让我们定义一些要使用的工具。让我们编写一个非常简单的 Python 函数来计算传入的单词的长度。
from langchain.agents import tool


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

tools = [get_word_length]

'''
现在让我们创建提示。由于 OpenAI 函数调用针对工具使用进行了微调，因此我们几乎不需要任何关于如何推理或如何输出格式的说明。
我们将只有两个输入变量： input 和 agent_scratchpad , input 应为包含用户目标的字符串。
 agent_scratchpad 应该是包含先前代理工具调用和相应工具输出的消息序列。
'''
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

'''
代理如何知道它可以使用哪些工具？在本例中，我们依赖于 OpenAI 函数调用 LLM，它将函数作为单独的参数，并经过专门训练，可以知道何时调用这些函数。
要将我们的工具传递给代理，我们只需要将它们格式化为 OpenAI 函数格式并将它们传递给我们的模型。（通过对函数进行绑定操作，我们确保每次调用模型时都会传入它们。
'''
from langchain.tools.render import format_tool_to_openai_function

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

'''
将这些部分放在一起，我们现在可以创建代理。
我们将导入最后两个实用程序函数：一个组件用于格式化中间步骤（代理操作、工具输出对）以输入可发送到模型的消息，以及一个用于将输出消息转换为代理操作/代理完成的组件。
'''
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

# 现在我们有了代理，让我们来玩吧！让我们传入一个简单的问题和空的中间步骤，看看它返回了什么：
respose=agent.invoke({"input": "how many letters in the word educa?", "intermediate_steps": []})
print(respose)

"=======================定义运行时=========================="
from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
respose=agent_executor.invoke({"input": "how many letters in the word educa?"})
print(respose)

"=======================添加历史记录内存=========================="
from langchain.prompts import MessagesPlaceholder
MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but bad at calculating lengths of words.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
# 然后，我们可以设置一个列表来跟踪聊天记录
from langchain_core.messages import AIMessage, HumanMessage

chat_history = []

# 然后我们可以把它们放在一起！
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# 运行时，我们现在需要将输入和输出作为聊天记录进行跟踪
input1 = "how many letters in the word educa?"
result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
chat_history.extend(
    [
        HumanMessage(content=input1),
        AIMessage(content=result["output"]),
    ]
)
respose=agent_executor.invoke({"input": "is that a real word?", "chat_history": chat_history})
print(respose)
