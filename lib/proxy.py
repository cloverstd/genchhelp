#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from BeautifulSoup import BeautifulSoup
from random import randint
from time import ctime
from cache import CommonCache

def get_proxy():

    proxies = get_proxies()

    second = int(str(ctime())[-7:-5])
    return proxies[second]

    #proxy = dict(http=proxies[randint(0, len(proxies)-1)])

    #return proxy

    #req = requests.get("http://www.telize.com/ip", proxies=proxy)
    #print req.text

@CommonCache(expires=9000)
def get_proxies():
    req = requests.get("http://www.site-digger.com/html/articles/20110516/proxieslist.html")

    soup = BeautifulSoup(req.text)

    soup = soup.table.tbody('td')

    proxies = list()

    for i in range(0, len(soup), 3):
        proxies.append("http://%s" % soup[i].text)

    return proxies
