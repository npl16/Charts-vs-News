from datetime import datetime, timedelta
from newsapi import NewsApiClient #importing News Api
import csv # For reading from and writing to csv files
from time import sleep

refresh_time = 5 #how long to wait before checking the headlines again, in minutes
sleep_rate = 5*60 #convert to seconds

newsapi = NewsApiClient(api_key='6df6b43338a7489ab0d9000c617d4320') #Unique News API key

while True:

    headlines = newsapi.get_top_headlines(sources="google-news-uk", page_size=20) #get up to top 20 headlines from Google News UK
    headlines = headlines['articles'] #Obtaining relevant information to get headlines from returned JSON object
    numArticles = len(headlines)
    titles = [None for i in range(numArticles)]
    for i in range(numArticles):
         titles[i] = [headlines[i]['title']] #Put headlines from News API JSON object into list of headline strings


    newsTimeStr = datetime.strftime(datetime.now(), '%Y-%m-%d-%H%M') #Current Date and Time
    todayStr = datetime.strftime(datetime.now(), '%Y-%m-%d') #Current Date Only

    newsStr = todayStr + '_Headlines.csv' #Filename for Today's News

    previousHeadlines = [] #To store headlines obtained last time code was run (ie. 5 min ago)
    oldNews = 'previousHeadlines.csv'
    with open(oldNews, newline='') as f: #Read from previousHeadlines.csv, which was created as an empty csv before code was first run
        reader = csv.reader(f)
        for row in reader:
            previousHeadlines.append(row) #Take headlines from previous batch and append into list

    count = 0 #Created to tally up number of new headlines
    for headline in titles: #from newly obtained headlines, leave out any if they were in the previous lot
        if headline in previousHeadlines:
            pass
        else:
            count += 1
            with open(newsStr,'a') as fd: #append new headlines to log for the day - this will create a new file when the date changes (as the filename will change)
                wr = csv.writer(fd, dialect='excel')
                wr.writerow(headline)


    with open(oldNews,'w',newline='') as result_file: #overwrite previousHeadlines.csv with all headlines found this time around
        wr = csv.writer(result_file, dialect='excel')
        wr.writerows(titles)

    log_info = 'Obtained ' + str(count) + ' New Headlines at ' + newsTimeStr #get log info on when and how many new articles are found
    with open('NewsLog1.csv','a') as log:
        wr = csv.writer(log,dialect='excel')
        wr.writerow([log_info])

    print(log_info) #confirmation that task was successfully completed at a certain time
    sleep(sleep_rate)