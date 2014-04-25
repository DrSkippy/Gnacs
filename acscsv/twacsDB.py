# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague, Fiona Pigot"
__license__="Simplified BSD"

import sys
import acscsv
import inspect
import datetime

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
            #if k not in json_record:
            if k not in res:
                return self.default_value
            res = res[k]
        return res


# TODO:
# - convert all class docstrings to consistently use the key1.key2.key3 syntax 


# notes 
#
# - on class naming conventions...
# the path to a particular key-value pair may be quite long. as long as there arent collisions, 
# ive chosen to use the following convention: field_<top level key>_<final_key>(...) . 
# in this way, the user can get a sense of the beginning and end of the path to the field of 
# interest. when it helps clarify, additional keys or abbreviations can also be added. 
# where possible, avoid mixing camelCase and underscore_case by collapsing camelCase 
# keys into lowercase e.g. camelcase. (JM)
#
# - on self.value types...
# in order to do the final list join, all classes must end with self.value as either a string 
# or a list (which will be converted to a string using acscsv.listBuildString() within the 
# csv() method (JM)
#
#
 
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


class field_id(_field):
    """assign to self.value the value in id"""
    path = ["id"]
    
    def __init__(self, json_record):
        super(
            field_id
            , self).__init__(json_record)
        # self.value starts with tag:search.twitter.....
        self.value = self.value.split(":")[2]


class field_postedtime(_field):
    """assign to self.value the value in postedTime"""
    path = ["postedTime"]
    
    def __init__(self, json_record):
        super(
            field_postedtime
            , self).__init__(json_record)


class field_body(_field):
    """assign to self.value the value in top-level body"""
    path = ["body"]
    
    def __init__(self, json_record):
        super(
            field_body
            , self).__init__(json_record)


class field_link(_field):
    """assign to self.value the value in top-level link"""
    path = ["link"]
    
    def __init__(self, json_record):
        super(
            field_link
            , self).__init__(json_record)


class field_generator_displayname(_field):
    """assign to self.value the value in generator.displayName"""
    path = ["generator", "displayName"]
    
    def __init__(self, json_record):
        super(
            field_generator_displayname
            , self).__init__(json_record)





########
# urls
class field_gnip_urls(_field):
    """assign to self.value the list of 'expanded_url' values within 'gnip', 'urls'"""
    # nb: there exists a t.co url
    path = ["gnip", "urls"]
    
    def __init__(self, json_record):
        super(
            field_gnip_urls
            , self).__init__(json_record)
        # self.value is (possibly) a list of url & expanded url dicts
        if self.value != self.default_value:
            #self.value = [ x["expanded_url"] for x in self.value ] 
            self.value = str( [ x["expanded_url"] for x in self.value ] ) 


class _field_twitter_urls(_field):
    """base class for accessing multiple url fields within 'twitter_entities', 'urls'"""
    # nb: there are 3x urls in twitter_entities 
    path = ["twitter_entities", "urls"]
    
    def __init__(self, json_record, key):
        super(
            _field_twitter_urls
            , self).__init__(json_record)
        # self.value is a list. can be empty or list of dicts 
        if key is not None and isinstance(self.value, list) and len(self.value) > 0:
            for d in self.value:
                try:
                    # previous TypeError exception in case d isn't a dict? (JM) 
                    if key in d["urls"] and d["urls"][key] is not None: 
                        url_list.append( d["urls"][key] )
                    else:
                        url_list.append( self.default_value ) 
                except TypeError:
                    url_list = [ self.default_value ]
            #self.value = url_list
            self.value = str( url_list )
        else:
            self.value = str( [ self.default_value ] )


class field_twitter_urls_url(_field_twitter_urls):
    """
    assign to self.value the list of 'url' values within 'twitter_entities', 'urls' dict.
    Inherits from _filed_twitter_urls class.
    """
    
    def __init__(self, json_record):
        super(
            field_twitter_urls_url
            , self).__init__(json_record, "url")


class field_twitter_urls_expanded_url(_field_twitter_urls):
    """assign to self.value the list of 'expanded_url' values within 'twitter_entities', 
    'urls' dict. Inherits from _filed_twitter_urls class.
    """

    def __init__(self, json_record):
        super(
            field_twitter_urls_expanded_url
            , self).__init__(json_record, "expanded_url")


class field_twitter_urls_display_url(_field_twitter_urls):
    """assign to self.value the list of 'display_url' values within 'twitter_entities', 
    'urls' dict. Inherits from _filed_twitter_urls class.
    """

    def __init__(self, json_record):
        super(
            field_twitter_urls_display_url
            , self).__init__(json_record, "display_url")


