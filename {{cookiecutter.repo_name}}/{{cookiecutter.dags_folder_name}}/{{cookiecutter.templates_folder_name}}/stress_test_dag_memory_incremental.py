# airflow imports
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# other imports
from datetime import datetime
from time import time
import psutil


def eat_mem_test():
    # size [one MB]
    MB = 1024 * 1024
    # MB to add in each step
    chunk_size = 512
    # duration of each step
    runtime = 60

    # run test
    for i in range(20):
        size = chunk_size * MB * i
        print(f"{size/MB} MB used", psutil.virtual_memory())
        a = "a" * (size)

        timeout = time() + runtime
        while True:
            if time() > timeout:
                break


dag = DAG(
    dag_id="stress_test_dag_memory_incremental",
    description="memory stress dag",
    schedule_interval=None,
    start_date=datetime(2022, 4, 20),
    catchup=False,
)

mem_stress_test = PythonOperator(task_id="Memory_Stress_Test", python_callable=eat_mem_test, dag=dag)

mem_stress_test
