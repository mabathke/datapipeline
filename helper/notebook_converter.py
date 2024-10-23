import os
from nbconvert import PythonExporter
import nbformat

# Set the directories
NOTEBOOK_DIR = './'  # Replace with the path where your notebooks are stored
HELPER_DIR = './helper'

# Ensure the helper directory exists
os.makedirs(HELPER_DIR, exist_ok=True)

def convert_notebook_to_py(notebook_name):
    notebook_path = os.path.join(NOTEBOOK_DIR, notebook_name)
    py_file_name = notebook_name.replace('.ipynb', '.py')
    py_file_path = os.path.join(HELPER_DIR, py_file_name)
    
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)
    
    # Convert notebook to Python script
    exporter = PythonExporter()
    script, _ = exporter.from_notebook_node(notebook_content)
    
    # Write the Python script to the /helper directory
    with open(py_file_path, 'w', encoding='utf-8') as py_file:
        py_file.write(script)

    print(f"Converted {notebook_name} to {py_file_path}")

def convert_all_notebooks():
    # Iterate over all notebooks in the directory
    for file_name in os.listdir(NOTEBOOK_DIR):
        if file_name.endswith('.ipynb'):
            convert_notebook_to_py(file_name)

if __name__ == "__main__":
    convert_all_notebooks()