class field_twitter_hashtags_text(_field):
    """assign to self.value the value of twitter_entities.hashtags.text"""
    path = ["twitter_entities", "hashtags"]

    def __init__(self, json_record):
        super(
            field_twitter_hashtags_text
            , self).__init__(json_record)
        # self.value is possibly a list of dicts for each activity hashtag
        if self.value != self.default_value:
            self.value = [ x["text"] for x in self.value ] 
        self.value = str( self.value )


########
# langs 
class field_actor_lang(_field):
    """assign to self.value the value of 'actor', 'languages'"""
    path = ["actor", "languages"]
    
    def __init__(self, json_record):
        super(
            field_actor_lang
            , self).__init__(json_record)
        # self.value is a list, but have only ever seen with one value, so take that one. 
        # can simply use str( self.value ) if more than one appear someday
        self.value = self.value[0]


class field_gnip_lang(_field):
    path = ["gnip","language","value"]
    
    def __init__(self, json_record):
        super(
            field_gnip_lang
            , self).__init__(json_record)


class field_twitter_lang(_field):
    """assign to self.value the value of top-level 'twitter_lang'"""
    path = ["twitter_lang"]
    
    def __init__(self, json_record):
        super(
            field_twitter_lang
            , self).__init__(json_record)


########
# rules 
class field_gnip_rules(_field):
    """assign to self.value the value of 'gnip', 'matching_rules'"""
    path = ["gnip", "matching_rules"]
    
    def __init__(self, json_record):
        super(
            field_gnip_rules
            , self).__init__(json_record)
        # if matching_rules exists, self.value is a list of dicts 
        #   to be consistent with old code, want a list of [rule (tag), ... ]
        if self.value != self.default_value:
            self.value = [ "{} ({})".format( d["value"], d["tag"] ) for d in self.value ]
        else:
            self.value = [ self.default_value ]
        self.value = str( self.value )


########
# geo
class field_geo_type(_field):
    """
    Assign to self.value the value of geo.type . this is the type of user-enabled 
    tweet geotag."""
    path = ["geo", "type"]
    
    def __init__(self, json_record):
        super(
            field_geo_type
            , self).__init__(json_record)


class field_geo_coords(_field):
    """
    Assign to self.value the value of geo.coordinates . this is the coordinate pair 
    of the user-enabled tweet geotag.
    """
    path = ["geo", "coordinates"]
    
    def __init__(self, json_record):
        super(
            field_geo_coords
            , self).__init__(json_record)
        self.value = str( self.value )


class field_location_coords(_field):
    """assign to self.value the value of location.geo.coordinates ."""
    path = ["location", "geo", "coordinates"]
    
    def __init__(self, json_record):
        super(
            field_location_coords
            , self).__init__(json_record)
        # self.value is a list of lists of floats 
        if self.value != self.default_value: 
            self.value = str( self.value[0] )
        # twitter coords are [ lat, lon ]
    

class field_location_type(_field):
    """assign to self.value the value of location.geo.type ."""
    path = ["location", "geo", "type"]
    
    def __init__(self, json_record):
        super(
            field_location_type
            , self).__init__(json_record)


class field_location_displayname(_field):
    """assign to self.value the value of 'location', 'displayName' """
    path = ["location", "displayName"]
    
    def __init__(self, json_record):
        super(
            field_location_displayname
            , self).__init__(json_record)


class field_location_twittercountry(_field):
    """assign to self.value the value of 'location', 'twitter_country_code' """
    path = ["location", "twitter_country_code"]
    
    def __init__(self, json_record):
        super(
            field_location_twittercountry
            , self).__init__(json_record)


class field_actor_utcoffset(_field):
    """assign to self.value the value of 'actor' 'utcOffset' """
    path = ["actor", "utcOffset"]
    
    def __init__(self, json_record):
        super(
            field_actor_utcoffset
            , self).__init__(json_record)
        # self.value is a signed integer 
        self.value = str( self.value )


class field_actor_loc_displayname(_field):
    """assign to self.value the value of actor.location.displayName"""
    path = ["actor", "location", "displayName"]
    
    def __init__(self, json_record):
        super(
            field_actor_loc_displayname
            , self).__init__(json_record)


class field_gnip_pl_displayname(_field):
    """
    Assign to self.value the value of gnip.profileLocation.displayName . Currently only 
    supports one list item, but could add support more in the future.
    """
    path = ["gnip", "profileLocations", "displayName"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_displayname
            , self).__init__(json_record)
 
