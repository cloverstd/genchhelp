#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

def DesktopOnly(func):
    @functools.wraps(func)
    def wraps(self, *args, **kwargs):

        ua = self.request.headers["User-Agent"]
        if ua.find("X11; Windows NT") != -1 or\
            ua.find("X11; Linux x86_64") != -1 or \
            ua.find("Macintosh") != -1:
            print "Desktop"
            return self.redirect("/d", permanent=True)

        result = func(self, *args, **kwargs)

        return result

    return wraps

