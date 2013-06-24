#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv

class TwacsCSV(acscsv.acscsv.AcsCSV):
    def __init__(self, delim, options_geo, options_user, options_rules, options_urls, options_lang, options_influence):
        super(TwacsCSV, self).__init__(delim)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_lang = options_lang
        self.options_influence = options_influence

    def procRecordToList(self,d):
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
                record.append(d["object"]["id"])
                record.append(gnipDateTime)
                record.append('-'.join([gnipRemove, verb]))
                return record
            elif verb == "scrub_geo":
                record.append(d["actor"]["id"])
                record.append(gnipDateTime)
                record.append('-'.join([gnipRemove, verb]))
                return record
            # always first 3 items
            record.append(d["id"])
            record.append(d["postedTime"])
            record.append(self.cleanField(d["body"]))
            #
            gnip = d["gnip"]
            actor = d["actor"]
            if self.options_urls:
                urls = "None"
                if "urls" in gnip:
                    urls = self.buildListString([ l["expanded_url"] for l in gnip["urls"]])
                record.append(urls)
                twitter_urls = "None"
                twitter_un_urls = "None"
                if "twitter_entities" in d:
                    if "urls" in d["twitter_entities"]:
                        if len(d["twitter_entities"]["urls"]) > 0 and "url" in d["twitter_entities"]["urls"]:
                            twitter_urls = self.buildListString([   l["url"]          for l in d["twitter_entities"]["urls"] if "url"          in l])
                            twitter_un_urls = self.buildListString([l["expanded_url"] for l in d["twitter_entities"]["urls"] if "expanded_url" in l])
                record.append(twitter_urls)
                record.append(twitter_un_urls)
            if self.options_lang:
                record.append(str([str(l) for l in actor["languages"]]))
                glang = "None"
                if "language" in gnip:
                    glang = gnip["language"]["value"]
                record.append(glang)
            if self.options_rules:
                rules = '[]'
                if "matching_rules" in gnip:
                    rules = self.buildListString([ "%s (%s)"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            if self.options_geo:
                geoType = "None"
                geoCoords = "None"
                if "geo" in d:
                    if "type" in d["geo"]:
                        geoType = d["geo"]["type"]
                        geoCoords = str([str(l) for l in d["geo"]["coordinates"]])
                record.append(geoCoords)
                record.append(geoType)
                locType = "None"
                locCoords = "None"
                locName = "None"
                locCountry = "None"
                if "location" in d:
                    locName = self.cleanField(d["location"]["displayName"])
                    locCountry = self.cleanField(d["location"]["twitter_country_code"])
                    if "geo" in d["location"] and d["location"]["geo"] is not None:
                        if "type" in d["location"]["geo"]:
                            locType = d["location"]["geo"]["type"]
                            locCoords = str([str(l) for l in d["location"]["geo"]["coordinates"][0]])
                record.append(locCoords)
                record.append(locType)
                record.append(locName)
                record.append(locCountry)
                record.append(str(actor["utcOffset"]))
                dName = "None"
                if "location" in actor and "displayName" in actor["location"]:
                    dName = self.cleanField(actor["location"]["displayName"])
                record.append(dName)
            if self.options_user:
                record.append(self.cleanField(actor["displayName"]))
                record.append(self.cleanField(actor["preferredUsername"]))
            if self.options_influence:
                klout = "None"
                followers = "None"
                friends = "None"
                listed = "None"
                statuses = "None"
                if "klout_score" in gnip:
                    klout = str(gnip["klout_score"])
                followers = str(actor["followersCount"])
                friends = str(actor["friendsCount"])
                listed = str(actor["listedCount"])
                statuses = str(actor["statusesCount"])
                record.append(klout)
                record.append(followers)
                record.append(friends)
                record.append(listed)
                record.append(statuses)
            #
            return record
        except KeyError:
            sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(gnipError)
            record.append(gnipRemove)
            return record
