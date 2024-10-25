from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from dags.charging_stations.task_create_table import create_table
from dags.charging_stations.task_insert_data import insert_data_to_postgres
from charging_stations.task_delete_table import delete_table

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
    '''
    if you need to reset the table because of schema changes/updates use the delete_table_task
    
    delete_table_task = PythonOperator(
        task_id='delete_table',
        python_callable=delete_table
    )

    #delete_table_task >> create_table_task >> insert_data_task
    '''
    create_table_task >> insert_data_task
