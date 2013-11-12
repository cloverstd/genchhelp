#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import string
import json
import requests
import functools
import redis
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    import hashlib
    sha1 = hashlib.sha1
except ImportError:
    import sha
    sha1 = sha.new

BASE_URL = "http://jwxt.gench.edu.cn/eams/"
LOGIN_URL = "login.action"
COURSE_URL = "courseTableForStd!courseTable.action"
GRADE_URL = "teach/grade/course/person!historyCourseGrade.action"

_redis_cache = redis.StrictRedis()

def _compute_key(function, *args, **kwargs):
    key = pickle.dumps((function.func_name, args, kwargs))
    return sha1(key).hexdigest()

def _prefix(key):
    return "Cache: %s" % key

def cache(func):
    @functools.wraps(func)
    def wraps(self, *args, **kwargs):
        key = _compute_key(func, self.school_num, *args, **kwargs)
        if _redis_cache.exists(_prefix(key)):
            return pickle.loads(_redis_cache.get(_prefix(key)))

        result = func(self, *args, **kwargs)

        pickled = pickle.dumps(result)
        pipe = _redis_cache.pipeline()
        pipe.set(_prefix(key), pickled)
        pipe.expire(_prefix(key), 86400) # 24 * 60 * 60 # 1 day
        pipe.execute()

        return result

    return wraps


class JWXT(object):

    def __init__(self):
        self.base_url = BASE_URL
        self.login_url = self.base_url + LOGIN_URL
        self.code_url = self.base_url + "security/captcha.action"
        self.course_url = self.base_url + COURSE_URL
        self.ids_url = self.base_url + "courseTableForStd.action"
        self.grade_url = self.base_url + GRADE_URL

        self.headers = {
                'Referer': self.base_url,
                'Origin': self.base_url[:-6],
                'Host': self.base_url[7:-6],
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64)\
                        AppleWebKit/537.36 (KHTML, like Gecko)\
                        Chrome/30.0.1599.101 Safari/537.36",
                'Connection': 'Keep-Alive',
                }

        self.session = requests.Session()
        self.session.headers.update(self.headers)


    def set_user(self, school_num, password):
        self.school_num = school_num
        self.password = password

    def login(self):
        # 验证码似乎不需要了
        data = {
                'username': self.school_num,
                'password': self.password,
                'encodedPassword': '',
                }
        req = self.session.post(self.login_url, data=data)
        if req.text.find(u"账户不存在") != -1:
            return u"用户名错误"
        elif req.text.find(u"密码错误") != -1:
            return u"密码错误"
        elif req.text.find(self.school_num) != -1:
            return u"登录成功"
        else:
            return u"登录失败"

        return req.text

    def get_ids(self):
        self.login()

        text = self._get_html(self.ids_url)
        key = re.compile(ur'form,"ids","(\d+)"')
        ids = re.findall(key, text)[0]
        return ids

    def _get_html(self, url):
        return self.session.get(url).text

    @cache
    def get_course(self):
        """
        semester.id 说明
        330 2013-2014 1学期
        331 2013-2014 2学期
        startWeek  说明，对应startWeek周课表
        """
        data = {"ignoreHead": 1,
                "setting.kind": "std",
                "startWeek": 1,
                "semester.id": 330,     # 学期 ID
                "ids": self.get_ids(),  # 每人唯一 ID
            }

        req = self.session.post(self.course_url, data=data)
        course_unicode = self._parser_course(req.text)
        return self._course2list(course_unicode)

    def _parser_course(self, content):
        #key = ur"""var adminClassId="\d+";(.*)table0\.marshalTable"""
        key = ur"""\/\/activity.*activities\[index\]\.length\]=activity;"""

        # 取得课表段 js
        rv = re.findall(re.compile(key, re.DOTALL), content)

        # 替换掉里面的\t
        tb = string.maketrans("\n\r\t", "\n\n\n")
        # Unicode translate
        rv = rv[0].encode("utf-8").translate(tb, "\t").decode("utf-8")

        # 删掉里面多余的地方
        rv = re.sub(re.compile("\/\/.*"), "", rv)
        rv = re.sub(re.compile("table0.*"), "", rv)
        # 删掉里面的多余的换行，方便接下来的处理
        rv = rv.replace("\n\n\n", "\n")

        # 删掉第一个\n
        rv = rv[1:]

        # 格式化一下方便操作
        rv = rv.replace("activity = new TaskActivity(", "\n")
        rv = rv.replace(");", "||||")
        rv = rv.replace("index =", "week:")
        rv = rv.replace("*unitCount+", "&&row:")
        rv = rv.replace(";", "||")

        rv = rv.split('\n\n')

        #print rv, len(rv)

        rv = ''.join(rv)

        # 去掉第一个\n
        #rv = rv[0:]

        return rv

    def _course2list(self, course_unicode):
        """转换course_unicode源数据为list"""
        courses = list()
        def get_course(raw):
            """从course源数据里得到course"""
            temp = "[%s]" % raw
            temp = json.loads(temp)
            if temp[5] == "":
                temp[5] = None
            return dict(teacher=temp[1],
                        name=temp[3],
                        room=temp[5])


        def get_date(raw):
            """从course源数据里得到date"""
            raw = ''.join(raw).split('||')[:-1]
            def get_date_from(raw):
                raw = raw.split('&&')
                week = raw[0][5:]
                row = raw[1][4:]
                return dict(week=int(week),
                            row=int(row))

            return [get_date_from(i) for i in raw]

        for line in course_unicode.split('\n'):
            temp = line.split('||||')
            course = get_course(temp[0])
            course_date = get_date(temp[1:])

            courses.append(dict(course=course, course_date=course_date))


        #course_table = list()
        #for i in range(5):
            ## week
            #course_week = list()
            #for j in range(16):
                #for course in courses:
                    #for date in course["course_date"]:
                        #if date["week"] == i and date["row"] == j:
                            #course_dict = dict(course=course["course"],
                                          #index=(i, j))
                            #course_week.append(course_dict)
                            #break
            #course_table.append(course_week)
        course_table = list()
        for i in range(5):
            week = list()
            for j in range(16):
                week.append(None)
            course_table.append(week)

        for i in range(5):
            # week
            course_week = list()
            for j in range(16):
                for course in courses:
                    for date in course["course_date"]:
                        if date["week"] == i and date["row"] == j:
                            course_table[i][j] = course["course"]
                            break
                    if course_table[i][j] is not None:
                        break
                            #course_dict = dict(course=course["course"],
                                            #index=(i, j))
                            #course_week.append(course_dict)
            course_table.append(course_week)

        return course_table

    @cache
    def get_grade(self):
        self.login()
        data = dict(projectType="MAJOR")

        key = re.compile(ur'<table.*<\/table>', re.S)
        req = self.session.post(self.grade_url, data=data)
        rv = re.findall(key, req.text)

        return rv[0]


#if __name__ == '__main__':
    #jwxt = JWXT()
    #jwxt.set_user('1121276', "wsaw2931336")
    #content = jwxt.login()
    #print content
