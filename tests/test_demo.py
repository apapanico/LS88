
# from pathlib import Path

# import nbformat
# from nbconvert.preprocessors import ExecutePreprocessor
# from nbconvert.preprocessors import CellExecutionError

# ROOT = Path('..').resolve()
# SKIP = [ROOT / 'tests', ROOT / 'data']

# notebooks_to_test = ROOT.glob('**/*.ipynb')
# for nb_f in notebooks_to_test:
#     if any(skip in nb_f.parents for skip in SKIP):
#         continue

#     with open(nb_f) as f:
#         nb = nbformat.read(f, as_version=4)

#     ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

#     run_path = str(nb_f.parent)

#     try:
#         out = ep.preprocess(nb, {'metadata': {'path': run_path}})
#     except CellExecutionError as e:
#         out = None
#         msg = 'Error executing the notebook "%s".\n\n' % nb_f
#         print(msg)
#         raise e
