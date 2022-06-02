# airflow imports
from airflow.models import DAG
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.dummy_operator import DummyOperator

# other imports
from datetime import datetime
from datetime import timedelta
import logging

# variables
GCP_REGION = "us-east1"
GCP_LOCATION = "Moncks Corner"
GCP_ZONE = "us-east1-d"
GCP_PROJECT_ID = "gcp_project"
GCP_SERVICE_ACOCUNT = "service_account_composer"
GCP_SUBNETWORK_URI = "gcp_subnetwork_uri"

today_date = datetime.now().strftime("%Y%m%d")
# Public data set - 569,15 KB in size
table_name_baseball = "bigquery-public-data.baseball.schedules"
table_name_tsunami = "bigquery-public-data.noaa_tsunami.historical_source_event"
table_name_moon_phases = "bigquery-public-data.moon_phases.moon_phases"
yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())
# default arguments for dag
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": yesterday,
    #'email': ['airflow@airflow.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
    "project_id": GCP_PROJECT_ID,
    "zone": GCP_ZONE,
    "region": GCP_REGION,
    "gcp_conn_id": "google_cloud_default",
}

with DAG(dag_id="test_dag_expanded", schedule_interval=None, default_args=default_args) as dag:
    # dummy operators - start and end tasks
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")
    # logging process step
    logging.error("trying to bq_query: ")
    logging.error("table name: " + table_name_baseball)
    logging.error("table name: " + table_name_tsunami)
    logging.error("table name: " + table_name_moon_phases)
    # sql to execute on BQ
    sql_baseball = f"SELECT * FROM `{table_name_baseball}` LIMIT 5"
    sql_tsunami = f"SELECT * FROM `{table_name_tsunami}` LIMIT 5"
    sql_moon_phases = f"SELECT * FROM `{table_name_moon_phases}` LIMIT 5"
    # BQ operator - big query task
    bq_query_baseball = BigQueryOperator(
        task_id="bq_query_select_public_dataset_baseball",
        use_legacy_sql=False,
        sql=sql_baseball,
        depends_on_past=False,
        dag=dag,
    )
    bq_query_tsunami = BigQueryOperator(
        task_id="bq_query_select_public_dataset_tsunami",
        use_legacy_sql=False,
        sql=sql_tsunami,
        depends_on_past=False,
        dag=dag,
    )
    bq_query_moon_phases = BigQueryOperator(
        task_id="bq_query_select_public_dataset_moon_phases",
        use_legacy_sql=False,
        sql=sql_moon_phases,
        depends_on_past=False,
        dag=dag,
    )
start >> bq_query_baseball >> bq_query_tsunami >> bq_query_moon_phases >> end
