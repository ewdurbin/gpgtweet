
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
    parser.add_option('-a', '--listen-address',
                      help="Listen Address for Tornado Server",
                      default="127.0.0.1", action="store", type="string",
                      dest="listen_address")
    parser.add_option('-p', '--port',
                      help="Port for Tornado Server",
                      default="8888", action="store", type="int",
                      dest="listen_port")
    (options, args) = parser.parse_args()
    return (options, args)

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('gpgtweet.com')

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
        (r"/", RootHandler),
        ], **settings
    )

    application.listen(options.listen_port, address=options.listen_address)
    tornado.ioloop.IOLoop.instance().start()
