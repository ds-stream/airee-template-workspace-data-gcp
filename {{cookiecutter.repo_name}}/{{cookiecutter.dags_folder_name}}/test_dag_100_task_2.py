from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from pathlib import Path
import sys

path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

import example_tasks


default_args = {
    "owner": 'Airflow',
    "start_date": datetime(2022, 1, 1)
}


dag = DAG(dag_id="test_100_task_2", schedule_interval=None, default_args=default_args)


with dag:
    for i in range(100):
        task = PythonOperator(
            task_id=f"task_{i}", python_callable=example_tasks.sleep_task, op_args=[100], provide_context=True
        )
