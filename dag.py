from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator
from airflow.providers.google.cloud.hooks.datafusion import PipelineStates

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 12, 18),
    'depends_on_past': False,
    'email': ['thp.nite@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'employee_data',
    default_args=default_args,
    description='Runs an external Python script',
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_script_task = BashOperator(
        task_id='extract_data',
        bash_command='python /home/airflow/gcs/dags/scripts/extract.py',
    )

    start_pipeline = CloudDataFusionStartPipelineOperator(
        task_id='start_datafusion_pipeline',
        location="us-west1",
        pipeline_name="etl-pipeline",
        instance_name="datafusion-dev",
        pipeline_timeout=900,
        success_states=[PipelineStates.COMPLETED],
    )   

    # Orchestration
    run_script_task >> start_pipeline