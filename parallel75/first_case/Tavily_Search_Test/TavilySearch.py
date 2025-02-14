import getpass
import os

# 单独测试Tavily
# os.environ["TAVILY_API_KEY"] = getpass.getpass()
# from langchain_community.tools.tavily_search import TavilySearchResults
# tool = TavilySearchResults()
# re=tool.invoke({"query": "What happened in the latest burning man floods"})
# print(re)

# 以Chaining方式测试Tavily
import getpass
import os
from dotenv import load_dotenv
load_dotenv("E:\code_work_space\langchain_user_case\.env")
from langchain_community.tools.tavily_search import TavilySearchResults
# os.environ["OPENAI_API_KEY"] = getpass.getpass()
print(os.environ["OPENAI_API_KEY"])
print(os.environ["TAVILY_API_KEY"])

print(getpass.getpass())
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)
print(prompt)
llm = ChatOpenAI(temperature=0)
C = llm
tavily_tool = TavilySearchResults()
tools = [tavily_tool]
agent = create_openai_functions_agent(C, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)
re=agent_executor.invoke({"input": "What happened in the latest burning man floods?"})
print("==============================Chaining=============================")
print(re)
