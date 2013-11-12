#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from lib.cache import CommonCache

@CommonCache(expires=1800)
def get_main_news():
    url = "http://news.gench.edu.cn/s/24/t/171/main.htm"

    req = requests.get(url)

    soup = BeautifulSoup(req.text)

    news = soup("table", align="center")[0].findAll('a')

    news_main = list()

    for new in news:
        if new["href"][:4] == "http":
            news_main.append(dict(href=new["href"],
                                  title=new["title"]))
        else:
            news_main.append(dict(href="http://news.gench.edu.cn%s" % new["href"],
                                title=new["title"]))

    return news_main


@CommonCache(expires=1800)
def get_public_news():
    url = "http://i.gench.edu.cn/s/119/t/169/main.htm"

    req = requests.get(url)

    soup = BeautifulSoup(req.text)

    news = soup("table", align="center")[0].findAll('a')

    news_public = list()

    for new in news:
        if new["href"][:4] == "http":
            news_public.append(dict(href=new["href"],
                                title=new["title"]))
        else:
            news_public.append(dict(href="http://i.gench.edu.cn%s" % new["href"],
                                    title=new["title"]))
    return news_public