class field_gnip_pl_objecttype(_field):
    """Assign to self.value the value of gnip.profileLocations.objectType"""
    path = ["gnip", "profileLocations", "objectType"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_objecttype
            , self).__init__(json_record)


class field_gnip_pl_country(_field):
    """Assign to self.value the value of gnip.profileLocations.address.country"""
    path = ["gnip", "profileLocations", "address", "country"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_country
            , self).__init__(json_record)


class field_gnip_pl_region(_field):
    """Assign to self.value the value of gnip.profileLocations.address.region"""
    path = ["gnip", "profileLocations", "address", "region"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_region
            , self).__init__(json_record)


class field_gnip_pl_countrycode(_field):
    """Assign to self.value the value of gnip.profileLocations.address.countryCode"""
    path = ["gnip", "profileLocations", "address", "countryCode"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_countrycode
            , self).__init__(json_record)


class field_gnip_pl_locality(_field):
    """Assign to self.value the value of gnip.profileLocations.address.locality"""
    path = ["gnip", "profileLocations", "address", "locality"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_locality
            , self).__init__(json_record)


class field_gnip_pl_geo_type(_field):
    """Assign to self.value the value of gnip.profileLocations.geo.type"""
    path = ["gnip", "profileLocations", "geo", "type"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_geo_type
            , self).__init__(json_record)


class field_gnip_pl_geo_coords(_field):
    """Assign to self.value the value of gnip.profileLocations.geo.coordinates"""
    path = ["gnip", "profileLocations", "geo", "coordinates"]
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_geo_coords
            , self).__init__(json_record)


########
# actor 
class field_actor_displayname(_field):
    """Assign to self.value the value of actor.displayName"""
    path = ["actor", "displayName"]
    
    def __init__(self, json_record):
        super(
            field_actor_displayname
            , self).__init__(json_record)


class field_actor_preferredusername(_field):
    """Assign to self.value the value of actor.preferredUsername"""
    path = ["actor", "preferredUsername"]
    
    def __init__(self, json_record):
        super(
            field_actor_preferredusername
            , self).__init__(json_record)


class field_actor_id(_field):
    """Assign to self.value the value of actor.id"""
    path = ["actor", "id"]
    
    def __init__(self, json_record):
        super(
            field_actor_id
            , self).__init__(json_record)
        # self.value has an id:twitter....
        self.value = self.value.split(":")[2]


