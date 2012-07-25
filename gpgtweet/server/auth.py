
import tornado.auth
from twitter import TwitterError

from gpgtweet.server import core
from gpgtweet.server import utils

import json

class SignOutHandler(core.BaseHandler):
    def get(self):
        self.clear_cookie('access_token')
        self.redirect('/')

def build_cookie(token, secret, settings):
    api = utils.get_twitter_api(token, secret, settings)
    try:
        twitter_user = api.VerifyCredentials()
        access_token = {'key': token,
                        'secret': secret,
                        'screen_name': twitter_user.screen_name,
                        'protected': twitter_user.protected,
                        'user_id': twitter_user.id} 
        return tornado.escape.json_encode(access_token)
    except TwitterError:
        return None

class SignInHandler(core.BaseHandler):

    def _redirect(self):
        callback_url = self.request.full_url()
        if self.get_argument("oob", None):
            callback_url = "oob"
        request_token = utils.get_request_token(self.settings,
                                                callback_uri=callback_url)
        if request_token:
            request_token_data = tornado.escape.json_encode(request_token)
            self.set_secure_cookie("request_token", request_token_data)
            twitter_url = "%s?oauth_token=%s&force_login=true" % (utils.SIGNIN_URL,
                                                                  request_token['oauth_token'])
            if callback_url == "oob":
                self.write(twitter_url)
            else:
                self.redirect(twitter_url)
        else:
            self.send_error(status_code=500)

    def _return(self):
        oauth_token = self.get_argument("oauth_token")
        oauth_verifier = self.get_argument("oauth_verifier")
        request_token_data = self.get_secure_cookie("request_token")
        self.clear_cookie("request_token")
        request_token = tornado.escape.json_decode(request_token_data)
        access_token = utils.convert_request_access(self.settings,
                                                    request_token,
                                                    oauth_verifier)
        cookie_data = build_cookie(access_token["oauth_token"],
                                   access_token["oauth_token_secret"],
                                   self.settings)
        self.set_secure_cookie("access_token", cookie_data) 
        self.redirect("/")

    def get(self):
        if self.get_argument("oauth_token", None):
            self._return()
        else:
            self._redirect()

    def post(self):
        request_token_data = self.get_secure_cookie("request_token")
        self.clear_cookie("request_token")
        request_token = tornado.escape.json_decode(request_token_data)
        verifier = self.get_argument('oauth_verifier')
        access_token = utils.convert_request_access(self.settings,
                                                    request_token, verifier)
        if access_token and self.get_argument("oob", None):
            self.write(tornado.escape.json_encode(access_token))
        elif access_token:
            cookie_data = build_cookie(access_token["oauth_token"],
                                       access_token["oauth_token_secret"],
                                       self.settings)
            self.set_secure_cookie("access_token", cookie_data)
            self.redirect("/")
        else:
            self.send_error(status_code=401)

class ReAuthHandler(core.BaseHandler):
    def post(self):
        secret = self.get_argument('oauth_secret')
        token = self.get_argument('oauth_token')
        if secret and token: 
            settings = self.settings
            cookie_data = build_cookie(token, secret, settings)
            if cookie_data:
                self.set_secure_cookie("access_token", cookie_data) 
                self.redirect('/')
            else:
                self.send_error(status_code=401)
