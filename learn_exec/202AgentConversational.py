import os
from dotenv import load_dotenv

load_dotenv("E:\code_work_space\langchain_user_case\.env")
os.environ['OPENAI_API_KEY'] = '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'
print(os.environ['SERPAPI_API_KEY'])
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper

search = SerpAPIWrapper()
tools = [
    Tool(
        name="当前搜索",
        func=search.run,
        description="当您需要回答有关时事或世界现状的问题时非常有用",
    ),
]
llm = OpenAI(temperature=0)

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent

prompt = hub.pull("hwchase17/react-chat")

with open('promptstore/hwchase17/react-chat.txt', 'w') as file:
    file.write(str(prompt))

agent = create_react_agent(llm, tools, prompt)

memory = ConversationBufferMemory(memory_key="chat_history")
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# res=agent_executor.invoke({"input": "刘德华在2023年12月30号有什么电影将会在中国上映?"})["output"]
# print(res)

res = agent_executor.invoke(
    {

        "input": "what's my name? Only use a tool if needed, otherwise respond with Final Answer",
        # Notice that chat_history is a string, since this prompt is aimed at LLMs, not chat models
        "chat_history": "Human: Hi! My name is Bob\nAI: Hello Bob! Nice to meet you",
    }
)
print(res)
