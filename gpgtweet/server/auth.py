
import tornado.auth
from twitter import TwitterError

from gpgtweet.server import core
from gpgtweet.server import utils

import json

class SignOutHandler(core.BaseHandler):
    def get(self):
        self.clear_cookie('access_token')
        self.redirect('/')

class SignInHandler(core.BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect(callback_uri=self.request.full_url())

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
        access_token = user['access_token']
        access_token['protected'] = user['protected']
        cookie_data = tornado.escape.json_encode(access_token)
        self.set_secure_cookie("access_token", cookie_data) 
        self.redirect('/')

class ReAuthHandler(core.BaseHandler):
    def post(self):
        secret = self.get_argument('oauth_secret')
        token = self.get_argument('oauth_token')
        if secret and token: 
            settings = self.settings
            api = utils.get_twitter_api(token, secret, settings)
            try:
                twitter_user = api.VerifyCredentials()
                access_token = {'key': token,
                                'secret': secret,
                                'screen_name': twitter_user.screen_name,
                                'protected': twitter_user.protected,
                                'user_id': twitter_user.id} 
                cookie_data = tornado.escape.json_encode(access_token)
                self.set_secure_cookie("access_token", cookie_data) 
                self.redirect('/')
            except TwitterError:
                self.send_error(status_code=401)

class OOBHandler(core.BaseHandler):
    def get(self):
        request_token = utils.get_request_token(self.settings)
        if request_token:
            request_token_data = tornado.escape.json_encode(request_token)
            self.set_secure_cookie("request_token", request_token_data)
            self.write("%s?oauth_token=%s" % (utils.AUTHORIZATION_URL,
                                              request_token['oauth_token']))
        else:
            self.send_error(status_code=500)

class OOBCatchHandler(core.BaseHandler):
    def post(self):
        request_token_data = self.get_secure_cookie("request_token")
        self.clear_cookie("request_token")
        request_token = tornado.escape.json_decode(request_token_data)
        pin = self.get_argument('pin')
        access_token = utils.convert_request_access(self.settings,
                                                    request_token, pin)
        if access_token:
            self.write(tornado.escape.json_encode(access_token))
        else:
            self.send_error(status_code=401)
