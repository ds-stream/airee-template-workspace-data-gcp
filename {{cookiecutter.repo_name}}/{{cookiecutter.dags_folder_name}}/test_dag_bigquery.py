# airflow imports
from airflow.models import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryDeleteDatasetOperator,
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryInsertJobOperator,
)
from airflow.operators.dummy_operator import DummyOperator


# other imports
from datetime import datetime, timedelta

# variables
GCP_REGION = "us-east1"
GCP_LOCATION = "Moncks Corner"
GCP_ZONE = "us-east1-d"
GCP_PROJECT_ID = "dsstream-airflowk8s"
GCP_SERVICE_ACCOUNT = "service_account_composer"
GCP_SUBNETWORK_URI = "gcp_subnetwork_uri"

today_date = datetime.now().strftime("%Y%m%d")
yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

# default arguments for dag
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": yesterday,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
    "project_id": GCP_PROJECT_ID,
    "zone": GCP_ZONE,
    "region": GCP_REGION,
    "gcp_conn_id": "google_cloud_default",
}

with DAG(dag_id="test_dag_bigquery", schedule_interval=None, default_args=default_args) as dag:

    # dummy operators - start and end tasks
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    dataset = "dag_tests"
    table = "test_table"

    table_schema = [
        {"name": "first", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "second", "type": "STRING", "mode": "NULLABLE"},
    ]
    insert_query = f"""insert {dataset}.{table} values
        (1, 'some value'),
        (2, 'other value'),
        (3, 'other value 2'),
        (4, 'other value 3'),
        (5, 'other value 4');
        """

    delete_dataset = BigQueryDeleteDatasetOperator(task_id="delete_dataset", dataset_id=dataset, delete_contents=True)

    create_dataset = BigQueryCreateEmptyDatasetOperator(task_id="create_dataset", dataset_id=dataset)

    create_table = BigQueryCreateEmptyTableOperator(
        task_id="create_table", dataset_id=dataset, table_id=table, schema_fields=table_schema
    )

    insert_query_job = BigQueryInsertJobOperator(
        task_id="insert_query_job",
        configuration={
            "query": {
                "query": insert_query,
                "useLegacySql": False,
            }
        },
    )

start >> delete_dataset >> create_dataset >> create_table >> insert_query_job >> end
