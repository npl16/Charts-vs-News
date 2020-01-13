import pandas as pd
import numpy as np
import nltk
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from newsapi import NewsApiClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from fycharts import SpotifyCharts
import random

api = SpotifyCharts.SpotifyCharts()

def removeDuplicates(names):
    namesList = []
    for line in names:
        if line not in namesList:
            namesList.append(line)
    return namesList

def sentimentAnalysis(namesList):
    sia = SIA()
    Results = []

    for line in namesList:
        pol_score = sia.polarity_scores(line)
        pol_score['headline/name'] = line
        Results.append(pol_score)
    return Results

def assessPositivity(Results,posThresh,negThresh):
    df = pd.DataFrame.from_records(Results)
    df['positivity'] = 0
    pos_val = posThresh
    neg_val = negThresh
    df.loc[df['compound'] >= pos_val, 'positivity'] = 1
    df.loc[df['compound'] < neg_val, 'positivity'] = -1
    return df

def process_text(headlines):
    tokens = []
    for line in headlines:
        toks = tokenizer.tokenize(line)
        toks = [t.lower() for t in toks if t.lower() not in stopWords and len(t)>2]
        tokens.extend(toks)

    return tokens

def analyseHeadlines(posThresh,negThresh):
    newsapi = NewsApiClient(api_key='') #Key redacted
    posThresh = posThresh
    negThresh = negThresh

    headlines = newsapi.get_top_headlines(sources="google-news-uk", page_size=20)
    headlines = headlines['articles']
    numArticles = len(headlines)
    namesList = []
    for i in range(numArticles):
        namesList.append(headlines[i]['title'])
    sentimentScores = sentimentAnalysis(namesList)
    df = assessPositivity(sentimentScores,posThresh,negThresh)
    sentiment = df['compound'].mean()
    return sentiment

def analyseCharts(state,posThresh,negThresh):
    timelag = 1
    currentHour = int(datetime.strftime(datetime.now(), '%H'))
    if currentHour < 20:
        dateStr = datetime.strftime(datetime.now() - timedelta(timelag+1), '%Y-%m-%d')
    else:
        dateStr = datetime.strftime(datetime.now() - timedelta(timelag), '%Y-%m-%d')
    fileName = 'top200_' + dateStr + '.csv'
    api.top200Daily(output_file = fileName, start = dateStr, end = dateStr, region = 'gb')
    charts = pd.read_csv(fileName)
    headList = removeDuplicates(charts['Track Name'])
    sentimentScores = sentimentAnalysis(headList)
    df = assessPositivity(sentimentScores,posThresh,negThresh)
    df['position'] = range(0, len(df))

    posSongs = []
    posSongIDs = []
    negSongs = []
    negSongIDs = []
    resultIDs = []

    for k in df[df['positivity']==1]['position']:
        posSongs.append([k,df['headline/name'][k]])
        posSongIDs.append(charts['id'][k])

    for k in df[df['positivity']==-1]['position']:
        negSongs.append([k,df['headline/name'][k]])
        negSongIDs.append(charts['id'][k])

    if state == 'negative':
        indices = random.sample(range(len(negSongs)-1),(len(negSongs)//2))
        for i in indices:
            resultIDs.append(negSongIDs[i])
        return resultIDs

    elif state == 'positive':
        indices = random.sample(range(len(posSongs)-1),(len(posSongs)//2))
        for i in indices:
            resultIDs.append(posSongIDs[i])
        return resultIDs
