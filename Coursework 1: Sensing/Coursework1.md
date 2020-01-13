The UK News headlines and UK Spotify Daily Top 200 data are provided in the CSV files above, alongside the Python files (and IPython Notebook*) used to gather them.

Due technical difficulties during the intial set-up, it was not possible get the data collection to autonomously run in a normal Python script on PythonAnywhere. Therefore, this workaround, of running the code within an IPython notebook (which can't be directly automated to run on PythonAnywhere), and creating a separate to Python script which could be automated by PythonAnywhere to run the notebook, was implemented.

Dependencies:
The code requires the following packages and APIs to run:
1. Python News API
2. FyCharts API
3. nbconvert library
