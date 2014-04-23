# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague"
__license__="Simplified BSD"
import sys
import acscsv
import inspect

# move to acscsv?

class _field(object):
    """
    Base class for finding the appropriate key-value pairs in a JSON Activity Streams payload.
    Common default value (for e.g. missing values) is "None", but child subclasses can override
    this default when needed. Subclasses should also define the keypath to the desired location
    by overwriting the "path" list. 
    """
    default_value = "None"
    value = None
    path = []

    def __init__(self, json_record):
        self.value = self.walk_path(json_record)

    def __repr__(self):
        return self.value

    def walk_path(self, json_record):
        res = json_record
        for k in self.path:
            if k not in json_record:
                return self.default_value
            res = res[k]
        return res

#### parsing and formating objects 
# 2014-04-22, JM
#   -- working through them top --> bottom of original twacscsv.py

class field_verb(_field):
    """assign to self.value the value of top-level 'verb' key"""
    # specify path to desired field as a list of dict keys 
    path = ["verb"]
    # if needed, overwrite default_value
    default_value = "Unidentified meta message"
    
    def __init__(self, json_record):
        """Calls base constructor, which walks the specified dict path to find appropriate value"""
        super(
                field_verb
                , self).__init__(json_record)
        # in any field_* class, add any needed custom parsing here


class field_gnip_urls(_field):
    """assign to self.value the list of 'expanded_url' values within 'gnip', 'urls'"""
    # nb: there exists a t.co url
    path = ["gnip", "urls"]
    
    def __init__(self, json_record):
        super(
            field_gnip_urls
            , self).__init__(json_record)
        # after base __init__(), self.value is a list of url & expanded url dicts.
        # call buildListString within the Twacs class, not here. just return the list.
        self.value = [ x["expanded_url"] for x in self.value ] ]


class _field_twitter_urls(_field):
    """base class for accessing multiple url fields within 'twitter_entities', 'urls'"""
    # nb: there are 3x urls in twitter_entities 
    path = ["twitter_entities", "urls"]
    
    def __init__(self, json_record, key=None):
        super(
            _field_twitter_urls
            , self).__init__(json_record)
        # after base __init__(), self.value is a list. can be empty or list of dicts 
        if key is not None and isinstance(self.value, list) and len(self.value) > 0:
            for d in self.value:
                try:
                    # JM: previous TypeError exception in case d isn't a dict? 
                    if key in d["urls"] and d["urls"][key] is not None: 
                        url_list.append( d["urls"][key] )
                    else:
                        url_list.append( self.default_value ) 
                except TypeError:
                    url_list = [ self.default_value ]
            self.value = url_list
        else:
            self.value = [ self.default_value ]


class field_twitter_urls_url(_field_twitter_urls):
    """assign to self.value the list of 'url' values within 'twitter_entities', 'urls' dict"""
    
    def __init__(self, json_record):
        super(
            field_twitter_urls_url
            , self).__init__(json_record, key="url")


class field_twitter_expanded_urls(_field_twitter_urls):
    """assign to self.value the list of 'expanded_url' values within 'twitter_entities', 'urls' dict"""

    def __init__(self, json_record):
        super(
            field_twitter_expanded_urls
            , self).__init__(json_record, key="expanded_url")


class field_twitter_display_urls(_field):
    """assign to self.value the list of 'display_url' values within 'twitter_entities', 'urls' dict"""

    def __init__(self, json_record):
        super(
            field_twitter_expanded_urls
            , self).__init__(json_record, key="display_url")


class field_actor_lang(_field):
    """assign to self.value the value of 'actor', 'languages'"""
    path = ["actor", "languages"]
    
    def __init__(self, json_record):
        super(
            field_actor_lang
            , self).__init__(json_record)
        # self.value is now a list


class field_gnip_language(_field):
    path = ["gnip","language","value"]
    
    def __init__(self, json_record):
        super(
                field_gnip_language
                , self).__init__(json_record)


class field_twitter_lang(_field):
    """assign to self.value the value of top-level 'twitter_lang'"""
    path = ["twitter_lang"]
    
    def __init__(self, json_record):
        super(
            field_twitter_lang
            , self).__init__(json_record)
        # JM, does twitter_lang ever have > 1 value?

