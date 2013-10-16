#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Jinsub Hong"
__license__="Simplified BSD"
import sys
import acscsv
import json

class StntvCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_user,options_struct,options_influence,options_key_path):
        super(StntvCSV, self).__init__(delim)
        self.options_user = options_user
        self.options_struct = options_struct
        self.options_influence = options_influence
        self.options_key_path = options_key_path

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
            #key_path
            if self.options_key_path:
                buildstring=''
                kp=self.options_key_path.split(":")
                for num in range(0,len(kp)):
                    try:
                        buildstring+='{0}'.format(str(kp[num]))
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
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record
