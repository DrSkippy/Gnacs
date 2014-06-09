# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import acscsv

class TwacsCSV(acscsv.AcsCSV):
    """Subset of Twitter fields with specified delimiter.  Please see help for options"""

    def __init__(self, delim, options_keypath, options_geo, options_user, options_rules, options_urls, options_lang, options_influence, options_struct):
        super(TwacsCSV, self).__init__(delim,options_keypath)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_lang = options_lang
        self.options_influence = options_influence
        self.options_struct = options_struct
        
    def procRecordToList(self,d):
        """Builds the list of output fields in determined order according to input options"""
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
                record.append(d["object"]["id"])
                record.append(acscsv.gnipDateTime)
                record.append('-'.join([acscsv.gnipRemove, verb]))
                return record
            elif verb == "scrub_geo":
                record.append(d["actor"]["id"])
                record.append(acscsv.gnipDateTime)
                record.append('-'.join([acscsv.gnipRemove, verb]))
                return record
            # always first 2 items
            record.append(d["id"])
            record.append(d["postedTime"])
            # add some handling so calling gnacs without a pub is still useful
            #   n.b.: -stocktwits is native, so no 'verb' to get here
            #         -put more-specific fields at the beginning to catch them 
            obj = d["object"]
            if d["id"].rfind("getglue") != -1 : # getglue 
                record.append(verb)     # 'body' is inconsistent in gg
            elif "foursquareCategories" in obj or "foursquareCheckinOffset" in obj:      # fsq
                record.append(str(obj["geo"]["coordinates"]))
            elif "wpBlogId" in obj:     # wp
                record.append(str(obj["wpBlogId"]))
            elif "tumblrType" in obj:   # tumblr
                record.append(obj["tumblrType"])
            elif "body" in d:           # tw, disqus, stocktw,  
                record.append(self.cleanField(d["body"]))       
            elif "link" in d:           # ng
                record.append(d["link"])
            else:                       # ? 
                record.append("None")
            #
            gnip = {}
            actor = {}
            if "gnip" in d:
                gnip = d["gnip"]
            if "actor" in d:    # no 'actor' in ng
                actor = d["actor"]
            #
            if self.options_urls:
                urls = "None"
                if "urls" in gnip:
                    urls = self.buildListString([ l["expanded_url"] for l in gnip["urls"]])
                record.append(urls)
                twitter_urls = "None"
                twitter_un_urls = "None"
                if "twitter_entities" in d:
                    if "urls" in d["twitter_entities"]:
                        if len(d["twitter_entities"]["urls"]) > 0:
                            tmp_url_list = []
                            tmp_un_url_list = []
                            for tmp_rec in d["twitter_entities"]["urls"]:
                                try:
                                    if "url" in tmp_rec and tmp_rec["url"] is not None:
                                        tmp_url_list.append(tmp_rec["url"])
                                    else:
                                        tmp_url_list.append("None")
                                except TypeError:
                                    tmp_url_list = ["twitter_entiteis:urls:url"]
                                try:
                                    if "expanded_url" in tmp_rec and tmp_rec["expanded_url"] is not None:
                                        tmp_un_url_list.append(tmp_rec["expanded_url"])
                                    else:
                                        tmp_un_url_list.append("None")
                                except TypeError:
                                    tmp_un_urls_list = ["twitter_entities:urls:expanded_url"]
                            twitter_urls = self.buildListString(tmp_url_list)
                            twitter_un_urls = self.buildListString(tmp_un_url_list)
                record.append(twitter_urls)
                record.append(twitter_un_urls)
            if self.options_lang:
                try:
                    record.append(str([str(l) for l in actor["languages"]]))
                except UnicodeEncodeError, e:
                    record.append(str("bad encoding"))
                glang = "None"
                if "language" in gnip:
                    glang = gnip["language"]["value"]
                record.append(glang)
                tlang = "None"
                if "twitter_lang" in d:
                    tlang = d["twitter_lang"]
                record.append(tlang)
            if self.options_rules:
                rules = '[]'
                if "matching_rules" in gnip:
                    rules = self.buildListString([ "%s (%s)"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
                record.append(rules)
            if self.options_geo:
                geoType = "None"
                self.geoCoordsList = None
                geoCoords = "None"
                if "geo" in d:
                    if "type" in d["geo"]:
                        geoType = d["geo"]["type"]
                        #self.geoCoords = [str(l) for l in d["geo"]["coordinates"]]
                        self.geoCoordsList = d["geo"]["coordinates"]
                        geoCoords = str(self.geoCoordsList)
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
                # gnip:profileLocations
                pl_otype = "None"
                pl_name = "None"
                # profileLocations:address
                pl_country = "None"
                pl_region = "None"
                pl_countrycode = "None"
                pl_locality = "None"
                # profileLocations:geo
                pl_gtype = "None"
                pl_coords = "None"
                if "profileLocations" in gnip:
                    # n.b. profileLocations is a list, suggests it might include >1 thing eventually
                    pl = gnip["profileLocations"][0]
                    if "objectType" in pl:
                        pl_otype = pl["objectType"]
                    if "displayName" in pl:
                        pl_name = pl["displayName"]
                    if "address" in pl:
                        adrs = pl["address"]
                        if "country" in adrs:
                            pl_country = adrs["country"]
                        if "region" in adrs:
                            pl_region = adrs["region"]
                        if "countryCode" in adrs:
                            pl_countrycode = adrs["countryCode"]
                        if "locality" in adrs:
                            pl_locality = adrs["locality"]
                    if "geo" in pl:
                        geo = pl["geo"]
                        if "type" in geo:
                            pl_gtype = geo["type"]
                        if "coordinates" in geo:
                            pl_coords = str(geo["coordinates"])
                record.append(pl_name)
                record.append(pl_otype)
                record.append(pl_country)
                record.append(pl_region)
                record.append(pl_countrycode)
                record.append(pl_locality)
                record.append(pl_gtype)
                record.append(pl_coords)
                #
            if self.options_user:
                record.append(self.cleanField(actor["displayName"]))
                record.append(self.cleanField(actor["preferredUsername"]))
                try:
                    tmp = actor["id"].split(":")[2] #Brian's 1st attempt at Gnacsification
                except IndexError:
                    tmp = "actor:id"                    
                record.append(tmp)
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
            if self.options_struct:
                oid = "None"
                opt = "None"
                overb = "None"
                inReplyTo = "None"
                if "inReplyTo" in d:
                    inReplyTo = d["inReplyTo"]["link"]
                if "object" in d:
                    obj = d["object"]
                    if "objectType" in obj:
                        overb = obj["objectType"]
                if verb == "share" and overb == "activity":
                    record.append("Retweet")
                    if "id" in obj:
                        oid = obj["id"]
                    if "postedTime" in obj:
                        opt = obj["postedTime"]
                elif inReplyTo == "None":
                    record.append("Tweet")
                else:
                    record.append("Reply")
                record.append(inReplyTo)
                record.append(oid)
                record.append(opt)
            #
            return record
        except KeyError:
            #sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record
