from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import example_tasks


default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}


dag = DAG(dag_id="test_1_task_10s", schedule_interval=None, default_args=default_args)


with dag:
    task = PythonOperator(task_id="task", python_callable=example_tasks.sleep_task, op_args=[10], provide_context=True)
