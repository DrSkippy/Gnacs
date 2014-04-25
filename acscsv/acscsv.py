#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import datetime
import json
import unittest

gnipError = "GNIPERROR"
gnipRemove = "GNIPREMOVE"
gnipDateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

class TestAcsCSV(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCleanField(self):
        a = AcsCSV("|", False)
        self.assertEquals(a.cleanField("laksjflasjdfl;a"), "laksjflasjdfl;a")
        self.assertEquals(a.cleanField("\r\n \n\r \r\r \n\n"), "")
        self.assertEquals(a.cleanField("\r\na \n\r \r\r a\n\n"), "a       a")
        self.assertEquals(a.cleanField("asdf|asdf,,adsf|asdf"), "asdf asdf,,adsf asdf")
        b = AcsCSV(",", False)
        self.assertEquals(b.cleanField("asdf|asdf,,adsf|asdf"), "asdf|asdf  adsf|asdf")
        self.assertEquals(b.cleanField(245), "245")
        self.assertEquals(b.cleanField(a), "None")

class AcsCSV(object):
    def __init__(self, delim, options_keypath, options_db):
        self.delim = delim
        if delim == "":
            print >>sys.stderr, "Warning - Output has Null delimiter"
        self.cnt = None
        self.options_keypath = options_keypath
        self.options_db = options_db

    def cleanField(self,f):
        try:
            # odd edge case that f is a number
            # then can't call string functions
            float(f)
            f = str(f)
        except ValueError:
            pass
        except TypeError:
            f = "None"
        return f.strip(
                ).replace("\n"," "
                ).replace("\r"," "
                ).replace(self.delim, " "
                )

    def buildListString(self,l):
        # unicode output of list (without u's)
        res = '['
        for r in l:
            res += "'" + r + "',"
        if res.endswith(','):
            res = res[:-1]
        res += ']'
        return res

    def splitId(self, x, index=1):
        tmp = x.split("/")
        if len(tmp) > index:
            return tmp[index]
        else:
            return x

    def asString(self,l):
        if l is None:
            return None
        # debug
        #print >>sys.stderr, "list l={}".format(l) 
        #
        return self.delim.join(l)

    def procRecord(self, cnt, x):
        self.cnt = cnt
        source_list = self.procRecordToList(x)
        if self.options_keypath:
            source_list.append(self.keyPath(x))
        # ensure no pipes, newlines, etc
        #TODO: remove calls to cleanField() in submodules
        source_list = [ self.cleanField(x) for x in source_list ]
        return self.asString(source_list)

    def asGeoJSON(self, cnt, x):
        recordList = self.procRecordToList(x)
        if self.__class__.__name__ == "TwacsCSV" and self.options_geo:
            if self.geoCoordsList is None:
                return
            lon_lat = self.geoCoordsList[::-1]
        elif self.__class__.__name__ == "FsqacsCSV" and self.options_geo:
            lon_lat = self.geo_coords_list
        else:
            return {"Error":"This publisher doesn't have geo"}
        return {"type": "Feature", "geometry": { "type": "Point", "coordinates": lon_lat }, "properties": {"id": recordList[0]} }
    
    def keyPath(self,d):
        key_list = self.options_keypath.split(":")
        key_stack = self.options_keypath.split(":")
        x = d
        while len(key_stack) > 0:
            try:
                k = key_stack.pop(0)
                try:
                    idx = int(k)
                except ValueError:
                    # keys are ascii strings
                    idx = str(k)
                x = x[idx]
            except (IndexError, TypeError, KeyError) as e:
                sys.stderr.write("Keypath error at %s\n"%k)
                return "PATH_EMPTY"
        return str(x)

if __name__ == "__main__":
    unittest.main()
