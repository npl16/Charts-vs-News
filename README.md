# Charts-vs-News
DE4 2020 Sensing and IoT project that analyses the sentiment of UK News Headlines and names of songs in the Spotify UK Top 200 Charts (spotifycharts.com) on a daily basis, and features a web app (hosted at npl16.pythonanywhere.com) that generates a Spotify playlist with songs from the latest Spotify UK Top 200 chart whose names either oppose or match the current sentiment of UK News Headlines.

## Coursework 1: Sensing
This directory contains all data gathered over the 12-day period measured in the form of dated CSV files, and the various Python (and Python Notebook) files used to gather this data. The 'NewsLog' and 'PreviousHeadlines' CSV files were used to keep track of number of headlines obtained at each query, and the latest headlines obtained, respectively.

Spotify Charts data was gathered using FyCharts:https://pypi.org/project/fycharts/

Headlines from Google News UK were obtained with the News API:https://newsapi.org/docs/client-libraries/python

All data analysis, for both parts of the coursework (excluding the web app), is contained within the 'DataAnalysis.ipynb' notebook.

Sentiment analysis is performed using NLTK (nltk.org).

NLTK, FyCharts and the Python News API must all be installed to run the code.

## Coursework 2: Web App
This directory contains all files used to create and host the 'Charts vs News' web app on PythonAnywhere.

The web app was made using Flask, with two custom HTML templates in the '/templates' directory.

Flask-Spotify-Auth (https://github.com/vanortg/Flask-Spotify-Auth) by Greg Van Ort was used to handle Spotify authentication. Its code ('flask_spotify_auth.py', 'setup.py' and 'startup.py') is uploaded with minor modifications in the main directory with the other website code files, which include various functions for performing sentiment analysis of headlines and charts' song names, and creating a playlist that matches or opposes the news. The latter is achieved with SpotiPy (https://spotipy.readthedocs.io/en/latest/).