########
# influence 
class field_gnip_kloutscore(_field):
    """Assign to self.value the value of gnip.klout_score"""
    path = ["gnip", "klout_score"]
    
    def __init__(self, json_record):
        super(
            field_gnip_kloutscore
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


class field_actor_followers(_field):
    """Assign to self.value the value of actor.followersCount"""
    path = ["actor", "followersCount"]
    
    def __init__(self, json_record):
        super(
            field_actor_followers
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


class field_actor_friends(_field):
    """Assign to self.value the value of actor.friendsCount"""
    path = ["actor", "friendsCount"]
    
    def __init__(self, json_record):
        super(
            field_actor_friends
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


class field_actor_lists(_field):
    """Assign to self.value the value of actor.listedCount"""
    path = ["actor", "listedCount"]
    
    def __init__(self, json_record):
        super(
            field_actor_lists
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


class field_actor_statuses(_field):
    """Assign to self.value the value of actor.statusesCount"""
    path = ["actor", "statusesCount"]
    
    def __init__(self, json_record):
        super(
            field_actor_statuses
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


########
# influence 
class field_activity_type(_field):
    """Assign to self.value the appropriate value of Tweet, Retweet, or Reply"""
    path = []
    
    def __init__(self, json_record):
        super(
            #field_structure_type
            field_activity_type
            , self).__init__(json_record)
        # self.value is None
        verb = field_verb(json_record).value 
        inReplyTo = "None"
        obj_objtype = "None"
        if "inReplyTo" in json_record:
            # possible KeyError? (JM)
            inReplyTo = json_record["inReplyTo"]["link"]
        if "object" in json_record:
            obj = json_record["object"]
            if "objectType" in obj:
                obj_objtype = obj["objectType"]
        # now we can determine self.value
        if verb == "share" and obj_objtype == "activity":
            self.value = "Retweet"
        elif inReplyTo == "None":
            self.value = "Tweet"
        else:
            self.value = "Reply"


class field_inreplyto_link(_field):
    """Assign to self.value the value of inReplyTo.link"""
    path = ["inReplyTo", "link"]
    
    def __init__(self, json_record):
        super(
            field_inreplyto_link
            , self).__init__(json_record)


class field_object_id(_field):
    """Assign to self.value the value of object.id"""
    path = ["object", "id"]
    
    def __init__(self, json_record):
        super(
            field_object_id
            , self).__init__(json_record)


class field_object_postedtime(_field):
    """Assign to self.value the value of object.postedTime"""
    path = ["object", "postedTime"]
    
    def __init__(self, json_record):
        super(
            field_object_postedtime
            , self).__init__(json_record)



############################
#class TwacsCSV(acscsv.AcsCSV):
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
            , options_struct
            , options_db
            ):
        super(Twacs, self).__init__(delim, options_keypath, options_db)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_lang = options_lang
        self.options_influence = options_influence
        self.options_struct = options_struct
        self.options_db = options_db
        
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
                #TODO: convert gnipDateTime, gnipRemove into classes like everything else
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
        except KeyError:
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record
        # at this point, it's a valid, non-compliance activity
        if self.options_db:
            return self.multi_rec(d, record)
        #
        return self.csv(d, record)

    # start refactor to use objects
    def csv(self, d, record):
        try:                            # KeyError exception at EOF
            # always first 2 items 
#######################
#            # old code (JM)
#            record.append(d["id"])
#            record.append(d["postedTime"])
#######################
            record.append( field_id(d).value )
            record.append( field_postedtime(d).value )
            # add some handling so calling gnacs without a pub is still useful
            #   -put more-specific fields at the beginning to catch them 
            #   -stocktwits is native, so no 'verb' to get here
            obj = d["object"]
            if d["id"].rfind("getglue") != -1 : # getglue 
#                record.append(verb)     # 'body' is inconsistent in gg
                record.append( field_verb(d).value ) 
            elif "foursquareCategories" in obj or "foursquareCheckinOffset" in obj:      # fsq
                record.append(str(obj["geo"]["coordinates"]))
            elif "wpBlogId" in obj:     # wp
                record.append(str(obj["wpBlogId"]))
            elif "tumblrType" in obj:   # tumblr
                record.append(obj["tumblrType"])
            elif "body" in d:           # tw, disqus, stocktw,  
#                record.append(self.cleanField(d["body"]))       
                record.append( field_body(d).value  )       
            elif "link" in d:           # ng
                record.append(d["link"])
            else:                       # ? 
                record.append("None")
            #
#######################
#            # old code (JM)
#            gnip = {}
#            actor = {}
#            if "gnip" in d:
#                gnip = d["gnip"]
#            if "actor" in d:    # no 'actor' in ng
#                actor = d["actor"]
#######################
            if self.options_urls:
                # we may not need to explicitly call the object's .value attr if the .join(record)
                #   calls the objects' __repr__ (JM)
                #
                # if ___.value is "None", the buildListString method isn't correct. try having all
                #   classes store a string as their final self.value
                #
#                record.append( self.buildListString( field_gnip_urls(d).value ) ) 
#                record.append( self.buildListString( field_twitter_urls_url(d).value ) ) 
#                record.append( self.buildListString( field_twitter_urls_expanded_url(d).value ) ) 
#                record.append( self.buildListString( field_twitter_urls_display_url(d).value ) ) 
                record.append( field_gnip_urls(d).value ) 
                record.append( field_twitter_urls_url(d).value ) 
                record.append( field_twitter_urls_expanded_url(d).value ) 
                record.append( field_twitter_urls_display_url(d).value )
#########################
#                # old code (JM)
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
########################
            if self.options_lang:
                # actor lang
                try: 
#                    record.append( self.buildListString( field_actor_lang(d).value ) ) 
                    record.append( field_actor_lang(d).value ) 
                except UnicodeEncodeError, e:
                    record.append("bad-encoding")
                # gnip lang
                record.append( field_gnip_lang(d).value )
                # twitter lang
                record.append( field_twitter_lang(d).value )
#########################
#                # old code (JM)
#                try:
#                    record.append(str([str(l) for l in actor["languages"]]))
#                except UnicodeEncodeError, e:
#                    record.append(str("bad encoding"))
#                #glang = "None"
#                #if "language" in gnip:
#                #    glang = gnip["language"]["value"]
#                tlang = "None"
#                if "twitter_lang" in d:
#                    tlang = d["twitter_lang"]
#                record.append(tlang)
#########################
            if self.options_rules:
#                record.append( self.buildListString( field_gnip_rules(d).value ) )
                record.append( field_gnip_rules(d).value )
#########################
#                # old code (JM)
#                rules = '[]'
#                if "matching_rules" in gnip:
#                    rules = self.buildListString([ "%s (%s)"%(l["value"], l["tag"]) for l in gnip["matching_rules"]])
#                record.append(rules)
#########################
            if self.options_geo:
#                record.append( self.buildListString( field_geo_coords(d).value ) )  
                record.append( field_geo_coords(d).value ) 
                record.append( field_geo_type(d).value )  
#                record.append( self.buildListString( field_location_coords(d).value ) ) 
                record.append( field_location_coords(d).value ) 
                record.append( field_location_type(d).value )  
                record.append( field_location_displayname(d).value )  
                record.append( field_location_twittercountry(d).value )  
                record.append( field_actor_utcoffset(d).value )  
                record.append( field_actor_loc_displayname(d).value )  
                record.append( field_gnip_pl_displayname(d).value )  
                record.append( field_gnip_pl_objecttype(d).value )  
                record.append( field_gnip_pl_country(d).value )  
                record.append( field_gnip_pl_region(d).value )  
                record.append( field_gnip_pl_countrycode(d).value )  
                record.append( field_gnip_pl_locality(d).value )  
                record.append( field_gnip_pl_geo_type(d).value )  
                record.append( field_gnip_pl_geo_coords(d).value )  
#########################
#                # old code (JM)
#                geoType = "None"
#                self.geoCoordsList = None
#                geoCoords = "None"
#                if "geo" in d:
#                    if "type" in d["geo"]:
#                        geoType = d["geo"]["type"]
#                        #self.geoCoords = [str(l) for l in d["geo"]["coordinates"]]
#                        self.geoCoordsList = d["geo"]["coordinates"]
#                        geoCoords = str(self.geoCoordsList)
#                record.append(geoCoords)
#                record.append(geoType)
#                locType = "None"
#                locCoords = "None"
#                locName = "None"
#                locCountry = "None"
#                if "location" in d:
#                    locName = self.cleanField(d["location"]["displayName"])
#                    locCountry = self.cleanField(d["location"]["twitter_country_code"])
#                    if "geo" in d["location"] and d["location"]["geo"] is not None:
#                        if "type" in d["location"]["geo"]:
#                            locType = d["location"]["geo"]["type"]
#                            locCoords = str([str(l) for l in d["location"]["geo"]["coordinates"][0]])
#                record.append(locCoords)
#                record.append(locType)
#                record.append(locName)
#                record.append(locCountry)
#                record.append(str(actor["utcOffset"]))
#                dName = "None"
#                if "location" in actor and "displayName" in actor["location"]:
#                    dName = self.cleanField(actor["location"]["displayName"])
#                record.append(dName)
#
#                # gnip:profileLocations
#                pl_otype = "None"
#                pl_name = "None"
#                # profileLocations:address
#                pl_country = "None"
#                pl_region = "None"
#                pl_countrycode = "None"
#                pl_locality = "None"
#                # profileLocations:geo
#                pl_gtype = "None"
#                pl_coords = "None"
#                if "profileLocations" in gnip:
#                    # n.b. profileLocations is a list, suggests it might include >1 thing eventually
#                    pl = gnip["profileLocations"][0]
#                    if "objectType" in pl:
#                        pl_otype = pl["objectType"]
#                    if "displayName" in pl:
#                        pl_name = pl["displayName"]
#                    if "address" in pl:
#                        adrs = pl["address"]
#                        if "country" in adrs:
#                            pl_country = adrs["country"]
#                        if "region" in adrs:
#                            pl_region = adrs["region"]
#                        if "countryCode" in adrs:
#                            pl_countrycode = adrs["countryCode"]
#                        if "locality" in adrs:
#                            pl_locality = adrs["locality"]
#                    if "geo" in pl:
#                        geo = pl["geo"]
#                        if "type" in geo:
#                            pl_gtype = geo["type"]
#                        if "coordinates" in geo:
#                            pl_coords = str(geo["coordinates"])
#                record.append(pl_name)
#                record.append(pl_otype)
#                record.append(pl_country)
#                record.append(pl_region)
#                record.append(pl_countrycode)
#                record.append(pl_locality)
#                record.append(pl_gtype)
#                record.append(pl_coords)
########################
                #
            if self.options_user:
                record.append( field_actor_displayname(d).value )  
                record.append( field_actor_preferredusername(d).value )  
#########################
#                # old code (JM)
#                record.append(self.cleanField(actor["displayName"]))
#                record.append(self.cleanField(actor["preferredUsername"]))
#                try:
#                    tmp = actor["id"].split(":")[2] #Brian's 1st attempt at Gnacsification
#                except IndexError:
#                    tmp = "actor:id"                    
#                record.append(tmp)
########################
            if self.options_influence:
                record.append( field_gnip_kloutscore(d).value )  
                record.append( field_actor_followers(d).value )  
                record.append( field_actor_friends(d).value )  
                record.append( field_actor_lists(d).value )  
                record.append( field_actor_statuses(d).value )  
#########################
#                # old code (JM)
#                klout = "None"
#                followers = "None"
#                friends = "None"
#                listed = "None"
#                statuses = "None"
#                if "klout_score" in gnip:
#                    klout = str(gnip["klout_score"])
#                followers = str(actor["followersCount"])
#                friends = str(actor["friendsCount"])
#                listed = str(actor["listedCount"])
#                statuses = str(actor["statusesCount"])
#                record.append(klout)
#                record.append(followers)
#                record.append(friends)
#                record.append(listed)
#                record.append(statuses)
#########################
            if self.options_struct:
                record.append( field_activity_type(d).value )  
                record.append( field_inreplyto_link(d).value )  
                record.append( field_object_id(d).value )  
                record.append( field_object_postedtime(d).value )  
#########################
#                # old code (JM)
#                oid = "None"
#                opt = "None"
#                overb = "None"
#                inReplyTo = "None"
#                if "inReplyTo" in d:
#                    inReplyTo = d["inReplyTo"]["link"]
#                if "object" in d:
#                    obj = d["object"]
#                    if "objectType" in obj:
#                        overb = obj["objectType"]
#                if verb == "share" and overb == "activity":
#                    record.append("Retweet")
#                    if "id" in obj:
#                        oid = obj["id"]
#                    if "postedTime" in obj:
#                        opt = obj["postedTime"]
#                elif inReplyTo == "None":
#                    record.append("Tweet")
#                else:
#                    record.append("Reply")
#                record.append(inReplyTo)
#                record.append(oid)
#                record.append(opt)
#########################
            return record
        except KeyError:
            #sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record

    def multi_rec(self, d, record):
        """Return multiple lists for e.g. writing to separate streams/files""" 
        ########
        # need to do a handful of preprocessing steps for various fields. use the 
        #   object attrs where possible 
        #
        # remember that all objects have a string for self.value
        #
        # timestamp format
        t_fmt = "%Y-%m-%dT %H:%M:%S"
        ##### geotag coords
        if not eval( field_location_coords(d).value ):  # .value = "None" (no coords)
            coords = ["None", "None"]
        else:
            coords = eval( field_location_coords(d).value )
        ##### hashtags 
        # don't know anything about them a priori 
        hashtag_list = eval( field_twitter_hashtags_text(d).value )
        n = len(hashtag_list)
        entity_count = 5            # arb number, defined by table schema
        if n < entity_count:    # pad list
            for _ in range(entity_count - n):
                hashtag_list.append("None")
        if n > entity_count:    # truncate list
            hashtag_list = hashtag_list[:entity_count]
        ##### urls
#
#
#
# WIP
#
#

        #
        acs_list = [
                    field_id(d).value 
                    , field_gnip_rules(d).value 
                    , datetime.datetime.utcnow().strftime( t_fmt )
                    , field_postedtime(d).value 
                    , field_verb(d).value 
                    , field_actor_id(d).value 
                    , field_body(d).value 
                    , field_twitter_lang(d).value 
                    , field_gnip_lang(d).value 
                    , field_link(d).value 
                    , field_generator_displayname(d).value 
                    , coords[0] 
                    , coords[1] 
                    , hashtag_list[0]
                    , hashtag_list[1]
                    , hashtag_list[2]
                    , hashtag_list[3]
                    , hashtag_list[4]

                    ] 
        ustatic_list = [
                        "test_ustatic"
                        ]
        udyn_list = [ 
                    "test_udyn"
                    ]
        #
        flag = "GNIPSPLIT"  # this is hardcoded into gnacs.py, as well. change both if needed!
        # only need mortar on first two bricks 
        [ x.append(flag) for x in acs_list, ustatic_list ]
        combined_list = [] 
        combined_list.extend(acs_list)
        combined_list.extend(ustatic_list)
        combined_list.extend(udyn_list)
        #
        return combined_list 


