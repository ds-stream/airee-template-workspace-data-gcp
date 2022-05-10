import time
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.subdag import SubDagOperator

from subdag_factory import load_subdag


def test(**context):
    time.sleep(10)


default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}

dag = DAG(dag_id="dag_with_subdag", schedule_interval=None, default_args=default_args)

with dag:
    t1 = PythonOperator(task_id="task1", python_callable=test, provide_context=True)

    load_tasks = SubDagOperator(
        task_id="load_tasks",
        subdag=load_subdag(
            parent_dag_name="dag_with_subdag", parent_task_name="load_tasks", default_args=default_args
        ),
        default_args=default_args,
        dag=dag,
    )

    t1 >> load_tasks