#################
# WIP
################



#   
class Twacs(acscsv.AcsCSV):
    def __init__(self
            , delim
            , options_keypath
            , options_geo
            , options_user
            , options_rules
            , options_urls
            , options_lang
            , options_influence
            , options_struct):
        super(Twacs, self).__init__(delim,options_keypath)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_lang = options_lang
        self.options_influence = options_influence
        self.options_struct = options_struct
        
    def procRecordToList(self, d):
        """
        Reads JSON payload d, identify the activity type by its verb, 
        return the appropriate parsed + delimited line.
        """ 
        record = []
        try:        # try block needs a KeyError exception?
            #if "verb" in d:
            #    verb = d["verb"]
            verb = field_verb(d).value
            # check for compliance
            if verb is None:
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
        # at this point, it's a valid, non-compliance activity
        return self.csv(d, record)

    # refactor to use objects
    def csv(self, d, record)
        try:                            # KeyError exception at EOF
            # always first 2 items 
            record.append(d["id"])
            record.append(d["postedTime"])
            # add some handling so calling gnacs without a pub is still useful
            #   -put more-specific fields at the beginning to catch them 
            #   -stocktwits is native, so no 'verb' to get here
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
#            gnip = {}
#            actor = {}
#            if "gnip" in d:
#                gnip = d["gnip"]
#            if "actor" in d:    # no 'actor' in ng
#                actor = d["actor"]
            #
            # JM: breaking this section out into separate classes, 
            #       but the if self.options flag will combine them all (consistent 
            #       current implementation
            if self.options_urls:
                ## new code, JM
                record.append( self.buildListString( field_gnip_urls(d).value ) ) 
                record.append( self.buildListString( field_twitter_urls_url(d).value ) ) 
                record.append( self.buildListString( field_twitter_urls_expanded_url(d).value ) ) 
                record.append( self.buildListString( field_twitter_urls_display_url(d).value ) ) 
                ##
#                urls = "None"
#                if "urls" in gnip:
#                    urls = self.buildListString([ l["expanded_url"] for l in gnip["urls"]])
#                record.append(urls)
#                twitter_urls = "None"
#                twitter_un_urls = "None"
#                if "twitter_entities" in d:
#                    if "urls" in d["twitter_entities"]:
#                        if len(d["twitter_entities"]["urls"]) > 0:
#                            tmp_url_list = []
#                            tmp_un_url_list = []
#                            for tmp_rec in d["twitter_entities"]["urls"]:
#                                try:
#                                    if "url" in tmp_rec and tmp_rec["url"] is not None:
#                                        tmp_url_list.append(tmp_rec["url"])
#                                    else:
#                                        tmp_url_list.append("None")
#                                except TypeError:
#                                    tmp_url_list = ["twitter_entiteis:urls:url"]
#                                try:
#                                    if "expanded_url" in tmp_rec and tmp_rec["expanded_url"] is not None:
#                                        tmp_un_url_list.append(tmp_rec["expanded_url"])
#                                    else:
#                                        tmp_un_url_list.append("None")
#                                except TypeError:
#                                    tmp_un_urls_list = ["twitter_entities:urls:expanded_url"]
#                            twitter_urls = self.buildListString(tmp_url_list)
#                            twitter_un_urls = self.buildListString(tmp_un_url_list)
#                record.append(twitter_urls)
#                record.append(twitter_un_urls)
            if self.options_lang:
                ## new code, JM
                # actor lang
                try: 
                    record.append( self.buildListString( field_actor_lang(d).value ) ) 
                except UnicodeEncodeError, e:
                    record.append("bad-encoding")
                # gnip lang
                record.append(field_gnip_language(d).value)
                # twitter lang
                 
########################################
# WIP here, JM
########################################

                ##
#                try:
#                    record.append(str([str(l) for l in actor["languages"]]))
#                except UnicodeEncodeError, e:
#                    record.append(str("bad encoding"))
                #glang = "None"
                #if "language" in gnip:
                #    glang = gnip["language"]["value"]
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

    def db_output(self, d):
        """Explicitly specific the order and fields that get output to specific files."""
        return [
                field_gnip_language(d).value, 
                ]
