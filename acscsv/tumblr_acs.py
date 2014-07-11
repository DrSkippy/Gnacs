#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv

class TblracsCSV(acscsv.AcsCSV):
    """Tumblr activities"""
    def __init__(self, delim, options_keypath, options_user, options_rules, options_lang, options_struct):
        super(TblracsCSV, self).__init__(delim,options_keypath)
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_lang = options_lang
        self.options_struct = options_struct

    def procRecordToList(self,d):
        """Take a JSON Activity Streams payload as a Python dictionary. Check 
        activity for system information and compliance handling. If necessary, 
        return the system info or compliance message. Otherwise, if the activity 
        is valid, return list of fields as specified by the input flags.
        
        Flags::

            delim
            options_keypath
            options_user
            options_rules
            options_lang
            options_struct

        """

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
                #record.append(self.cleanField(obj["summary"]))
                record.append(obj["summary"])
            elif "content" in obj and obj["content"] is not None:
                #record.append(self.cleanField(obj["content"]))
                record.append(obj["content"])
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
                    # there is no reblogged from
                    record.append("None")
                    # consider case where "link = null"
                    link = d["inReplyTo"]["author"]["link"]
                    if link is None:
                        record.append("None")
                    else:
                        record.append(d["inReplyTo"]["author"]["link"])
                else:
                    record.append("None")
                    record.append("None")
            if self.options_user:
                try:
                    tmp1 = actor["id"].split("/")[1]
                    tmp2 = d["target"]["displayName"]
                except IndexError:
                    tmp1 = "actor:id"
                    tmp2 = "target:displayName"
                record.append(tmp1)
                record.append(tmp2)
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            return record
