import clickhouse_driver
import pandas as pd
from clickhouse_sqlalchemy import make_session
from sqlalchemy import create_engine

db_user = "weint"
db_password = "123@abcd"
df_port = 8123
db_host = "192.168.26.201"
db_name = "mts"
# # 假设你的ClickHouse服务器地址是 localhost:8123，数据库是 your_database
# ch_connection = clickhouse_driver.connect(host=db_host, port=df_port, user=db_user, password=db_password,
#                                           database='mnt')
# print(ch_connection.host)
# print(ch_connection.dialect)


# engine = create_engine(f"clickhouse://{db_user}:{db_password}@{db_host}:{df_port}/{db_name}")
# print(engine.dialect)
# print(engine.get_execution_options())
# session = make_session(engine)
# sql = 'SHOW TABLES'
# cursor = session.execute(sql)
# try:
#     fields = cursor._metadata.keys
#     df = pd.DataFrame([dict(zip(fields, item)) for item in cursor.fetchall()])
# finally:
#     cursor.close()
#     session.close()


from clickhouse_driver  import Client
from langchain.sql_database import SQLDatabase

# 配置 ClickHouse 连接
clickhouse_host = '192.168.26.201'
clickhouse_port = 8123
clickhouse_user = 'weint'
clickhouse_password = '123@abcd'
clickhouse_database = 'mts'

# 连接到 ClickHouse 数据库
client = Client(
    host=clickhouse_host,
    port=clickhouse_port,
    username=clickhouse_user,
    password=clickhouse_password,
    database=clickhouse_database
)

# 将 ClickHouse 连接包装在 SQLDatabase 中
database = SQLDatabase.from_custom(client, dialect="clickhouse")

# 定义一个函数，将自然语言转换为 SQL 查询
def natural_language_to_sql(natural_language_query):
    # 示例：将自然语言查询转换为 SQL 查询
    if "recent records" in natural_language_query:
        return "SELECT * FROM your_table ORDER BY timestamp DESC LIMIT 10"
    else:
        return "SELECT * FROM your_table LIMIT 10"

# 用户的自然语言查询
user_query = "Show me the most recent records"

# 将自然语言查询转换为 SQL 查询
sql_query = natural_language_to_sql(user_query)

# 执行生成的 SQL 查询
result = database.execute(sql_query)

# 打印查询结果
for row in result:
    print(row)
