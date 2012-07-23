
import os.path
import ConfigParser

class GPGTweetConfig:

    def __init__(self, config_file=os.path.expanduser('~/.gpgtweetrc')):
        self.config_file = config_file
        self.oauth_token = None
        self.oauth_token_secret = None
        self.api_provider = "https://gpgtweet.com"
        self.gnupg_home = os.path.expanduser("~/.gnupg")
        self.config = ConfigParser.RawConfigParser()
        self.config.add_section('TwitterApi')
        self.config.add_section('GPGTweet')
        self.config.add_section('gnupg')
        if os.path.isfile(config_file):
            self.config.read(self.config_file)
            self.oauth_token = self.config.get('TwitterApi', 'oauth_token')
            self.oauth_token_secret = self.config.get('TwitterApi',
                                                      'oauth_token_secret')
            self.api_provider = "https://gpgtweet.com"
            self.gnupg_home = os.path.expanduser("~/.gnupg")

    def set_oauth_token(self, oauth_token):
        self.oauth_token = oauth_token
        self.config.set('TwitterApi', 'oauth_token', oauth_token)

    def set_oauth_token_secret(self, oauth_token_secret):
        self.oauth_token_secret = oauth_token_secret
        self.config.set('TwitterApi', 'oauth_token_secret', oauth_token_secret)

    def set_api_provider(self, api_provider):
        self.api_provider = api_provider
        self.config.set('GPGTweet', 'api_provider', api_provider)

    def set_gnupg_home(self, gnupg_home):
        self.gnupg_home = gnupg_home
        self.config.set('GPGTweet', 'gnupg_home', gnupg_home)

    def write(self):
        with open(self.config_file, 'wb') as file:
            self.config.write(file)
