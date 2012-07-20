
import oauth2 as oauth
import twitter

def get_twitter_api(token, secret, settings):
    consumer_key = settings['twitter_consumer_key']
    consumer_secret = settings['twitter_consumer_secret']
    return twitter.Api(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token_key=token,
                       access_token_secret=secret)

