
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
        if self.config.gnupg_home:
            self.gpg = gnupg.GPG(gnupghome=self.config.gnupg_home)
        else:
            self.gpg = gnupg.GPG()

    def check_twitter_auth(self):
        if self.config.oauth_token and self.config.oauth_token_secret:
            data = {'oauth_token': self.config.oauth_token,
                    'oauth_secret': self.config.oauth_token_secret}
            try:
                resp = self.conn.make_request("%s/auth/reauth" % self.config.api_provider, data)
                return True
            except urllib2.URLError:
                return None
        else:
            return None

    def oob_auth(self):
        resp = self.conn.make_request("%s/auth/signin?oob=true" % self.config.api_provider)
        print("Open URL in browser of choice:\n\t%s" % resp.read())
        pin = raw_input("Pin: ")
        data = {'oauth_verifier': pin}
        resp = self.conn.make_request("%s/auth/signin?oob=true" % self.config.api_provider, data)
        access_token = json.loads(resp.read())
        self.config.set_oauth_token(access_token['oauth_token'])
        self.config.set_oauth_token_secret(access_token['oauth_token_secret'])

    def get_message(self):
        message = raw_input("Twitter Status: ")
        return message

    def sign_message(self, message):
        passphrase = getpass.getpass("GPG Passphrase: ")
        try:
            signed_message = self.gpg.sign(message,
                                           keyid=self.config.signing_keyid,
                                           passphrase=passphrase)
        except ValueError:
            return None
        return signed_message

    def set_message(self):
        message = self.get_message() 
        while not message:
            message = self.get_message()
        signed_message = self.sign_message(message)
        while not signed_message:
            print("Message failed to sign... passphrase correct?")
            signed_message = self.sign_message(message)
        return (message, signed_message)

    def set_status(self, message, signed_message):
        self.conn.make_request("%s/message/add" % self.config.api_provider,
                               {'message': message,
                                'smessage': signed_message,
                                'tweet': True})
