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

class IndexHandler(BaseHandler):

    def get(self):

        self.render("mobile/index.html")

class LoginHandler(BaseHandler):

    def get(self):

        self.redirect("/#login-page", permanent=True)

    @Session
    def post(self):
        school_num = self.get_argument("username", None)
        password = self.get_argument("password", None)
        autologin = self.get_argument("autologin", None)

        template_values = dict()
        template_values["status"] = False

        if not school_num:
            template_values["err_msg"] = u"学号为空"
            return self.write_json(template_values)
        elif not password:
            template_values["err_msg"] = u"密码为空"
            return self.write_json(template_values)

        gench = JWXT()
        gench.set_user(school_num, password)
        login_status = gench.login()

        if login_status == u"登录成功":
            self.session["gench"] = gench
            if autologin == '1':
                print "autologin"
                self.session["permanent"] = True

            template_values["status"] = True
            template_values["err_msg"] = u"登录成功"
            return self.write_json(template_values)

        template_values["err_msg"] = login_status

        return self.write_json(template_values)

class LogoutHandler(BaseHandler):
    @Session
    def get(self):
        self.session.kill()
        #template_values = dict()
        #template_values["status"] = True
        #template_values["err_msg"] = u"登出成功"

        #self.write_json(template_values)
        self.redirect("/", permanent=True)

class UserHandler(BaseHandler):
    @authenticated
    @Session
    def get(self):

        template_values = dict()
        week = datetime.now().weekday()
        if week > 4:
            week = 0
        template_values["week_now"] = week

        self.render("mobile/user.html", **template_values)


class CourseHandler(BaseHandler):
    @authenticated
    @Session
    def get(self):

        gench = self.session["gench"]
        courses = gench.get_course()
        template_values = dict()
        template_values["courses"] = courses
        self.render("mobile/course_table.html", **template_values)


class GradeHandler(BaseHandler):

    @authenticated
    @Session
    def get(self):

        semester = self.get_argument("s", None)
        term = self.get_argument("t", None)

        if term and semester:
            gench = self.session["gench"]
            grade = gench.get_grade_by_semester(semester, term, raw=False)
            return self.write("%r" % grade)

        gench = self.session["gench"]
        grade = gench.get_grade()
        template_values = dict()
        template_values["grade"] = grade

        self.render("mobile/grades.html", **template_values)



class DakaHandler(BaseHandler):
    """打卡查询"""

    @authenticated
    def get(self):
        self.render("mobile/daka.html")

    @authenticated
    @Session
    def post(self):
        birthday = self.get_argument("birthday")
        template_values = dict()
        template_values["error"] = False
        try:
            birthday = "".join(birthday.split('-'))
        except:
            template_values["error"] = True
            template_values["error_msg"] = "生日输入错误"
            return self.render("mobile/daka_result.html", **template_values)

        gench = self.session["gench"]
        number = int(gench.school_num)
        sport = Sport(number, birthday)
        if not sport.login():
            template_values["error"] = True
            template_values["error_msg"] = "生日错误，请重试"
            return self.render("mobile/daka_result.html", **template_values)

        count, info = sport.get_score()

        template_values["count"] = count
        template_values["info"] = info
        self.render("mobile/daka_result.html", **template_values)


class MainNewsHandler(BaseHandler):

    def get(self):
        news = get_main_news()

        template_values = dict()
        template_values["news"] = news
        template_values["page_title"] = u"建桥要闻"

        self.render("mobile/news.html", **template_values)

class PublicNewsHandler(BaseHandler):

    def get(self):
        news = get_public_news()

        template_values = dict()
        template_values["news"] = news
        template_values["page_title"] = u"信息公开"

        self.render("mobile/news.html", **template_values)


class CETHandler(BaseHandler):

    def get(self):
        self.render("mobile/cet.html")

    def post(self):

        number = self.get_argument("number")
        name = self.get_argument("name")

        template_values = dict()
        template_values["result"] = get_last_cet_score(number, name)


        self.render("mobile/cet_result.html", **template_values)


class EatHandler(BaseHandler):

    def get(self):

        self.render("mobile/eat.html")


class CreditHandler(BaseHandler):

    @authenticated
    def get(self):

        self.render("mobile/credit.html")

    @authenticated
    @Session
    def post(self):

        semester = self.get_argument("semester")

        semester, term = semester.split(":")[0], semester.split(":")[1]

        gench = self.session["gench"]

        credit_base, credit_reward = gench.get_credit(semester, int(term))
        template_values = dict()
        template_values["credit_base"] = credit_base
        template_values["credit_reward"] = credit_reward
        template_values["semester"] = semester
        template_values["term"] = term

        self.render("mobile/credit_result.html", **template_values)
