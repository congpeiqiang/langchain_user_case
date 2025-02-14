from dotenv import load_dotenv
from langchain.utilities import SQLDatabase

load_dotenv("../../../.env")

import os

# db_user = "root"
# db_password = "admin"
# db_host = "127.0.0.1"
# db_name = "students"
# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}")
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM high_school_students LIMIT 10;"))

# from langchain_community.utilities import SQLDatabase

from langchain_community.chat_models import ChatOllama

# db = SQLDatabase.from_uri("sqlite:///Chinook.db")
db = SQLDatabase.from_uri("sqlite:///D:/software/sqlite-tools-win-x64-3460000/Chinook.db")
print(db.dialect)
print(db.table_info)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM Artist LIMIT 10;"))


from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

model = ChatOllama(model="qwen2:7b", base_url="http://192.168.25.34:11434")

print("=============提问问题转为sql================")
"=============提问问题转为sql================"
chain = create_sql_query_chain(model, db)
response = chain.invoke({"question": "How many employees are there"})
print(response)
print(db.run(response))


print("=============提问问题转为sql,并自动执行sql===============")
print("=============提问问题转为sql,并自动执行sql===============")
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(model, db)
chain = write_query | execute_query
print(chain.invoke({"question": "How many employees are there"}))


from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | model | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)

print(chain.invoke({"question": "How many employees are there"}))

"===================代理====================="
print("===================代理=====================")
# create_sql_agent
from langchain_community.agent_toolkits import create_sql_agent
agent_executor = create_sql_agent(model, db=db, agent_type="openai-tools", verbose=True)
res = agent_executor.invoke(
    {
        "input": "List the total sales per country. Which country's customers spent the most?"
    }
)
print(res)

print(agent_executor.invoke({"input": "Describe the playlisttrack table"}))