import tweepy
import twitter_secret as secret

consumer_key = secret.twitter_consumer_key
consumer_secret = secret.twitter_consumer_secret
access_token = secret.twitter_access_token
access_secret = secret.twitter_access_secret

def connect_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    return api

def UserTimelineCursor(screen_name):
    tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended")
    return tweets

api = connect_api()
query = '@Sonny7 filter:replies since:2022-05-08 until:2022-05-09'

for status in tweepy.Cursor(api.search_tweets, q=query, lang='en').items():
    print(status.text)