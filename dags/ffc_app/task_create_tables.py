from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# SQL statements for creating the tables
CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS types_of_fish (
        id SERIAL PRIMARY KEY,
        type TEXT UNIQUE,
        avg_length INTEGER NOT NULL,
        upper_bound INTEGER NOT NULL,
        lower_bound INTEGER NOT NULL,
        is_rare BOOLEAN NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS scoreboard (
        id SERIAL PRIMARY KEY,
        owner_id INTEGER NOT NULL,
        fish_type_id INTEGER NOT NULL,
        length INTEGER NOT NULL,
        points INTEGER NOT NULL,
        date TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS email_verified (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE,
        register_key INTEGER UNIQUE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        hashed_password BYTEA,
        salt BYTEA,
        name TEXT,
        email TEXT UNIQUE
    );
    """
]

def create_tables():
    # Use PostgresHook to connect to the PostgreSQL database
    pg_hook = PostgresHook(postgres_conn_id='datapipeline_postgres')
    
    # Execute each SQL statement
    for sql in CREATE_TABLES_SQL:
        pg_hook.run(sql)
        print(f"Executed SQL: {sql}")