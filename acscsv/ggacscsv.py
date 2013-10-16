#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv 
import json

class GgacsCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_user, options_rules, options_urls, options_provider,options_key_path):
        super(GgacsCSV, self).__init__(delim)
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_user = options_user
        self.options_provider = options_provider
        self.options_key_path = options_key_path

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
            if self.options_provider:
                prov = d["provider"]
                record.append(prov["displayName"])
                record.append(prov["link"])
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
            record.append(acscsv.gnipRemove)
            return record
