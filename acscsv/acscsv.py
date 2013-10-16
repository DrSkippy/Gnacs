#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import datetime
import json
gnipError = "GNIPERROR"
gnipRemove = "GNIPREMOVE"
gnipDateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

class AcsCSV(object):
    def __init__(self, delim,options_keypath):
        self.delim = delim
        self.cnt = None
        self.options_keypath = options_keypath

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
        source_list = self.procRecordToList(x)
        if self.options_keypath:
            source_list.append(self.keyPath(x))
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
                    idx = str(k)
                x = x[idx]
            except (IndexError, TypeError, KeyError) as e:
                sys.stderr.write("Keypath error at %s\n"%k)
                return "PATH_EMPTY"
        return str(x)
        #kp = self.options_keypath.split(":")
        #buildstring=''
        #output = "PATH_EMPTY"
        #for num in range(0,len(kp)):
        #    try:
        #        buildstring+='["{0}"]'.format(str(kp[num]))
        #        exec("kp_output=d{0}".format(buildstring))
        #        if num==len(kp)-1:
        #            output = json.dumps(kp_output)                    
        #    except (KeyError, TypeError, IndexError) as e:
        #        sys.stderr.write("Custom Keypath Error: {0} , Line: {1} , path_end: {2} \n".format(e,self.cnt,kp[num]))
        #        break
        #return output
