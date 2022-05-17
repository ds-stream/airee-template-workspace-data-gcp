# airflow imports
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# other imports
from datetime import datetime
from time import time


def eat_mem_test():
    # time to run test in seconds
    runtime = 120
    # size [one GB]
    GB = 1024 * 1024 * 1024
    # set the size to test - integer number
    size = 2
    a = "a" * (size * GB)
    # set time out
    timeout = time() + runtime
    # run test
    while True:
        if time() > timeout:
            break


dag = DAG(
    dag_id="memory_stress_dag",
    description="memory stress dag",
    schedule_interval=None,
    start_date=datetime(2022, 4, 20),
    catchup=False,
)

mem_stress_test = PythonOperator(task_id="Memory_Stress_Test", python_callable=eat_mem_test, dag=dag)

mem_stress_test
