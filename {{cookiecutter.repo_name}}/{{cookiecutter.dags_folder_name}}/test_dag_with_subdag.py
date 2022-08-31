from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.subdag import SubDagOperator
from pathlib import Path
import sys

path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

import example_tasks
from test_subdag_factory import load_subdag


default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}
dag_id = "test_dag_with_subdag"
dag = DAG(dag_id=dag_id, schedule_interval=None, default_args=default_args)

with dag:
    t1 = PythonOperator(task_id="task1", python_callable=example_tasks.sleep_task, op_args=[10], provide_context=True)

    load_tasks = SubDagOperator(
        task_id="load_tasks",
        subdag=load_subdag(parent_dag_name=dag_id, parent_task_name="load_tasks", default_args=default_args),
        default_args=default_args,
        dag=dag,
    )

    t1 >> load_tasks
