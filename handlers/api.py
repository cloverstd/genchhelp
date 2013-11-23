# coding: utf-8


from . import BaseHandler
import sys
import os
import tornado.util
import functools
sys.path.append(os.path.dirname(__name__))
from spider.jwxt import JWXT
from spider.cet import get_last_cet_score
from lib.session import Session
from spider.sport import Sport
from spider.news import get_main_news, get_public_news

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.write_msg("请先登录")
            return self.dumps()
        return method(self, *args, **kwargs)
    return wrapper



class BaseAPIHandler(BaseHandler):

    def __init__(self, *args, **kwargs):
        super(BaseAPIHandler, self).__init__(*args, **kwargs)
        self.json_values = tornado.util.ObjectDict()
        self.json_values["status"] = True
        self.json_values["err_msg"] = None

    def dumps(self):
        return self.write_json(self.json_values)

    def status_false(self):
        self.json_values["status"] = False

    def write_msg(self, msg):
        self.status_false()
        self.json_values["err_msg"] = msg.decode("utf-8")


class LoginHandler(BaseAPIHandler):

    @Session
    def get(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)

        if not username or not password:
            self.write_msg("用户名或密码为空")
            return self.dumps()

        gench = JWXT()
        gench.set_user(username, password)
        if gench.login() != u"登录成功":
            self.write_msg("用户名或密码错误")
            return self.dumps()

        self.session["gench"] = gench
        self.session["permanent"] = True

        return self.dumps()

class LogoutHandler(BaseAPIHandler):

    @Session
    def get(self):
        self.session.kill()
        return self.dumps()


class GradeHandler(BaseAPIHandler):

    @authenticated
    @Session
    def get(self, start, end, term):
        start = int(start)
        end = int(end)
        term = int(term) - 1
        if start+1 != end:
            self.write_msg("学期输入不正确")
            return self.dumps()

        gench = self.session["gench"]
        semester = "%s-%s" % (start, end)
        try:
            grade = gench.get_grade_by_semester(semester, term, False)
        except KeyError:
            grade = None
            self.write_msg("学期输入不正确")

        self.json_values.grade = grade
        return self.dumps()


class CourseHandler(BaseAPIHandler):

    @authenticated
    @Session
    def get(self):

        gench = self.session["gench"]
        course = gench.get_course()

        self.json_values.course = course
        return self.dumps()


class DakaHandler(BaseAPIHandler):

    def get(self, username, password):

        password = int(password)

        sport = Sport(username, password)

        if not sport.login():
            self.write_msg("学号或者生日错误")
            return self.dumps()

        count, info = sport.get_score()

        self.json_values.count = count
        self.json_values.info = info


        return self.dumps()


class CreditHandler(BaseAPIHandler):

    @authenticated
    @Session
    def get(self, start, end, term):

        start = int(start)
        end = int(end)
        term = int(term) - 1
        if start+1 != end:
            self.write_msg("学期输入不正确")
            return self.dumps()

        gench = self.session["gench"]
        semester = "%s-%s" % (start, end)

        credit_base, credit_reward = gench.get_credit(semester, term)

        self.json_values.credit_base = credit_base
        self.json_values.credit_reward = credit_reward

        return self.dumps()


class CETHandler(BaseAPIHandler):

    def get(self):

        number = self.get_argument("number", None)
        name = self.get_argument("name", None)

        if not number or not name:
            self.write_msg("准考证或姓名为空")
            return self.dumps()

        rv = get_last_cet_score(number, name[:3])
        if rv["error"]:
            self.write_msg("没有结果，请确定准考证号或姓名正确")
            return self.dumps()

        self.json_values.cet = rv
        return self.dumps()


class MainNewsHandler(BaseAPIHandler):

    def get(self):

        news = get_main_news()

        self.json_values.news = news
        return self.dumps()


class PublicNewsHandler(BaseAPIHandler):

    def get(self):

        news = get_public_news()

        self.json_values.news = news
        return self.dumps()
