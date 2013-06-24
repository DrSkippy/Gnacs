#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"

import datetime

gnipError = "GNIPERROR"
gnipRemove = "GNIPREMOVE"
gnipDateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

class AcsCSV(object):
    def __init__(self, delim):
        self.delim = delim
        self.cnt = None

    def cleanField(self,f):
        return f.strip().replace("\n"," ").replace("\r"," ").replace(self.delim, " ")

    def buildListString(self,l):
        # unicode output of list (without u's)
        res = '['
        for r in l:
            res += "'" + r + "',"
        if res.endswith(','):
            res = res[:-1]
        res += ']'
        return res

    def splitId(self, x):
        tmp = x.split("/")
        if len(tmp) > 1:
            return tmp[1]
        else:
            return x

    def asString(self,l):
        if l is None:
            return None
        return self.delim.join(l)

    def procRecord(self, cnt, x):
        self.cnt = cnt
        return self.asString(self.procRecordToList(x))
