import twitter
import twitter_secret as secret

consumer_key = secret.twitter_consumer_key
consumer_secret = secret.twitter_consumer_secret
access_token = secret.twitter_access_token
access_secret = secret.twitter_access_secret

twitter_api = twitter.Api(consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token,
            access_token_secret=access_secret)

account = "@Sonny7"
status = twitter_api.GetUserTimeline(screen_name=account, count=500, include_rts=True, exclude_replies=False)
print(status)