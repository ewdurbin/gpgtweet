
import os.path
import ConfigParser

class GPGTweetConfig:

    def _set_defaults(self):
        self.oauth_token = None
        self.oauth_token_secret = None
        self.gnupg_home = None 
        self.signing_keyid = None 
        self.api_provider = "https://gpgtweet.com"
        
    def _build_config(self):
        config = ConfigParser.RawConfigParser()
        config.add_section('TwitterApi')
        config.set('TwitterApi', 'oauth_token', None)
        config.set('TwitterApi', 'oauth_token_secret', None)
        config.add_section('GPGTweet')
        config.set('GPGTweet', 'api_provider', 'https://gpgtweet.com')
        config.add_section('gnupg')
        config.set('gnupg', 'signing_keyid', None)
        config.set('gnupg', 'gnupg_home', None)
        return config

    def _read_config(self, config_file):
        if os.path.isfile(config_file):
            self.config.read(config_file)
            self.oauth_token = self.config.get('TwitterApi', 'oauth_token')
            self.oauth_token_secret = self.config.get('TwitterApi', 'oauth_token_secret')
            self.gnupg_home = self.config.get('gnupg', 'gnupg_home') 
            self.signing_keyid = self.config.get('gnupg', 'signing_keyid')
            self.api_provider = self.config.get('GPGTweet', 'api_provider') 

    def __init__(self, config_file=os.path.expanduser('~/.gpgtweetrc')):
        self.config_file = config_file
        self._set_defaults()
        self.config = self._build_config()
        self._read_config(self.config_file)

    def set_oauth_token(self, oauth_token):
        self.oauth_token = oauth_token
        self.config.set('TwitterApi', 'oauth_token', oauth_token)

    def set_oauth_token_secret(self, oauth_token_secret):
        self.oauth_token_secret = oauth_token_secret
        self.config.set('TwitterApi', 'oauth_token_secret', oauth_token_secret)

    def set_gnupg_home(self, gnupg_home):
        self.gnupg_home = gnupg_home
        self.config.set('gnupg', 'gnupg_home', gnupg_home)

    def set_signing_keyid(self, signing_key):
        self.signing_keyid = signing_keyid 
        self.config.set('gnupg', 'signing_keyid', signing_keyid)

    def set_api_provider(self, api_provider):
        self.api_provider = api_provider
        self.config.set('GPGTweet', 'api_provider', api_provider)

    def write(self):
        with open(self.config_file, 'wb') as file:
            self.config.write(file)
