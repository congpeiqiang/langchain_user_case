from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from langchain import OpenAI, SQLDatabase

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
database = SQLDatabase(engine)

# 定义一个函数，将自然语言转换为 SQL 查询
def natural_language_to_sql(natural_language_query):
    # 示例：将自然语言查询转换为 SQL 查询
    if "recent records" in natural_language_query:
        return "SELECT * FROM mts_basket_flow_info ORDER BY timestamp DESC LIMIT 10"
    else:
        return "SELECT * FROM mts_basket_flow_info LIMIT 10"

# 用户的自然语言查询
user_query = "Show me the most recent records"

# 将自然语言查询转换为 SQL 查询
sql_query = natural_language_to_sql(user_query)

# 执行生成的 SQL 查询
result = database.run(sql_query)

# 打印查询结果
for row in result:
    print(row)
