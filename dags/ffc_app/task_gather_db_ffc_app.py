#!/usr/bin/env python
# coding: utf-8

# # Gather FFC data
# I host a website in my own networkk with a raspberry and expose it via DynDNS from my router. The app is used for tracking our catches from our fishing trips and ranks the catch based on length & rarity with its own rating system. I want to gather all the data by ssh-ing into the raspberry and downloading the data. The data is stored in a sqlite database. I will download the .db file.

# In[1]:


import paramiko
import os
import sqlite3
import pandas as pd
from io import BytesIO
import tempfile
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.providers.postgres.hooks.postgres import PostgresHook


# In[56]:


def get_dataframe_from_raspberry_local(table_name):
    """
    Connects to Raspberry Pi, downloads a SQLite file, queries a specific table, and returns the result as a DataFrame.
    
    Args:
    - table_name (str): The name of the table to query.
    
    Returns:
    - pd.DataFrame: A DataFrame containing the queried table's data.
    """
    # Raspberry Pi SSH details (replace with your credentials)
    RASPBERRY_PI_HOST = os.getenv("RASPBERRY_PI_HOST")  # Raspberry Pi IP
    RASPBERRY_PI_USER = os.getenv("RASPBERRY_PI_USER")  # Raspberry Pi Username
    RASPBERRY_PI_PASSWORD = os.getenv("RASPBERRY_PI_PASSWORD")  # Raspberry Pi Password

    
    # Remote path for the SQLite file on the Raspberry Pi
    REMOTE_SQLITE_FILE_PATH = '/home/mabathke/ffc-app/var/db/todos.db'  # Path to the SQLite DB on the Raspberry Pi

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to {RASPBERRY_PI_HOST}...")
        ssh.connect(RASPBERRY_PI_HOST, username=RASPBERRY_PI_USER, password=RASPBERRY_PI_PASSWORD)

        # Open an SFTP session
        sftp = ssh.open_sftp()

        # Download the SQLite file into an in-memory BytesIO object
        sqlite_file_obj = BytesIO()
        with sftp.open(REMOTE_SQLITE_FILE_PATH, 'rb') as sqlite_file:
            sqlite_file_obj.write(sqlite_file.read())

        print("SQLite file downloaded into memory.")

        # Close the SFTP connection
        sftp.close()

        # Write the in-memory SQLite file to a temporary file on disk
        sqlite_file_obj.seek(0)  # Reset the file pointer to the beginning
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(sqlite_file_obj.read())
            tmpfile_path = tmpfile.name

        print(f"SQLite file written to temporary file at {tmpfile_path}.")

        # Open the SQLite database from the temporary file
        conn = sqlite3.connect(tmpfile_path)

        # Query the table from the SQLite database
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)

        print(f"Queried table '{table_name}' from the SQLite database.")

        # Close the SQLite connection
        conn.close()

        # Clean up the temporary file
        os.remove(tmpfile_path)

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        ssh.close()


# In[ ]:


def get_and_insert_tables_from_raspberry(table_names):
    """
    Connects to Raspberry Pi via an Airflow SSH connection, downloads a SQLite file, 
    queries multiple tables, and inserts the data into PostgreSQL.

    Args:
    - table_names (list): A list of table names to query and insert.

    Returns:
    - None
    """
    # Use the SSH connection defined in Airflow
    ssh_hook = SSHHook(ssh_conn_id='raspberry')  # Use the connection ID from your Airflow setup
    
    # Remote path for the SQLite file on the Raspberry Pi
    REMOTE_SQLITE_FILE_PATH = '/home/mabathke/ffc-app/var/db/todos.db'  # Path to the SQLite DB on the Raspberry Pi

    # Use the PostgresHook to connect to PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='datapipeline_postgres')

    # Create an SSH client from the hook
    ssh_client = ssh_hook.get_conn()

    try:
        print("Connected to Raspberry Pi via Airflow SSHHook...")

        # Open an SFTP session
        sftp = ssh_client.open_sftp()

        # Download the SQLite file into an in-memory BytesIO object
        sqlite_file_obj = BytesIO()
        with sftp.open(REMOTE_SQLITE_FILE_PATH, 'rb') as sqlite_file:
            sqlite_file_obj.write(sqlite_file.read())

        print("SQLite file downloaded into memory.")

        # Close the SFTP connection
        sftp.close()

        # Write the in-memory SQLite file to a temporary file on disk
        sqlite_file_obj.seek(0)  # Reset the file pointer to the beginning
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(sqlite_file_obj.read())
            tmpfile_path = tmpfile.name

        print(f"SQLite file written to temporary file at {tmpfile_path}.")

        # Open the SQLite database from the temporary file
        conn = sqlite3.connect(tmpfile_path)

        # Loop through each table, query it, and insert data into PostgreSQL
        for table_name in table_names:
            print(f"Processing table: {table_name}")

            # Query the table from the SQLite database
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)

            print(f"Queried table '{table_name}' from the SQLite database.")
            
            # Insert DataFrame into PostgreSQL
            if not df.empty:
                df.to_sql(table_name, pg_hook.get_sqlalchemy_engine(), if_exists='replace', index=False)
                print(f"Inserted data from table '{table_name}' into PostgreSQL.")
            else:
                print(f"No data found in table '{table_name}'.")

        # Close the SQLite connection
        conn.close()

        # Clean up the temporary file
        os.remove(tmpfile_path)

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        ssh_client.close()


# In[57]:


# Example usage:
table_name = 'scoreboard'  # Replace with the actual table name you want to query
df = get_dataframe_from_raspberry_local(table_name)


# In[ ]:


df

