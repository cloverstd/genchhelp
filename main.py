#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options, parse_command_line
from routes import routes
import os
import redis
from lib.session import RedisSessionBackend

define("port", default=8080, type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class Application(tornado.web.Application):

    def __init__(self):
        setting = dict(debug=True,
                       autoescape=None,
                       template_path=os.path.join(os.path.dirname(__name__), "templates"),
                       #static_path=os.path.join(os.path.dirname(__name__), "static"),
                       cookie_secret="key",
                       xsrf_cookies=True,
                       login_url="/login",
                       )

        super(Application, self).__init__(handlers=routes, **setting)

        # Session
        self.redis = redis.Redis()
        self.session_backend = RedisSessionBackend(self.redis, secret_key="This is a key")

if __name__ == "__main__":
    parse_command_line()
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
