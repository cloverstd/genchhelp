#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re

url = "http://211.80.112.212/Default.aspx"
url_score = "http://211.80.112.212/stScore.aspx"
URL_BASE = "http://211.80.112.212/"
from BeautifulSoup import BeautifulSoup
from lib import cache

class Sport(object):

    def __init__(self, username, password):

        self.URL_BASE = "http://211.80.112.212/"
        self.url_login = self.URL_BASE + "Default.aspx"

        self.url_login = "http://211.80.112.212/Default.aspx"
        self.url_score = "http://211.80.112.212/stScore.aspx?item=1"

        self.username = str(username)
        self.password = str(password)
        self.session = requests.Session()

    def check_status(self):

        req = requests.get(self.URL_BASE)
        return bool(req.status_code == requests.codes.ok)

    @cache.CommonCache(expires=7200)
    def _get_viewstate(self):

        req = requests.get(self.URL_BASE)
        viewstate = re.compile(ur'__VIEWSTATE.+').findall(req.text)[0]
        return re.compile(ur'=".+"').findall(viewstate)[0][2:-1]

    def login(self):
        data = {
                "__EVENTTARGET"   : "",
                "__EVENTARGUMENT" : "",
                "__VIEWSTATE"     : self._get_viewstate(),
                "dlljs"           : "st",
                "txtuser"         : self.username,
                "txtpwd"          : self.password,
                "btnok.x"         : 33,
                "btnok.y"         : 19,
                }

        req = self.session.post(self.url_login, data=data)

        rv = req.text.encode("utf-8")

        return bool(rv.find("补刷卡")!=-1 and rv.find("早操")!=-1)

    def get_score(self):
        req = self.session.get(self.url_score.decode("utf-8"))

        soup = BeautifulSoup(req.content)

        count_table = soup.findAll("table")[11]
        info_table = soup.findAll("table")[14]


        def walk_table(table):
            return filter(lambda x: bool(x), [[col.text for col in row.findAll('td')]
                    for row in table.findAll('tr')])

        return walk_table(count_table), walk_table(info_table)
