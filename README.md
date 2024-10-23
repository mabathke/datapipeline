# Datapipeline

This is a simple datapipeline which has the purpose of gathering all the data I need for analyzing or doing some backups from my e.g. ffc-app. TODO: I want to add 
grafana as visualization tool. This will be done as soon as I hav everything setup and actual data to analyze

## Setup
- Follow the airflow guide to setup the airflow environment in docker. If you are one windows, you can use Docker Desktop. Alternatively, use WSL2 and install docker on the wsl distro
- For setting up the python environment:
  1. Install Anaconda
  2. use `conda env create -f conda-env.yaml` in the terminal of your choice
  3. After that you can use `conda activate datapipeline`

## Usage
The base concept is that you write your code in a Jupyter Notebook in the dags directory. IMHO it is better for local testing and debugging than writting a python file. Since a DAG needs to be (or rather should be) in a .py format, you can use the `notebook_converter.py` to convert the notebook to a python file. The `
`notebook_converter.py` will also add the necessary imports and the DAG definition.