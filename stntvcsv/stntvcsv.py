#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Jinsub Hong"
__license__="Simplified BSD"
import datetime
import sys

gnipError = "GNIPERROR"
gnipRemove = "GNIPREMOVE"
gnipDateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

class StntvCSV(object):
    def __init__(self, delim, options_user,options_struct,options_influence):
        self.delim = delim
        self.cnt = 0
        self.options_user = options_user
        self.options_struct = options_struct
        self.options_influence = options_influence

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

    def asString(self,l):
        if l is None:
            return None
        return self.delim.join(l)

    def procRecord(self,x):
        return self.asString(self.procRecordToList(x))

    def procRecordToList(self, d):
        record = []
        try:
            user = d["user"]
            record.append(str(d["id"]))
            record.append(d["created_at"])
            body = "None"
            if "body" in d:
                # post type
                body = self.cleanField(d["body"])
            record.append(body)
            #
            if self.options_struct:
                in_reply_to = "None"
                parent_message = "None"
                replies = "None"
                if "conversation" in d:
                    con = d["conversation"]
                    if "in_reply_to_message_id" in con:
                        in_reply_to = str(con["in_reply_to_message_id"])
                    if "parent_message_id" in con:
                        parent_message = str(con["parent_message_id"])
                    if "replies" in con:
                        replies = str(con["replies"])
                record.append(parent_message)
                record.append(in_reply_to)
                record.append(replies)
            #
            if self.options_user:
                website_url = "None"
                record.append(self.cleanField(user["username"]))
                record.append(self.cleanField(user["name"]))
                if user["website_url"] != None:
                    website_url = user["website_url"]
                record.append(website_url)
            #
            if self.options_influence:
                following_stocks = str(user["following_stocks"])
                followers = str(user["followers"])
                experience = str(user["trading_strategy"]["experience"])
                record.append(following_stocks)
                record.append(followers)
                record.append(experience)

            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(gnipError)
            record.append(gnipRemove)
            return record
