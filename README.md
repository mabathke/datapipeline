# Datapipeline

This project implements a simple data pipeline for gathering, backing up, and analyzing data, such as from my ffc-app. For visualization I integrated Grafana and the postgres database. The pipeline is implemented using Apache Airflow, a popular open-source tool for orchestrating complex workflows and data processing pipelines.

## Setup

### Airflow Environment Setup
- Follow the [Airflow guide](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) to set up the Airflow environment using Docker.
  - If you're on **Windows**, you can use Docker Desktop.
  - Alternatively, you can install Docker on **WSL2** and set up Airflow within the WSL2 distribution.

### Python Environment Setup
1. **Install Anaconda**: You can download and install it from [here](https://www.anaconda.com/products/individual).
2. Create the environment by running the following command in your terminal:
    ```bash
    conda env create -f conda-env.yaml
    conda activate datapipeline
    ```
3. Update the conda environment with the following command:
    ```bash
    conda env update -f conda-env.yaml
    ```

### Setup database user for grafana

This guide explains how to create a custom read-only user in PostgreSQL and grant access to both existing and future tables in the `public` schema.

### Steps

#### 1. Create a Role for Read-Only Access

First, create a role (`readaccess`) that will have read-only access to the schema and tables:

```sql
CREATE ROLE readaccess; 
```
#### 2\. Grant Access to Existing Tables

To give the `readaccess` role the ability to read from all existing tables in the `public` schema, run the following commands:

```sql

GRANT USAGE ON SCHEMA public TO readaccess;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readaccess;
```
-   **USAGE**: Allows the role to access the schema.
-   **SELECT**: Grants read-only access to all existing tables in the `public` schema.

#### 3\. Grant Access to Future Tables

To ensure that the `readaccess` role has access to any tables created in the future in the `public` schema, alter the default privileges:

```sql

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readaccess;
```
This command ensures that the role will automatically receive `SELECT` privileges for any new tables created in the `public` schema.

#### 4\. Create a User with a Password

Next, create the `grafana` user with a password. This user will inherit the `readaccess` role:

```sql
CREATE USER grafana WITH PASSWORD 'secretpass@dev';
```
Replace `'secretpass@dev'` with a strong password for the user.

#### 5\. Grant the `readaccess` Role to the User

Finally, grant the `readaccess` role to the `grafana` user, which will give the user the read-only permissions:

```sql
GRANT readaccess TO grafana;
```
The `grafana` user now has read-only access to all existing and future tables in the `public` schema.
## Usage
The base workflow is to write code in a **Jupyter Notebook** within the `dags` directory. This approach allows for easier local testing and debugging compared to writing directly in a Python file.

Since Airflow DAGs need to be in `.py` format for execution, you can use the `notebook_converter.py` script to automatically convert your Jupyter notebooks to Python files. This script will also add the necessary imports and the DAG definition required by Airflow.

### Steps:

1.  Write your DAG logic in a Jupyter notebook inside the `dags` directory.
2.  Run `python notebook_converter.py` script in your terminal to convert the notebook into a `.py` file.
3.  The converted file will include all required DAG definitions and imports, making it ready for use within Airflow.