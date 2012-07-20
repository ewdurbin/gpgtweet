
import tornado.web
import tornado.ioloop

from gpgtweet.server import utils
from gpgtweet.server import auth 
from gpgtweet.server import messages 

COOKIE_SECRET = 'supersecretkey'

settings = {
    'twitter_consumer_key': utils.CONSUMER_KEY,
    'twitter_consumer_secret': utils.CONSUMER_SECRET,
    'cookie_secret': COOKIE_SECRET,
    'login_url': '/signin',
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

if __name__ == "__main__":
    application.listen(8888, address="*")
    tornado.ioloop.IOLoop.instance().start()
