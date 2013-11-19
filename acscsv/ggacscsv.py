#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv 

class GgacsCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_keypath, options_user, options_rules, options_urls, options_origin):
        super(GgacsCSV, self).__init__(delim,options_keypath)
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_user = options_user
        self.options_origin = options_origin

    def procRecordToList(self, d):
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
                record.append('-'.join([acscsv.gnipRemove, mtype]))
                record.append(acscsv.gnipDateTime)
                record.append(msg)
                return record
            actor = d["actor"]
            obj = d["object"]
            #
            record.append(d["id"])
            record.append(d["postedTime"])
            record.append(d["updatedTime"])
            record.append(verb)
            #
            record.append(obj["id"])
            record.append(obj["objectType"])
            record.append(self.cleanField(d["displayName"]))
            #
            if "target" in d:
                target = d["target"]
                record.append(target["id"])
                record.append(target["objectType"])
                record.append(self.cleanField(target["displayName"]))
            else:
                record.append("None")
                record.append("None")
                record.append("None")
            #
            body = "None"
            if "body" in d:
                # post type
                body = self.cleanField(d["body"])
            record.append(body)
            #
            reply = "None"
            if "inReplyTo" in d:
                reply = d["inReplyTo"]["link"]
            record.append(reply)
            #
            if self.options_rules:
                rules = "[]"
                if "gnip" in d:
                    gnip = d["gnip"]
                    if "matching_rules" in gnip:
                        rules = self.buildListString(
                            [ "%s (%s)"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            #
            if self.options_user:
                record.append(actor["id"])
                record.append(self.cleanField(actor["preferredUsername"]))
                record.append(self.cleanField(actor["displayName"]))
                record.append(actor["objectType"])
            #
            if self.options_urls:
                record.append(d["link"])
            #
            if self.options_origin:
                prov = d["provider"] 
                record.append(prov["displayName"])
                record.append(prov["link"])
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record
