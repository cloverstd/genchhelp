# coding: utf-8


from . import BaseHandler
import sys
import os
sys.path.append(os.path.dirname(__name__))
from spider.jwxt import JWXT


class LoginHandler(BaseHandler):

    def post(self):
        school_num = self.get_argument("school_num", None)
        password = self.get_argument("password", None)

        json_values = dict()
        json_values["status"] = False

        if not school_num:
            json_values["err_msg"] = u"学号为空"
            return self.write_json(json_values)
        elif not password:
            json_values["err_msg"] = u"密码为空"
            return self.write_json(json_values)

        gench = JWXT()
        gench.set_user(school_num, password)
        login_status = gench.login()

        if login_status == u"登录成功":
            self._login(gench)
            json_values["status"] = True
            json_values["err_msg"] = u"登录成功"
            return self.write_json(json_values)

        json_values["err_msg"] = login_status

        return self.write_json(json_values)


class LogoutHandler(BaseHandler):

    def get(self):
        self._logout()
        json_values = dict()
        json_values["status"] = True
        json_values["err_msg"] = u"登出成功"

        self.write_json(json_values)



class CourseTableHandler(BaseHandler):
    def get(self):
        gench = self.session["gench"]

        course = gench.get_course()

        self.write_json(course)
