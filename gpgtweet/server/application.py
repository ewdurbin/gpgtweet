#!/usr/bin/env python

import os.path

import tornado.web
import tornado.ioloop

from gpgtweet.server import utils
from gpgtweet.server import auth 
from gpgtweet.server import messages 
from gpgtweet.server.config import GPGTweetConfig

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        content = """<pre>
welcome to gpgtweet.com

github:
 https://github.com/ewdurbin/gpgtweet

Contact:
 Ernest W. Durbin III
 ernest@gpgtweet.com
 @EWDurbin
</pre>"""
        self.write(content)

class GPGTweetServer:

    def __init__(self, config_file):
        if os.path.exists(config_file):
            self.config = GPGTweetConfig(config_file)
            self.settings = {'twitter_consumer_key': self.config.consumer_key,
                             'twitter_consumer_secret': self.config.consumer_secret,
                             'cookie_secret': self.config.cookie_secret,
                             'login_url': '/auth/signin',
                             #Non Tornado Settings:
                             'storage_dir': self.config.storage_dir}
            self.auth_app = tornado.web.Application([
                (r"/auth/signin", auth.SignInHandler),
                (r"/auth/reauth", auth.ReAuthHandler),
                (r"/auth/signout", auth.SignOutHandler),
                ], **self.settings)
            self.message_app = tornado.web.Application([
                (r"/message/add", messages.AcceptMessage),
                (r"/message/retrieve/.*", messages.RetrieveMessage),
                (r"/message/retrievep/.*", messages.RetrieveProtectedMessage),
                (r"/ret/.*" , messages.RetrieveMessage),
                (r"/retpro/.*" , messages.RetrieveProtectedMessage),
                (r"/", RootHandler),
                ], **self.settings)
            self.application = tornado.web.Application([
                (r"/auth/signin", auth.SignInHandler),
                (r"/auth/reauth", auth.ReAuthHandler),
                (r"/auth/signout", auth.SignOutHandler),
                (r"/message/add", messages.AcceptMessage),
                (r"/message/retrieve/.*", messages.RetrieveMessage),
                (r"/message/retrievep/.*", messages.RetrieveProtectedMessage),
                (r"/ret/.*" , messages.RetrieveMessage),
                (r"/retpro/.*" , messages.RetrieveProtectedMessage),
                (r"/", RootHandler),
                ], **self.settings)
        else:
            self.config = None
            self.settings = None
            self.auth_app = None
            self.message_app = None
            self.application = None
