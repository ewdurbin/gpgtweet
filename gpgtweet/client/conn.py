
import urllib
import urllib2
import cookielib

class HTTPConnector:

    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    def make_request(self, url, data=None):
        if data:
            encoded_data = urllib.urlencode(data)
            return self.opener.open(url, encoded_data)
        return self.opener.open(url)
