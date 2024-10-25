from airflow.hooks.postgres_hook import PostgresHook

def delete_table():
    TABLE_NAME = "chargingstations"
    delete_sql = f"DROP TABLE IF EXISTS {TABLE_NAME};"
    
    pg_hook = PostgresHook(postgres_conn_id="datapipeline_postgres")
    pg_hook.run(delete_sql)
