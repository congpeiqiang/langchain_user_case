from datetime import timedelta, datetime

from airflow import DAG
from airflow.utils import dates
from airflow.utils.helpers import chain
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


def default_options():
    default_args = {
        "owner": "airflow",  # 拥有者名称
        "start_date": dates.days_ago(1),  # 第一次开始执行时间
        "retries": 1,  # 失败重试次数
        "retry_delay": timedelta(seconds=5)  # 失败重试间隔
    }
    return default_args


# 定义DAG
def task1(dag):
    t = "pwd"
    # operator支持多种类型，这里使用BashOperator
    task = BashOperator(
        task_id="MyTask1",  # task_id
        bash_command=t,  # 指定要执行的命令
        dag=dag  # 指定归属的dag
    )
    return task


def hello_word():
    current_time = str(datetime.today())
    print(f"hello world at {current_time}")


def task2(dag):
    # PythonOperator
    task = PythonOperator(
        task_id="MyTask2",
        python_callable=hello_word(),
        dag=dag
    )
    return task


def task3(dag):
    t = "date"
    task = BashOperator(
        task_id="MyTask3",  # task_id
        bash_command=t,  # 指定要执行的命令
        dag=dag  # 指定归属的dag
    )
    return task


with DAG(
        "helloworlddag",
        default_args=default_options(),  # dag id
        schedule_interval="2 * * * *"
) as d:
    task1 = task1(d)
    task2 = task2(d)
    task3 = task3(d)
    chain(task1, task2, task3)  # 指定执行顺序
