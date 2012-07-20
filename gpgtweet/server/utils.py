
import oauth2 as oauth
import twitter

CONSUMER_KEY = ''
CONSUMER_SECRET = ''

def get_twitter_api(token, secret):
    return twitter.Api(consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token_key=token,
                       access_token_secret=secret)

