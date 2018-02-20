import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

notebook_filename = "../Demos/1 - Pythagorean Expectation/Lab - Pythagorean Expectation - The Relationship between Runs and Wins (DS).ipynb"
notebook_filename_out = "executed_notebook.ipynb"

with open(notebook_filename) as f:
	nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

try:
    out = ep.preprocess(nb, {'metadata': {'path': run_path}})
except CellExecutionError:
    out = None
    msg = 'Error executing the notebook "%s".\n\n' % notebook_filename
    msg += 'See notebook "%s" for the traceback.' % notebook_filename_out
    print(msg)
    raise
finally:
    with open(notebook_filename_out, mode='wt') as f:
        nbformat.write(nb, f)