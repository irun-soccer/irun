import tweepy
import twitter_secret as secret
import datetime, time

consumer_key = secret.twitter_consumer_key
consumer_secret = secret.twitter_consumer_secret
access_token = secret.twitter_access_token
access_secret = secret.twitter_access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)


def next_date(now_date):
    now_date = datetime.date.fromisoformat(now_date)
    next_date = now_date + datetime.timedelta(days=1)
    return next_date.isoformat()

def get_replies(player_name, match_date):
    result = list()
    api = tweepy.API(auth, timeout=600, wait_on_rate_limit=True)
    query = f'{player_name} filter:replies since:{match_date} until:{next_date(match_date)}'
    
    for status in tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended', count=180).items():
        result.append(status.full_text)

    return result

if __name__ == "__main__":
    print(get_replies('Aubameyang', '2022-05-23'))