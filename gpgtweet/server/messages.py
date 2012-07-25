
import tornado.web
import tornado.escape
import tornado.auth

from gpgtweet.server import core
from gpgtweet.server import utils 

import string
import random
import os.path

def generate_id(size=6, chars=string.ascii_letters + string.digits):
    id = ''.join(random.choice(chars) for x in range(size))
    id_p = "%s.p" % id
    return (id, id_p)

def message_store(user, message, storage_dir, protected=False):
    dir_path = os.path.join(storage_dir, user)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    (id, id_p) = generate_id()
    file_path = os.path.join(dir_path, id)
    file_path_protected = os.path.join(dir_path, id_p)
    while os.path.exists(file_path) or os.path.exists(file_path_protected):
        (id, id_p) = generate_id()
        file_path = os.path.join(dir_path, id)
        file_path_protected = os.path.join(dir_path, id_p)
    if protected:
        file_path = file_path_protected
    with open(file_path, 'w') as file:
        file.write(message)
    return id

class AcceptMessage(core.BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        user = self.get_current_user() 
        access_token = self.get_access_token()
        message = self.decode_argument(self.get_argument('message'))
        signed_message = self.decode_argument(self.get_argument('smessage'))
        tweet = self.decode_argument(self.get_argument('tweet', None))
        protected = access_token['protected']
        storage_dir = self.settings['storage_dir']
        id = message_store(user, signed_message, storage_dir, protected)
        strings = (self.get_current_root(), user, id)
        self.ret_url = "%s/ret/%s/%s" % strings
        if tweet:
            self.twitter_request(
                "/statuses/update",
                post_args={"status": "%s %s" % (message, self.ret_url)}, 
                access_token=access_token,
                callback=self.async_callback(self._on_post))
        else:
            self.finish(self.ret_url)

    def _on_post(self, resp):
        if not resp:
            self.finish("Something Went Wrong!")
        self.finish(self.ret_url)

def parse_retrieve(uri_split):
    username = uri_split[-2]
    asset = uri_split[-1].replace('.p','')
    return (username, asset)

def retrieve_message(user, asset, storage_dir, protected=False):
    if not user or not asset:
        return None
    file_path = os.path.join(storage_dir, user, asset)
    asset_p = "%s.p" % asset
    file_path_protected = os.path.join(storage_dir, user, asset_p)
    if os.path.exists(file_path):
        with open(file_path, 'rU') as file:
            return file.read()
    if os.path.exists(file_path_protected):
        if protected:
            with open(file_path_protected, 'rU') as file:
                return file.read()
        else:
            return 'p'
    return None

class RetrieveMessage(core.BaseHandler):
    def get(self):
        (username, asset) = parse_retrieve(self.request.uri.split("/"))
        storage_dir = self.settings['storage_dir']
        message = retrieve_message(username, asset, storage_dir)
        if message == 'p':
            self.redirect("/retpro/%s/%s" % (username, asset))
            return
        elif message:
            self.write("<pre>\n")
            self.write(message)
            self.write("\n</pre>")
            return
        self.send_error(status_code=404)

class RetrieveProtectedMessage(core.BaseHandler, tornado.auth.TwitterMixin):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        (self.username,
         self.asset) = parse_retrieve(self.request.uri.split("/"))
        self.storage_dir = self.settings['storage_dir']
        access_token = self.get_access_token()
        self.twitter_request(
            "/users/show",
            screen_name=self.username,
            access_token=access_token,
            callback=self.async_callback(self._on_get))

    def _on_get(self, resp):
        if 'status' in resp:
            message = retrieve_message(self.username,
                                       self.asset,
                                       self.storage_dir,
                                       protected=True)
            if message: 
                self.write("<pre>\n")
                self.write(message)
                self.write("\n</pre>")
                self.finish()
                return
            else:
                self.send_error(status_code=404)
                return
        self.send_error(status_code=401)
