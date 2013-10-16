#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv
import json

class TblracsCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_user, options_rules, options_lang, options_struct,options_key_path):
        super(TblracsCSV, self).__init__(delim)
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_lang = options_lang
        self.options_struct = options_struct
        self.options_key_path = options_key_path

    def procRecordToList(self,d):
        record = []
        try:
            if "verb" in d:
                verb = d["verb"]
            else:
                msg = "Unidentified meta message"
                for mtype in ["error", "warning", "info"]:
                    if mtype in d:
                        if "message" in d[mtype]:
                            msg = d[mtype]["message"]
                        elif "message" in d:
                            msg = d["message"]
                        continue
                    mtype = "Unidentified"
                record.append(acscsv.gnipRemove)
                record.append(mtype)
                record.append(msg)
                return record
            if verb == "delete":
                record.append(d["id"])
                record.append(acscsv.gnipRemove)
                record.append(verb)
                return record
            elif verb == "update":
                # process as usual
                pass
            #
            record.append(d["id"])
            record.append(d["postedTime"])
            #
            gnip = d["gnip"]
            actor = d["actor"]
            obj = d["object"] 
            if "summary" in obj and obj["summary"] is not None:
                record.append(self.cleanField(obj["summary"]))
            elif "content" in obj and obj["content"] is not None:
                record.append(self.cleanField(obj["content"]))
            else:
                record.append("None")
            record.append(obj["objectType"])
            if self.options_lang:
                glang = "None"
                if "language" in gnip:
                    glang = gnip["language"]["value"]
                record.append(glang)
            if self.options_rules:
                rules = '[]'
                if "matching_rules" in gnip:
                    rules = self.buildListString([ "%s [%s]"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            if self.options_struct:
                # site
                record.append(obj["link"])
                if "tumblrRebloggedFrom" in d:
                    # thread - 1
                    reblogged_from = d["tumblrRebloggedFrom"]
                    record.append(reblogged_from["link"])
                    # thread root
                    reblogged_root = d["tumblrRebloggedRoot"]
                    record.append(reblogged_from["link"])
                elif "inReplyTo" in d:
                    record.append("None")
                    record.append(d["inReplyTo"]["author"]["link"])
                else:
                    record.append("None")
                    record.append("None")
            if self.options_user:
                try:
                    tmp = actor["id"].split("/")[1]
                except IndexError:
                    tmp = "actor:id"
                record.append(tmp)
            #key_path
            if self.options_key_path:
                buildstring=''
                kp=self.options_key_path.split(":")
                for num in range(0,len(kp)):
                    try:
                        buildstring+='["{0}"]'.format(str(kp[num]))
                        exec("kp_output=d{0}".format(buildstring))
                        if num==len(kp)-1:
                            record.append(json.dumps(kp_output))                    
                    except KeyError,e:
                        record.append("PATH_EMPTY")
                        sys.stderr.write("-- KeyError: {0} , Line: {1} , path_end: {2} --".format(e,self.cnt,kp[num]))
                        break
                    except TypeError,e:
                        record.append("PATH_EMPTY")
                        sys.stderr.write("-- TypeError: {0} , Line: {1} , path_end: {2} --".format(e,self.cnt,kp[num]))
                        break
                    except IndexError,e:
                        record.append("PATH_EMPTY")
                        sys.stderr.write("-- IndexError: {0} , Line: {1} , path_end: {2} --".format(e,self.cnt,kp[num]))
                        break 
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            return record
