from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from charging_stations.create_table_task import create_table
from charging_stations.insert_data_task import insert_data_to_postgres

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='insert_charging_stations',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    create_table_task = PythonOperator(
        task_id='create_table',
        python_callable=create_table
    )

    insert_data_task = PythonOperator(
        task_id='insert_data_to_postgres',
        python_callable=insert_data_to_postgres
    )

    # Set task dependencies
    create_table_task >> insert_data_task