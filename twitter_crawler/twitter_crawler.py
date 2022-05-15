import tweepy
import twitter_secret as secret
import datetime

consumer_key = secret.twitter_consumer_key
consumer_secret = secret.twitter_consumer_secret
access_token = secret.twitter_access_token
access_secret = secret.twitter_access_secret

def connect_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api

def next_date(now_date):
    now_date = datetime.date.fromisoformat(now_date)
    next_date = now_date + datetime.timedelta(days=1)
    return next_date.isoformat()

def GetReplies(player_name, match_date):
    api = connect_api()
    query = f'{player_name} filter:replies since:{match_date} until:{next_date(match_date)}'
    for status in tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items():
        print(status.full_text)

GetReplies('Harry Kane', '2022-05-13')