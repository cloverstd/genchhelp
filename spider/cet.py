# coding: utf-8


import requests
from lib.proxy import get_proxy
from BeautifulSoup import BeautifulSoup
import re


def get_last_cet_score(zkzh, xm):

    url = "http://www.chsi.com.cn/cet/query"


    #data = {
            #"zkzh": zkzh,
            #"xm":xm
            #}
    headers = {
            "Host": "www.chsi.com.cn",
            "Referer": "http://www.chsi.com.cn/cet/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.114 Safari/537.36",
            }
    proxies = {"http": get_proxy()}
    req = requests.get("%s?zkzh=%s&xm=%s" % (url, zkzh, xm), headers=headers, proxies=proxies)

    soup = BeautifulSoup(req.text)

    soup = soup.table.findAll('td')

    result = dict()

    try:
        result['name'] = soup[0].text
        result['school'] = soup[1].text
        result['type'] = soup[2].text
        result['number'] = soup[3].text
        result['time'] = soup[4].text
        score = soup[5].findAll(text=re.compile(ur'[0-9]+'))
        result['total'] = score[0].replace('&nbsp;', '')
        result['listen'] = score[1].replace('&nbsp;', '')
        result['read'] = score[2].replace('&nbsp;', '')
        result['com'] = score[3].replace('&nbsp;', '')
        result['write'] = score[4].replace('&nbsp;', '')
        result['error'] = False
    except:
        result['error'] = True

    return result
