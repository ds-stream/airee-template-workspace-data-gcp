import time
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup


def test(**context):
    time.sleep(10)


default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}


dag = DAG(dag_id="dag_with_task_group", schedule_interval=None, default_args=default_args)

with dag:
    for i in range(3):
        with TaskGroup(group_id=f"group_{i}") as tg:
            t1 = PythonOperator(task_id="task1", python_callable=test, provide_context=True)
            t2 = PythonOperator(task_id="task2", python_callable=test, provide_context=True)
            t1 >> t2
