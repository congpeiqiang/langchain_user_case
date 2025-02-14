import sys

sys.path.insert(0, '/mydata/intelligent-crystal-pulling-yuze/描述性分析/smart_pulling')

import logging
import datetime
import threading
import time
import dataSplit
import split_file_1
from concurrent.futures import ThreadPoolExecutor, Future
import daily_prod_record_combine

from airflow import DAG
from airflow.utils import dates
from airflow.utils.helpers import chain
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime

data = "天合_20240601-20240721"
# 数据源
source_base_path = "/mydata/intelligent-crystal-pulling-yuze/数据清理-拆分/天合/resultData_20240601-20240721"

# 中间输出结果
point_data_by_stove_path_record = f"/mydata/intelligent-crystal-pulling-yuze/描述性分析/smart_pulling/output/{data}/record"
point_data_by_stove_path_pro_record = f"/mydata/intelligent-crystal-pulling-yuze/描述性分析/smart_pulling/output/{data}/各炉台数据"

# 最终输出结果
point_data_by_stove_path_combined_prod_record = f"/mydata/intelligent-crystal-pulling-yuze/描述性分析/smart_pulling/output/mydata/intelligent-crystal-pulling-yuze/描述性分析/smart_pulling/{data}/combined_prod_record"


def beijing(sec, what):
    beijing_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return beijing_time.timetuple()


def default_options():
    default_args = {
        "owner": "airflow",  # 拥有者名称
        "start_date": dates.days_ago(1),  # 第一次开始执行时间
        "retries": 1,  # 失败重试次数
        "retry_delay": timedelta(seconds=5)  # 失败重试间隔
    }
    return default_args


# 定义DAG
def dataSplit_task(dag):
    # PythonOperator
    task = PythonOperator(
        task_id="dataSplit_task",
        python_callable=dataSplit._dir,
        depends_on_past=False,
        op_kwargs={
            'base_path': source_base_path,
            'point_data_by_stove_path': point_data_by_stove_path_record
        },
        dag=dag
    )
    return task


def split_file_1_task(dag):
    # PythonOperator
    task = PythonOperator(
        task_id="split_file_1_task",
        python_callable=split_file_1.split_file,
        depends_on_past=True,
        op_kwargs={
            'point_data_by_stove_path_record': point_data_by_stove_path_record,
            'point_data_by_stove_path_pro_record': point_data_by_stove_path_pro_record
        },
        dag=dag
    )
    return task


def daily_prod_record_combine_task(dag):
    # PythonOperator
    task = PythonOperator(
        task_id="daily_prod_record_combine_task",
        python_callable=daily_prod_record_combine.combine_prod_record,
        depends_on_past=True,
        op_kwargs={
            'base_dir': point_data_by_stove_path_pro_record,
            'point_data_by_stove_path_combined_prod_record': point_data_by_stove_path_combined_prod_record
        },
        dag=dag
    )
    return task


with DAG(
        "smart_pulling",
        default_args=default_options(),  # dag id
        schedule_interval="9 0 * * *"
) as d:
    dataSplit_task = dataSplit_task(d)
    split_file_1_task = split_file_1_task(d)
    daily_prod_record_combine_task = daily_prod_record_combine_task(d)
    chain(dataSplit_task, split_file_1_task, daily_prod_record_combine_task)  # 指定执行顺序
