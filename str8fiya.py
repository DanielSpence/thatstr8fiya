#!/usr/bin/env python
import urllib.request
import re
import random
import json
import os.path
import tweepy
from keys import keys
from soundCloud import songList
 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Adds songs that are new to the top 50 chart into the dictionary
def updateDictionary(songList, dict):
    for song in songList:
        if (not(song in dict)):
            dict[song] = -1
    return dict

#checks whether or not we have already replied to a song, returns true if we have not
def replyToTweet(dict, song, currentTweetID):
    if(dict.get(song)== -1):
        return True
    if(dict.get(song)>currentTweetID):
        return False
    return True             

#checks what songs we have replied to if any, loads the dictionary in if it exists
if (not(os.path.isfile('dictionary.json'))):
    urlDict = {}
    urlDict = updateDictionary(songList, urlDict)
else:
    # load from file:
    with open('dictionary.json', 'r') as f:
        try:
            urlDict = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            urlDict = {}
            urlDict = updateDictionary(songList, urlDict)       

#goes through each song from the top 50 and replies to the most recent 50 tweets featuring them that we have no already replied to
for song in songList:
    search_results = api.search(q=song + ' + -rt',count=50)
    for tweets in search_results:    
        if(not(replyToTweet(urlDict, song, tweets.id))):
            break
        #creates message string    
        screenName = tweets.user.screen_name
        message = '@%s \U0001F44D \U0001F44D \U0001F44D' % (screenName)
        tweets = api.update_status(message, tweets.id)
    if(len(search_results)>0):        
        urlDict[song] = search_results[0].id
    
# save to file:
with open('dictionary.json', 'w') as f:
    json.dump(urlDict, f)

