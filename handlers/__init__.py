# coding: utf-8


import tornado.web
import json
from lib.session import Session


class BaseHandler(tornado.web.RequestHandler):

    def write_json(self, d):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(d))

    @Session
    def _login(self, gench):
        self.session["gench"] = gench

    @Session
    def _logout(self):
        self.session.clear()

    @Session
    def get_current_user(self):
        if "gench" in self.session:
            return True
        return False

    def write_error(self, status_code, **kwargs):
        if status_code == 411:
            self.redirect("/#login-page", permanent=True)

        self.write("%r%s" % (kwargs, status_code))

    def check_xsrf_cookie(self):
        if not self.request.path.startswith("/api"):
            tornado.web.RequestHandler.check_xsrf_cookie(self)
