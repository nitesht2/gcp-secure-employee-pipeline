import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator
from airflow.providers.google.cloud.hooks.datafusion import PipelineStates

# Config via env vars (set as Airflow Variables / Composer env) — nothing
# project-specific or personal is hard-coded.
ALERT_EMAIL = os.environ.get("ALERT_EMAIL", "alerts@example.com")
GCP_REGION = os.environ.get("GCP_REGION", "us-west1")
DATAFUSION_INSTANCE = os.environ.get("DATAFUSION_INSTANCE", "datafusion-dev")
DATAFUSION_PIPELINE = os.environ.get("DATAFUSION_PIPELINE", "ETL Data Pipeline")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 18),
    'depends_on_past': False,
    'email': [ALERT_EMAIL],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'employee_secure_daily_pipeline',
    default_args=default_args,
    description='Generate synthetic employee data, then run the Data Fusion PII-protection pipeline',
    schedule='@daily',
    catchup=False,
    tags=['gcp', 'pii', 'datafusion'],
) as dag:

    run_script_task = BashOperator(
        task_id='extract_data',
        bash_command='python /home/airflow/gcs/dags/scripts/extract.py',
    )

    start_pipeline = CloudDataFusionStartPipelineOperator(
        task_id='start_datafusion_pipeline',
        location=GCP_REGION,
        pipeline_name=DATAFUSION_PIPELINE,
        instance_name=DATAFUSION_INSTANCE,
        pipeline_timeout=900,
        success_states=[PipelineStates.COMPLETED],
    )

    # Orchestration
    run_script_task >> start_pipeline
