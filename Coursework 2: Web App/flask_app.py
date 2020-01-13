# DE4 SIoT 2020 - Neel Le Penru
# Charts vs. News Web App v2.0

from flask import Flask, render_template, request, redirect, url_for, session
from newsapi import NewsApiClient
import json
import startup
import spotipy
import spotipy.util as util
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import random
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from fycharts import SpotifyCharts
from Charts_News_Analysis import analyseCharts, analyseHeadlines
api = SpotifyCharts.SpotifyCharts()
newsapi = NewsApiClient(api_key='' #Key redacted)

global posThresh
global negThresh
global adjPos
global adjNeg
global token
# posThresh = 0.2
# negThresh = -0.2
chartsPos = 0.2
chartsNeg = -0.2
posThresh = 0
negThresh = 0
adjPos = 0
adjNeg = 0

app = Flask(__name__)
app.secret_key = b'' #Session key redacted


@app.route('/', methods=['GET','POST'])
def index():
    errors = []
    welcome = 'Hello, and welcome to Charts vs News!'
    return render_template('index.html',page=welcome, errors=errors,intro=True,firstheadlines = True)

@app.route('/headlines/', methods=['GET', 'POST'])
def show_headlines():
    dateTimeStr1 = datetime.strftime(datetime.now(), '%H:%M on %d.%m.%Y')
    header = 'It is ' + dateTimeStr1 + '. Here are the latest UK headlines:'
    headlines = newsapi.get_top_headlines(sources="google-news-uk", page_size=20)
    headlines = headlines['articles']
    numArticles = len(headlines)
    titles = {}
    for i in range(numArticles):
        titles[i] = headlines[i]['title']
    sentiment = analyseHeadlines(adjPos,adjNeg)
    if sentiment >= posThresh:
        sentimentDesc = 'The Sentiment Analysis score of the current headlines is ' + str(sentiment) + '. This suggests their sentiment is positive.'
        session['sDesc'] = sentimentDesc
    if sentiment < negThresh:
        sentimentDesc = 'The Sentiment Analysis score of the current headlines is ' + str(sentiment) + '. This suggests their sentiment is negative.'
        session['sDesc'] = sentimentDesc
    return render_template('index.html',page=header,news=True,titles=titles,info=titles[0],n=numArticles,sentimentDesc=sentimentDesc)

@app.route('/spotify/', methods=['POST'])
def spotify_login():
    response = startup.getUser()
    return redirect(response)

@app.route('/callback/')
def test():
    startup.getUserToken(request.args['code'])
    token = startup.getAccessToken()
    token = token[0]
    session['token'] = token
    success = None
    sentimentDesc = session['sDesc']
    return render_template('index.html',authgranted=True,titles=True,sentimentDesc=sentimentDesc)

@app.route('/oppose/', methods = ['GET','POST'])
def opposeHeadlines():
    token = session['token']
    if token:
        sp = spotipy.Spotify(auth=token)
        user_data = sp.current_user()
        dateTimeStr = datetime.strftime(datetime.now(), '%Y-%m-%d, %H:%M')
        sentiment = analyseHeadlines(adjPos,adjNeg)
        if sentiment >= posThresh:
            song_id = analyseCharts('negative',chartsPos,chartsNeg)
            playlist_name = 'Charts vs News Negative Playlist - Opposing Sentiment of Headlines on ' + dateTimeStr
            desc = "Playlist with songs from the UK Spotify Charts whose names are deemed as negative, to oppose the current sentiment of UK News Headlines. Playlist created with a Flask WebApp on PythonAnywhere using Spotipy, NLTK for language processing and Google News UK via Python News API."
            sentimentDesc = 'The Sentiment Analysis score of the current headlines is ' + str(sentiment) + '. This suggests their sentiment is positive.'
        if sentiment < negThresh:
            song_id = analyseCharts('positive',chartsPos,chartsNeg)
            playlist_name = 'Charts vs News Positive Playlist - Opposing Sentiment of Headlines on ' + dateTimeStr
            desc = "Playlist with songs from the UK Spotify Charts whose names are deemed as positive, to oppose the current sentiment of UK News Headlines. Playlist created with a Flask WebApp on PythonAnywhere using Spotipy, NLTK for language processing and Google News UK via Python News API."
            sentimentDesc = 'The Sentiment Analysis score of the current headlines is ' + str(sentiment) + '. This suggests their sentiment is negative.'
        playlist = sp.user_playlist_create(user_data['id'], playlist_name, public=True, description=desc)
        playlist_id = playlist['id']
        print('Made Playlist, ID:',playlist_id)
        p = sp.user_playlist_add_tracks(user_data['id'], playlist_id, song_id)
        print('Track Added')
        success = True
        return render_template('disp_playlist.html',success=success,id=user_data['id'],playlist_id=playlist_id,sentimentDesc=sentimentDesc)
    else:
        success = None
        return render_template('disp_playlist.html',success=success,sentimentDesc=sentimentDesc)


@app.route('/match/', methods = ['GET','POST'])
def matchHeadlines():
    token = session['token']
    if token:
        sp = spotipy.Spotify(auth=token)
        user_data = sp.current_user()
        dateTimeStr = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')
        sentiment = analyseHeadlines(adjPos,adjNeg)
        if sentiment >= posThresh:
            song_id = analyseCharts('positive',chartsPos,chartsNeg)
            playlist_name = 'Charts vs News Positive Playlist - Matching Sentiment of Headlines on ' + dateTimeStr
            desc = "Playlist with songs from the UK Spotify Charts whose names are deemed as positive, to match the current sentiment of UK News Headlines. Playlist created with a Flask WebApp on PythonAnywhere using Spotipy, NLTK for language processing and Google News UK via Python News API."
            sentimentDesc = 'The Sentiment Analysis score of the current headlines is ' + str(sentiment) + '. This suggests their sentiment is positive.'
        if sentiment < negThresh:
            song_id = analyseCharts('negative',chartsPos,chartsNeg)
            playlist_name = 'Charts vs News Negative Playlist - Matching Sentiment of Headlines on ' + dateTimeStr
            desc = "Playlist with songs from the UK Spotify Charts whose names are deemed as negative, to match the current sentiment of UK News Headlines. Playlist created with a Flask WebApp on PythonAnywhere using Spotipy, NLTK for language processing and Google News UK via Python News API."
            sentimentDesc = 'The Sentiment Analysis score of the current headlines is ' + str(sentiment) + '. This suggests their sentiment is negative.'
        playlist = sp.user_playlist_create(user_data['id'], playlist_name, public=True, description=desc)
        playlist_id = playlist['id']
        print('Made Playlist, ID:',playlist_id)
        p = sp.user_playlist_add_tracks(user_data['id'], playlist_id, song_id)
        print('Track Added')
        success = True
        return render_template('disp_playlist.html',success=success,id=user_data['id'],playlist_id=playlist_id,sentimentDesc=sentimentDesc)
    else:
        success = None
        return render_template('disp_playlist.html',success=success,sentimentDesc=sentimentDesc)
