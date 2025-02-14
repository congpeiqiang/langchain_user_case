from dotenv import load_dotenv

load_dotenv("../../../.env")

from langchain import OpenAI, SQLDatabase
import os

db_user = "root"
db_password = "admin"
db_host = "127.0.0.1"
db_name = "students"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}")
print(db.dialect)
print(db.get_usable_table_names())
print(db.run("SELECT * FROM high_school_students LIMIT 10;"))
context = db.get_context()
print("==============context===========")
print(context)
print("===========list(context)===========")
print(list(context))

from langchain.chains.sql_database.prompt import SQL_PROMPTS
print("==========list(SQL_PROMPTS)============")
print(list(SQL_PROMPTS))

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature="0")
chain = create_sql_query_chain(llm, db)
print(chain.get_prompts()[0].pretty_print())

prompt_with_context = chain.get_prompts()[0].partial(table_info=context["table_info"])
print(prompt_with_context.pretty_repr()[:1500])