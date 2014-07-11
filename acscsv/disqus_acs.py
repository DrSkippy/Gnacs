#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv
class DiacsCSV(acscsv.AcsCSV):
    """
    DiacsCSV determins the parse order and included fields when parsing Disqus Activity Streams
    JSON records to CSV fields.
    """
    def __init__(self, delim, options_keypath, options_user, options_rules, options_lang, options_struct, options_status):
        super(DiacsCSV, self).__init__(delim,options_keypath)
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_lang = options_lang
        self.options_struct = options_struct
        self.options_status = options_status

    def procRecordToList(self, d):
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
            options_status

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
                record.append(acscsv.gnipRemove)
                record.append(verb)
                #record.append(self.cleanField(d["object"]["id"]))
                record.append(d["object"]["id"])
                return record
            #
            record.append(d["id"])
            record.append(d["postedTime"])
            #record.append(self.cleanField(d["body"]))
            record.append(d["body"])
            #
            gnip = d["gnip"]
            actor = d["actor"]
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
                target = d["target"]
                # site
                tmp = self.splitId(target["website"]["id"])
                record.append(tmp)
                # thread
                tmp2 = self.splitId(target["id"])
                record.append(tmp2)
                # thread link
                if "link" in target and target["link"] is not None:
                    record.append(target["link"])
                else:
                    record.append("None")
                # in reply to
                if "inReplyTo" in d:
                    in_reply_to = d["inReplyTo"]
                    # comment
                    tmp2 = self.splitId(in_reply_to["id"])
                    record.append(tmp2)
                    # reply to user
                    tmp3 = self.splitId(in_reply_to["author"]["id"])
                    if tmp3 == "-1":
                        tmp3 = "Anon"
                    record.append(tmp3)
                else:
                    record.append("None")
                    record.append("None")
            if self.options_user:
                tmp = self.splitId(actor["id"])
                if tmp == "-1":
                    tmp = "Anon"
                record.append(tmp)
            if self.options_status:
                record.append(verb)
                if "disqusType" in d:
                    record.append(str(d["disqusType"]))
                else:
                    record.append("None")
                if "disqusTypePrev" in d:
                    record.append(str(d["disqusTypePrev"]))
                else:
                    record.append("None")
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            return record

