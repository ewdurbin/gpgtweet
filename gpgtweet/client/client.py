
from gpgtweet.client.config import GPGTweetConfig
from gpgtweet.client.conn import HTTPConnector 

import urllib2
import gnupg
import getpass

import json

class GPGTweetClient:

    def __init__(self):
        self.config = GPGTweetConfig()
        self.conn = HTTPConnector()
        self.gpg = gnupg.GPG()

    def check_twitter_auth(self):
        if self.config.oauth_token and self.config.oauth_token_secret:
            data = {'oauth_token': self.config.oauth_token,
                    'oauth_secret': self.config.oauth_token_secret}
            try:
                resp = self.conn.make_request("%s/reauth" % self.config.api_provider,
                                              data)
                return True
            except urllib2.URLError:
                return None
        else:
            return None

    def oob_auth(self):
        resp = self.conn.make_request("%s/signin/oob" % self.config.api_provider)
        print "Open URL in browser of choice:\n\t%s" % resp.read()
        pin = raw_input("Pin: ")
        data = {'pin': pin}
        resp = self.conn.make_request("%s/signin/oob/catch" % self.config.api_provider,
                                      data)
        access_token = json.loads(resp.read())
        self.config.set_oauth_token(access_token['oauth_token'])
        self.config.set_oauth_token_secret(access_token['oauth_token_secret'])

    def get_message(self):
        message = raw_input("Twitter Status: ")
        confirmed = False
        print "Confirm Message?"
        print message
        if raw_input("y/n") == 'y':
            return message
        return None

    def sign_message(self, message):
        passphrase = getpass.getpass("GPG Passphrase: ")
        try:
            signed_message = self.gpg.sign(message, passphrase=passphrase)
        except ValueError:
            return None
        return signed_message

    def set_message(self):
        message = self.get_message() 
        while not message:
            message = self.get_message()
        signed_message = self.sign_message(message)
        while not signed_message:
            print "Message failed to sign, see stack trace... passphrase correct?"
            signed_message = self.sign_message(message)
        return (message, signed_message)

    def set_status(self, message, signed_message):
        self.conn.make_request("%s/message" % self.config.api_provider,
                               {'message': message,
                                'smessage': signed_message,
                                'tweet': True})
