
import tornado.web
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):

    def get_access_token(self):
        access_token = self.get_secure_cookie("access_token")
        return tornado.escape.json_decode(access_token)

    def get_current_user(self):
        access_token = self.get_secure_cookie("access_token")
        if not access_token:
            return None
        access_token = tornado.escape.json_decode(access_token)
        return access_token['screen_name'] 

    def get_current_root(self):
        path = self.request.path
        full_url = self.request.full_url()
        return full_url.replace(path, '')
