#airflow imports
from airflow import DAG
from airflow import models
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import PythonOperator

# other imports
from datetime import datetime, timedelta
from time import time
from multiprocessing import Pool
from multiprocessing import cpu_count

#variables
GCP_REGION=models.Variable.get('gcp_region')
GCP_LOCATION=models.Variable.get('gcp_location')
GCP_ZONE=models.Variable.get('gcp_zone')
GCP_PROJECT_ID=models.Variable.get('gcp_project')
GCP_SERVICE_ACOCUNT=models.Variable.get('service_account_composer')
GCP_SUBNETWORK_URI=models.Variable.get('gcp_subnetwork_uri')

today_date = datetime.datetime.now().strftime("%Y%m%d")
yesterday = datetime.datetime.combine(datetime.datetime.today() - datetime.timedelta(1), datetime.datetime.min.time())
# default arguments for dag
default_args = {
                'owner': 'airflow',
                'depends_on_past': False,
                'start_date': yesterday,
                #'email': ['airflow@airflow.com'],
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 1,
                'retry_delay': timedelta(minutes=3),
                'project_id': GCP_PROJECT_ID,
                'zone': GCP_ZONE,
                'region': GCP_REGION,
                'gcp_conn_id': 'google_cloud_default'
    }

def f(x):
    start_time = time.time()
    seconds = 20
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        x*x
        if elapsed_time > seconds:
            print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
            break

def CPU_test():
   processes = cpu_count()
   pool = Pool(processes)
   pool.map(f, range(processes))

with DAG(dag_id='CPU_stress_test',schedule_interval="@once",default_args=default_args) as dag:
                # dummy operators - start and end tasks
                start = DummyOperator(task_id='start')
                end = DummyOperator(task_id='end')
                # Python operator operator - CPU stress test task
                CPU_stress_test = PythonOperator(
                                             task_id="CPU_Stress_Test",
                                             python_callable=CPU_test,
                                             # op_kwargs = config,
                                             provide_context=True,
                                             dag = dag
                                )

start >> CPU_stress_test >> end

