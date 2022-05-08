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
son_timeline = UserTimelineCursor('@Sonny7')

i = 0
for each_tweet in son_timeline.items():
    print(f"{i}번째 트윗 : {each_tweet.full_text}")
    i += 1