from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from ffc_app.gather_db_ffc_app import get_dataframe_from_raspberry
from ffc_app.create_tables import create_tables
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

    gather_db_ffc_app_task = PythonOperator(
        task_id='gather_db_ffc_app',
        python_callable=get_dataframe_from_raspberry,  
        op_args=['scoreboard'],  
    )

    gather_db_ffc_app_task
