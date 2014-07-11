#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv

class FsqacsCSV(acscsv.AcsCSV):
    def __init__(self, delim, options_keypath, options_geo, options_user, options_rules):
        super(FsqacsCSV, self).__init__(delim,options_keypath)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules

    def procRecordToList(self, d):
        """Take a JSON Activity Streams payload as a Python dictionary. Check 
        activity for system information and compliance handling. If necessary, 
        return the system info or compliance message. Otherwise, if the activity 
        is valid, return list of fields as specified by the input flags.
        
        Flags::

            delim
            options_keypath
            options_geo
            options_user
            options_rules

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
                record.append('-'.join([acscsv.gnipRemove, mtype]))
                record.append(acscsv.gnipDateTime)
                record.append(msg)
                return record
            if verb == "delete":
                #record.append(self.cleanField(d["object"]["id"]))
                record.append(d["object"]["id"])
                record.append(acscsv.gnipDateTime)
                record.append('-'.join([acscsv.gnipRemove, verb]))
                return record
            elif verb == "scrub_geo":
                record.append(d["actor"]["id"])
                record.append(acscsv.gnipDateTime)
                record.append('-'.join([acscsv.gnipRemove, verb]))
                return record
            ## default fsq output: id|postedTime|UTCoffset|displayName|[categories]|[lat,lon]
            # consider a 3-field default output: id|postedTime|[lat,lon]
            # first test activity integrity
            try:        # should be in all AS activities
                act_id = d["id"]
                p_time = d["postedTime"]
                actor = d["actor"]
                obj = d["object"]
            except KeyError:
                sys.stderr.write("Standard Activity Streams fields missing - ")
                raise
            try:        # should be in all fsq acs
                #fsq_utc_offset = self.cleanField(d["foursquareCheckinUtcOffset"]) 
                fsq_utc_offset = d["foursquareCheckinUtcOffset"] 
                d_name = obj["displayName"]
                cat_list = obj["foursquareCategories"]
                # coords is an obj attribute so it can be used with the geojson methods
                self.geo_coords_list = obj["geo"]["coordinates"]
            except KeyError:
                sys.stderr.write("Standard pub-specific fields missing - ")
                raise
            geo_coords = str(self.geo_coords_list)
            # format fsq category list 
            if len(cat_list) > 0 and isinstance(cat_list[0],dict):
                cat_names = self.buildListString([cat["displayName"] for cat in cat_list])
            else:
                cat_names = "['None']"
            record.append(act_id)
            record.append(p_time)
            record.append(fsq_utc_offset)
            record.append(d_name)
            record.append(cat_names)
            record.append(geo_coords)
            #
            gnip = '[]'             # shorthand
            if "gnip" in d:         # only relevant for PT streams
                gnip = d["gnip"]
            if self.options_rules:
                rules = '[]'
                if "matching_rules" in gnip:
                    rules = self.buildListString([ "%s (%s)"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            if self.options_geo:    # add contents of d[object][address]
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
                try:
                    #record.append(self.cleanField(actor["gender"]))
                    record.append(actor["gender"])
                except KeyError:
                    sys.stderr.write("Standard pub-specific fields missing - ")
                    raise
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record
