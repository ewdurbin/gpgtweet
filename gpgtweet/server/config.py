
import os.path
import ConfigParser

class GPGTweetConfig:

    def __init__(self, config_file):
        self.storage_dir = None
        self.cookie_secret = None
        self.consumer_key = None
        self.consumer_secret = None
        if os.path.isfile(config_file):
            config = ConfigParser.RawConfigParser()
            config.read(config_file)
            storage_dir = config.get('GPGTweet', 'storage_dir') 
            storage_dir = os.path.expanduser(storage_dir)
            self.storage_dir = os.path.abspath(storage_dir)
            self.cookie_secret = config.get('Tornado', 'cookie_secret') 
            self.consumer_key = config.get('TwitterApi', 'consumer_key')
            self.consumer_secret = config.get('TwitterApi', 'consumer_secret')
