from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import example_tasks


default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}


dag = DAG(dag_id="dag_sleep_10sx50", schedule_interval=None, default_args=default_args)

previous_task = None

with dag:
    for i in range(50):
        task = PythonOperator(
            task_id=f"task_{i}", python_callable=example_tasks.sleep_task, op_args=[10], provide_context=True
        )
        if previous_task is not None:
            task.set_upstream(previous_task)
        previous_task = task
