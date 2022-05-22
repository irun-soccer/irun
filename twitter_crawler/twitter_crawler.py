import tweepy
import twitter_secret as secret
import datetime, time

consumer_key = secret.twitter_consumer_key
consumer_secret = secret.twitter_consumer_secret
access_token = secret.twitter_access_token
access_secret = secret.twitter_access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

req_cnt = 0

def next_date(now_date):
    now_date = datetime.date.fromisoformat(now_date)
    next_date = now_date + datetime.timedelta(days=1)
    return next_date.isoformat()

def get_replies(player_name, match_date):
    global req_cnt
    result = list()
    api = tweepy.API(auth, timeout=600)
    query = f'{player_name} filter:replies since:{match_date} until:{next_date(match_date)}'
    
    if req_cnt >= 120:
        print("... almost limit: sleep 1000 sec...")
        time.sleep(1000)
        req_cnt = 0

    for status in tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended', count=180).items():
        result.append(status.full_text)
    req_cnt += 1

    return result