# airflow imports
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# other imports
from datetime import datetime
import threading


def loopy(num):
    """
    function to loop for CPU test
    """
    for i in range(num):
        hash(i + num)


def CPU_test():
    # creating thread
    t1 = threading.Thread(target=loopy, args=(100000000,))
    t2 = threading.Thread(target=loopy, args=(100000000,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()


dag = DAG(
    dag_id="stress_test_dag_cpu",
    description="CPU stress dag",
    schedule_interval=None,
    start_date=datetime(2022, 4, 20),
    catchup=False,
)

CPU_stress_test = PythonOperator(task_id="CPU_Stress_Test", python_callable=CPU_test, dag=dag)

CPU_stress_test_1 = PythonOperator(task_id="CPU_Stress_Test_1", python_callable=CPU_test, dag=dag)

CPU_stress_test_2 = PythonOperator(task_id="CPU_Stress_Test_2", python_callable=CPU_test, dag=dag)

CPU_stress_test_3 = PythonOperator(task_id="CPU_Stress_Test_3", python_callable=CPU_test, dag=dag)

CPU_stress_test_4 = PythonOperator(task_id="CPU_Stress_Test_4", python_callable=CPU_test, dag=dag)

CPU_stress_test_5 = PythonOperator(task_id="CPU_Stress_Test_5", python_callable=CPU_test, dag=dag)

CPU_stress_test_6 = PythonOperator(task_id="CPU_Stress_Test_6", python_callable=CPU_test, dag=dag)

start = DummyOperator(task_id="start")
stop = DummyOperator(task_id="stop")

(
    start
    >> [
        CPU_stress_test,
        CPU_stress_test_1,
        CPU_stress_test_2,
        CPU_stress_test_3,
        CPU_stress_test_4,
        CPU_stress_test_5,
        CPU_stress_test_6,
    ]
    >> stop
)
