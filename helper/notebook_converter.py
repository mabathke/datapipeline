import os
from nbconvert import PythonExporter
import nbformat

DAGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dags')

def convert_notebook_to_py(notebook_path, output_dir):
    
    py_file_name = os.path.basename(notebook_path).replace('.ipynb', '.py')
    py_file_path = os.path.join(output_dir, py_file_name)
    
    print(f"Found notebook: {notebook_path}")
    
    # Load the notebook
    try:
        with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
            notebook_content = nbformat.read(notebook_file, as_version=4)
        
        # Convert notebook to Python script
        exporter = PythonExporter()
        script, _ = exporter.from_notebook_node(notebook_content)
        
        # Write the Python script to the output directory
        with open(py_file_path, 'w', encoding='utf-8') as py_file:
            py_file.write(script)

        print(f"Converted notebook to: {py_file_path}")
    except Exception as e:
        print(f"Error converting notebook {notebook_path}: {e}")

def find_and_convert_notebooks():
    # Recursively search through the DAGS_DIR for any .ipynb files
    print(f"Searching for notebooks in {DAGS_DIR}...")
    
    for root, dirs, files in os.walk(DAGS_DIR):
        print(f"Checking directory: {root}")  
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                # Ensure the output path mirrors the subdirectory structure
                relative_path = os.path.relpath(root, DAGS_DIR)
                output_dir = os.path.join(DAGS_DIR, relative_path)
                os.makedirs(output_dir, exist_ok=True) 
                
                # Convert the notebook
                convert_notebook_to_py(notebook_path, output_dir)
    
    print("Notebook search and conversion complete.")

if __name__ == "__main__":
    find_and_convert_notebooks()
