#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
from acscsv import *

class FsqacsCSV(AcsCSV):
    def __init__(self, delim, options_geo, options_user, options_rules, options_lang, options_influence):
        super(FsqacsCSV, self).__init__(delim)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_lang = options_lang
        # clean up options that don't pertain
        self.options_influence = options_influence

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
                record.append('-'.join([gnipRemove, mtype]))
                record.append(gnipDateTime)
                record.append(msg)
                return record
            if verb == "delete":
                record.append(self.cleanField(d["object"]["id"]))
                record.append(gnipDateTime)
                record.append('-'.join([gnipRemove, verb]))
                return record
            elif verb == "scrub_geo":
                record.append(self.cleanField(d["actor"]["id"]))
                record.append(gnipDateTime)
                record.append('-'.join([gnipRemove, verb]))
                return record
            # shorthand
            gnip = '[]'
            if "gnip" in d:
                gnip = d["gnip"]
            actor = d["actor"]
            obj = d["object"]
            cat_list = obj["foursquareCategories"]
            # default output: id|postedTime|UTCoffset|displayName|[categories]|[lat,lon]
            record.append(d["id"])
            record.append(d["postedTime"])
            record.append(self.cleanField(str(d["foursquareCheckinUtcOffset"])))
            record.append(self.cleanField(obj["displayName"]))
            if len(cat_list) > 0 and isinstance(cat_list[0],dict):
                cat_names = self.buildListString([cat["displayName"] for cat in cat_list])
            else:
                cat_names = str(["object:foursquareCategories_list-items:displayName"])
            record.append(cat_names)
            geo_coords = str([str(l) for l in obj["geo"]["coordinates"]])
            record.append(geo_coords)
            #
            if self.options_rules:
                rules = '[]'
                if "matching_rules" in gnip:
                    rules = self.buildListString([ "%s (%s)"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            if self.options_geo:
                # geo should add the contents of d[object][address]
                locality = "None"
                region = "None"
                postalCode = "None"
                country = "None"
                if "address" in obj:
                    if "locality" in obj["address"] and obj["address"]["locality"] is not None:
                        locality = obj["address"]["locality"]
                    if "region" in obj["address"] and obj["address"]["region"] is not None:
                        region = obj["address"]["region"]
                    if "postalCode" in obj["address"] and obj["address"]["postalCode"] is not None:
                        postalCode = obj["address"]["postalCode"]
                    if "country" in obj["address"] and obj["address"]["country"] is not None:
                        country = obj["address"]["country"]
                record.append(locality)
                record.append(region)
                record.append(country)
                record.append(postalCode)
            if self.options_user:
                record.append(self.cleanField(actor["gender"]))
            #
            self.cnt += 1
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(gnipError)
            record.append(gnipRemove)
            return record
