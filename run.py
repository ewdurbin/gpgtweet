
import sys
from optparse import OptionParser

import tornado.web
import tornado.ioloop

from gpgtweet.server import utils
from gpgtweet.server import auth 
from gpgtweet.server import messages 
from gpgtweet.server.config import GPGTweetConfig

def parse_options():
    parser = OptionParser()
    parser.add_option('-c', '--config-file',
                      help="Configuration File for GPGTweet Server",
                      default="gpgtweet.cfg", action="store", type="string",
                      dest="config_file")
    (options, args) = parser.parse_args()
    return (options, args)

if __name__ == "__main__":
    (options, args) = parse_options()

    config = GPGTweetConfig(options.config_file)

    settings = {
        'twitter_consumer_key': config.consumer_key,
        'twitter_consumer_secret': config.consumer_secret,
        'cookie_secret': config.cookie_secret,
        'login_url': '/signin',
        #Non Tornado Settings:
        'storage_dir': config.storage_dir,
    }
    
    application = tornado.web.Application([
        (r"/signin", auth.SignInHandler),
        (r"/reauth", auth.ReAuthHandler),
        (r"/message", messages.AcceptMessage),
        (r"/ret/.*", messages.RetrieveMessage),
        (r"/retpro/.*", messages.RetrieveProtectedMessage),
        (r"/signout", auth.SignOutHandler),
        ], **settings
    )

    application.listen(8888, address="*")
    tornado.ioloop.IOLoop.instance().start()
