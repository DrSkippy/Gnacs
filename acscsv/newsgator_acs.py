#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv

class NGacsCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_keypath, options_urls, options_user):
        super(NGacsCSV, self).__init__(delim,options_keypath)
        self.options_urls = options_urls
        self.options_user = options_user

    def procRecordToList(self, d):
        record = []
        try:
            if "verb" in d:
                verb = d["verb"]
            else:
                msg = "Unidentified meta message"
                # these apply?
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
            obj = d["object"]
            if "content" in obj:
                #record.append(self.cleanField(obj["content"]))
                record.append(obj["content"])
            else:
                record.append("None")
            #
            if self.options_urls:
                url = "None"
                if "link" in d:
                    url = d["link"]
                record.append(url)
                feed = "None"
                if "ngFeedXmlUrl" in d:
                    feed = d["ngFeedXmlUrl"]
                record.append(feed)
            #
            if self.options_user:
                user_name = "None"
                actor = d["actor"]
                if actor is not None and "displayName" in actor:
                    user_name = actor["displayName"]
                record.append(user_name)
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            return record

