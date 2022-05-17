from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import example_tasks

default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}


dag = DAG(dag_id="test_10_task_2", schedule_interval=None, default_args=default_args)


with dag:
    for i in range(10):
        task = PythonOperator(
            task_id=f"task_{i}", python_callable=example_tasks.sleep_task, op_args=[100], provide_context=True
        )
