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

config = GPGTweetConfig(os.path.expanduser('~/.gpgtweet-server.cfg'))

settings = {
    'twitter_consumer_key': config.consumer_key,
    'twitter_consumer_secret': config.consumer_secret,
    'cookie_secret': config.cookie_secret,
    'login_url': '/auth/signin',
    #Non Tornado Settings:
    'storage_dir': config.storage_dir,
}

application = tornado.web.Application([
    (r"/auth/signin", auth.SignInHandler),
    (r"/auth/reauth", auth.ReAuthHandler),
    (r"/auth/signout", auth.SignOutHandler),
    (r"/message/add", messages.AcceptMessage),
    (r"/message/retrieve/.*", messages.RetrieveMessage),
    (r"/message/retrievep/.*", messages.RetrieveProtectedMessage),
    (r"/ret/.*" , messages.RetrieveMessage),
    (r"/retpro/.*" , messages.RetrieveProtectedMessage),
    (r"/", RootHandler),
    ], **settings
)
