#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Jeff Kolb, Josh Montague"
__license__="Simplified BSD"

import sys
import acscsv

class StacsCSV(acscsv.AcsCSV):
    """Normalized stocktwits activities"""
    def __init__(self, delim, options_user, options_struct, options_influence, options_keypath):
        super(StacsCSV, self).__init__(delim, options_keypath)
        self.options_user = options_user
        self.options_struct = options_struct
        self.options_influence = options_influence

    def procRecordToList(self, d):
        """Creates the field list according to options selected."""
        record = []
        try:
            record.append(d['object']['id'])
            record.append(d['object']['postedTime'])
            record.append(self.cleanField(d['object']['summary']))
            actor = d['actor']
            if self.options_user:
                website_url = 'None'
                record.append(self.cleanField(actor['preferredUsername']))
                record.append(self.cleanField(actor['displayName']))
                if actor['link'] != None:
                    website_url = actor['link']
                record.append(website_url)
            #
            if self.options_influence:
                following_stocks = str(actor['followingStocksCount'])
                followers = str(actor['followingCount'])
                experience = str(actor['tradingStrategy']['experience'])
                record.append(following_stocks)
                record.append(followers)
                record.append(experience)
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
            return record
        except KeyError, e:
            sys.stderr.write("Field missing from record ({}), skipping. Error={}\n".format(self.cnt, e))
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record
