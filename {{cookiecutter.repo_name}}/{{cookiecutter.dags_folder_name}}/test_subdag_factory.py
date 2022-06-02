from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

import example_tasks


def load_subdag(parent_dag_name: str, parent_task_name: str, default_args: dict):

    subdag = DAG(dag_id=f"{parent_dag_name}.{parent_task_name}", schedule_interval=None, default_args=default_args)

    with subdag:
        previous_task = None

        for i in range(3):
            task = PythonOperator(
                task_id=f"task_{i}", python_callable=example_tasks.sleep_task, op_args=[10], provide_context=True
            )

            if previous_task is not None:
                task.set_upstream(previous_task)
            previous_task = task

    return subdag
