from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from ffc_app.task_gather_db_ffc_app import get_and_insert_tables_from_raspberry
from ffc_app.task_create_tables import create_tables
'''
The DAG gets only ran locally since I do not want to expose my Raspberry Pi to the internet.
If I find a solution to let airflow access my raspberry I will let the DAG run. The DA
'''
# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='insert_fc_app_data',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    get_and_insert_tables_from_raspberry_task = PythonOperator(
        task_id='get_and_insert_tables_from_raspberry',
        python_callable=get_and_insert_tables_from_raspberry,  
        op_args=[['types_of_fish', 'scoreboard', 'users']],  # Tables to be processed
    )
    
    create_tables_task = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables
    )

    create_tables_task >> get_and_insert_tables_from_raspberry_task
