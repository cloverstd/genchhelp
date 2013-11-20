# coding: utf-8

from . import BaseHandler
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(__name__))
from spider.jwxt import JWXT
from spider.news import get_main_news, get_public_news
from tornado.web import authenticated
from lib.session import Session
from spider.cet import get_last_cet_score
from spider.sport import Sport
import config

class IndexHandler(BaseHandler):

    def get(self):

        self.render("desktop/index.html")


class CETHandler(BaseHandler):

    def get(self):

        self.render("desktop/cet.html")

    def post(self):

        number = self.get_argument("number", None)
        name = self.get_argument("name", None)
        print number, name

        template_values = dict()
        template_values["result"] = get_last_cet_score(number, name)

        self.render("desktop/cet_result.html", **template_values)


class DakaHandler(BaseHandler):

    def get(self):
        self.render("desktop/daka.html")

    def post(self):
        number = self.get_argument("number", None)
        birthday = self.get_argument("birthday", None)

        template_values = dict()
        template_values["error"] = False

        sport = Sport(number, birthday)
        if not sport.login():
            template_values["error"] = True
            template_values["error_msg"] = "生日或者学号错误"
            return self.render("desktop/daka_result.html", **template_values)


        count, info = sport.get_score()

        template_values["count"] = count
        template_values["info"] = info

        self.render("desktop/daka_result.html", **template_values)

class CommentHandler(BaseHandler):

    def get(self):
        ua = self.request.headers["User-Agent"]
        template_values = dict()
        template_values["duoshuo"] = config.DUOSHUO

        if ua.find("X11; Windows NT") != -1 or\
            ua.find("X11; Linux x86_64") != -1 or \
            ua.find("Macintosh") != -1:

            return self.render("desktop/comment.html", **template_values)

        return self.render("mobile/comment.html", **template_values)


class AboutHandler(BaseHandler):

    def get(self):
        self.render("desktop/about.html")
