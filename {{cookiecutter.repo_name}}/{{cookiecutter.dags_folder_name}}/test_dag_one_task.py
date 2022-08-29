from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from pathlib import Path
import sys

path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

import example_tasks

default_args = {
    "owner": "Airflow",
    "start_date": datetime(2021, 1, 1),
}


dag = DAG(dag_id="test_1_task", schedule_interval=None, default_args=default_args)


with dag:
    task = PythonOperator(
        task_id="task", python_callable=example_tasks.sleep_task, op_args=[100], provide_context=True
    )
