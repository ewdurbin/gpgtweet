
import twitter

import oauth2 as oauth
try:
  from urlparse import parse_qsl
except:
  from cgi import parse_qsl

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

def get_twitter_api(token, secret, settings):
    consumer_key = settings['twitter_consumer_key']
    consumer_secret = settings['twitter_consumer_secret']
    return twitter.Api(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token_key=token,
                       access_token_secret=secret)

def get_request_token(settings, callback_uri="oob"):
    consumer_key = settings['twitter_consumer_key']
    consumer_secret = settings['twitter_consumer_secret']
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request(REQUEST_TOKEN_URL, method='POST',
                                   body="oauth_callback=%s" % callback_uri)
    if resp['status'] != '200':
        return None
    return dict(parse_qsl(content))

def convert_request_access(settings, request_token, verifier):
    consumer_key = settings['twitter_consumer_key']
    consumer_secret = settings['twitter_consumer_secret']
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    token = oauth.Token(request_token['oauth_token'],
                        request_token['oauth_token_secret'])
    token.set_verifier(verifier)
    client  = oauth.Client(consumer, token)
    resp, content = client.request(ACCESS_TOKEN_URL, method='POST',
                                   body='oauth_verifier=%s' % verifier)
    if resp['status'] != '200':
        return None
    return dict(parse_qsl(content))
