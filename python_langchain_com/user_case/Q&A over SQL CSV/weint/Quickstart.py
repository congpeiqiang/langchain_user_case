from dotenv import load_dotenv

'''
唯因特 追随项目 数据库clickhouse
IP: 192.168.26.201
端口: 8123
用户名: weint
密码:123@abcd
数据库名称:mnt
'''

from langchain import OpenAI, SQLDatabase
import os
from sqlalchemy.engine import URL

load_dotenv(r"E:\code_work_space\langchain_user_case\.env")
# os.environ["http_proxy"] = "http://localhost:7890"
# os.environ["https_proxy"] = "http://localhost:7890"

from sqlalchemy import create_engine
from clickhouse_sqlalchemy import make_session

# db_user = "weint"
# db_password = "123@abcd"
# df_port = 8123
# db_host = "192.168.26.201"
# db_name = "mts"
#
# db = create_engine(f"clickhouse+http://{db_user}:{db_password}@{db_host}:{df_port}/{db_name}")
# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}")
# db = SQLDatabase.from_uri(f"clickhouse+http://{db_user}:{db_password}@{db_host}:{df_port}/{db_name}")

clickhouse_host = '192.168.26.201'
clickhouse_port = 8123
clickhouse_user = 'weint'
clickhouse_password = '123@abcd'
clickhouse_database = 'mts'

# 配置 ClickHouse 连接
clickhouse_url = URL.create(
    drivername='clickhouse+http',
    host=clickhouse_host,
    port=clickhouse_port,
    username=clickhouse_user,
    password=clickhouse_password,
    database=clickhouse_database
)

# 创建 SQLAlchemy 引擎
engine = create_engine(clickhouse_url)

# 创建 SQLDatabase 实例
db = SQLDatabase(engine)

print(db.dialect)
print(db.get_usable_table_names())

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(openai_api_base="http://192.168.60.78:11434/api/chat", model="qwen2:0.5b", temperature=0)

from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

# 笔记本环境
model = ChatOllama(model="qwen2:7b", base_url="http://192.168.25.34:11434")

# 34服务器环境
# model = ChatOllama(model="llama3:8b",
#                    base_url="http://192.168.25.34:11434")  # 注意: 此处不是ollama,若是ollama,后面会报错 This output parser only works on ChatGeneration output

chain = create_sql_query_chain(model, db)

print("============================")
response = chain.invoke({"question": "数据库表mts_equipment_running,一共有多少条数据？"})
print("数据库表mts_equipment_running,一共有多少条数据？ 转为sql")
print(response)
print(db.run("SELECT COUNT(*) FROM mts_equipment_running;"))
# chain.get_prompts()[0].pretty_print()

print("============================")
"自然语言转为sql,并自动执行sql "
# from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# execute_query = QuerySQLDataBaseTool(db=db)
# write_query = create_sql_query_chain(model, db)
# chain = write_query | execute_query
# response = chain.invoke({"question": "数据库表mts_equipment_running,一共有多少条数据？"})
# print(response)


print("============================")
# create_sql_agent
from langchain_community.agent_toolkits import create_sql_agent

agent_executor = create_sql_agent(model, db=db, agent_type="openai-tools", verbose=True)
# res = agent_executor.invoke(
#     {
#         "input": "数据库表mts_equipment_running,一共有多少条数据？,请直接给出答案"
#     }
# )

res = agent_executor.invoke(
    {
        "input": "How many rows of data in the database table mts_flow_log, Please give the answer directly"
    }
)

print("数据库mts中, 表mts_flow_log中,一共有多少条数据？,请直接给出答案")
print(res)

print("============================")
# print("数据库表mts_equipment_running,一共有多少条数据？")
# res = agent_executor.invoke({"input": "Describe the mts_equipment_running table"})
# print(res)