import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

with open('GetCharts.ipynb') as f:
    nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '/home/npl16/'}})

with open('executed_notebook.ipynb', 'wt') as f:
    nbformat.write(nb, f)

print('Successfully Run Notebook')
