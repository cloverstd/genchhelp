#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

class Semester(dict):
    def __init__(self, *args, **kwargs):
        #self.data = {"2010-2011": [286, 201],
                     #"2011-2012": [221, 222],
                     #"2012-2013": [328, 329],
                     #"2013-2014": [330, 331]}
        self.update({"2010-2011": [286, 201]})
        self.update({"2011-2012": [221, 222]})
        self.update({"2012-2013": [328, 329]})
        self.update({"2013-2014": [330, 331]})

    def current_id(self):
        start_year, end_year, term = self._get_info()

        semester = "%s-%s" % (start_year, end_year)

        return self[semester][term]

    def next_id(self):
        start_year, end_year, term = self._get_info()
        now = datetime.now()
        if now.month > 8:
            semester = "%s-%s" % (start_year, end_year)
            return self[semester][term + 1]

        semester = "%s-%s" % (start_year+1, end_year+1)
        return self[semester][term-1]

    def prev_id(self):
        start_year, end_year, term = self._get_info()
        now = datetime.now()
        if now.month > 8:
            semester = "%s-%s" % (start_year-1, end_year-1)
            return self[semester][term + 1]

        semester = "%s-%s" % (start_year, end_year)
        return self[semester][term-1]



    def _get_info(self):
        """
        计算 start year, end year, term
        """
        now = datetime.now()
        term = 1
        if now.month > 8:
            term = 0
            start_year = now.year
            end_year = now.year+1
            return start_year, end_year, term

        start_year = now.year-1
        end_year = now.year
        return start_year, end_year, term




if __name__ == '__main__':
    a = Semester()
    print a.current_id()

    print a.next_id()
    print a.prev_id()
