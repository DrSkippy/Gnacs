# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague, Fiona Pigot"
__license__="Simplified BSD"

import sys
import acscsv
import inspect
import datetime
import itertools

# move to acscsv?
class _field(object):
    """
    Base class for finding the appropriate key-value pairs in a JSON Activity Streams payload.
    Common default value (for e.g. missing values) is "None", but child subclasses can override
    this default when needed. Subclasses should also define the keypath to the desired location
    by overwriting the "path" list. 
    """
    # default values, can be overwritten in custom classes 
    default_value = "None"
    value = None
    value_list = []
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


    def fix_length(self, iterable, limit=None):
        """
        Takes an iterable (typically a list) and an optional maximum length (limit). 
        If limit is not given, and the input iterable is not equal to self.default_value
        (typically "None"), the input iterable is returned. If limit is given, the return
        value is a list that is either truncated to the first limit items, or padded 
        with self.default_value until it is of size limit 
        """
        res = [] 

        if limit is None:
            # no limits on the length of the result, so just return the original iterable
            res = iterable
        else:
            if iterable == self.default_value or len(iterable) == 0:
                # if walk_path() finds the final key, but the value is an empty list 
                #   (common for e.g. the contents of twitter_entities) 
                #   overwrite self.value with a list of self.default_value and of length limit
                res = [ self.default_value ]*limit
            else:
                # found something useful in the iterable, either pad the list or truncate 
                #   to end up with something of the proper length 
                current_length = len( iterable ) 
                if current_length < limit:
                    res = iterable + [ self.default_value 
                                        for _ in range(limit - current_length) ]
                else:  
                    res = iterable[:limit]
        return res




# TODO:
# - test removing the super() call if only overwriting 'path'
# - convert all class docstrings to consistently use the key1.key2.key3 format 
# - choose an ordering for the field classes that makes sense / is managable and maintainable 
# - abstract all list extractions & padding (e.g fields in twitter_entities) to general 
#       class/method a la _field() class


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
# - on subclassing...
# all classes should reach back to the _field class, which does the JSON walk and sets the initial
# self.value. the first round of subclasses inherit from _field and update self.value to be backward
# compatible to older gnacs. in order to do further processing or create custom output, you can also 
# subclass the existing field_* classes and add your processing in the class constructor. this should 
# allows us to follow the "unix philosophy" and keep building on these classes. Note that the classes
# currently ending in _DB() are leaving self.value in a mix of str and list states. 
#
# - on self.value types...
# in order to do the final list join, all classes must end with self.value as a string. to maintain 
# backward compatibility, all classes currently result in similar self.value fields as before. now, 
# when you need to slightly modify the output (or create wholly different, custom output), you can 
# start by inheriting from the most basic class of that type, and manipulate self.value accordingly.
#
 
class example_class(_field):
    """
    Assign to self.value the value of zig.zag . This is the dictionary created by the user's chosen
    values of zig and zag (at the time of account creation. 

    Your real class should begin with 'field_' in order to be included in the test suite.
    """
    # each new class should overwrite the self.path variable with a list of the appropriate keys
    #   that lead to the field of interest
    path = ["zig", "zag"]               

    # if the final result to be used in the custom csv function is most appropriately a list, 
    #   reassign self.value_list so the code is easier to read in the assembly/output portion 
    value_list = []

    def __init__(self, json_record):
        """
        Calls parent constructor, which walks the specified dict path to find appropriate value
        to store in self.value. This __init__() only needs to be included if there is further 
        processing to be done on self.value e.g. slicing a list/string/other computations."""
        super(
                example_class
                , self).__init__(json_record)
        # include a helpful note here for the next user that describes what self.value becomes, 
        #   and then again at the final state
        # self.value is now a dictionary of magical unicorns 
        self.value = "|".join( [ x["rainbows"] for x in self.value ] )
        # self.value is now a pipe-delimited string of the values corresponding to the 'rainbow' keys 

        self.value_list = self.value.split("|")
        # self.value_list is now a list of the 'rainbow' keys (as an example)


####################
#   top-level keys 
####################

class field_verb(_field):
    """assign to self.value the value of top-level 'verb' key"""
    # specify path to desired field as a list of dict keys 
    path = ["verb"]
    # if needed, overwrite default_value
    default_value = "Unidentified meta message"
    
#    def __init__(self, json_record):
#        """Calls base constructor, which walks the specified dict path to find appropriate value"""
#        super(
#                field_verb
#                , self).__init__(json_record)
        # in any field_* class, add any needed custom parsing here


class field_id(_field):
    """assign to self.value the value in id"""
    path = ["id"]
    
    def __init__(self, json_record):
        super(
            field_id
            , self).__init__(json_record)
        # self.value starts with tag:search.twitter..... remove all but the actual id 
        self.value = self.value.split(":")[2]


class field_postedtime(_field):
    """assign to self.value the value in postedTime"""
    path = ["postedTime"]
    
#    def __init__(self, json_record):
#        super(
#            field_postedtime
#            , self).__init__(json_record)


class field_body(_field):
    """assign to self.value the value in top-level body"""
    path = ["body"]
    
#    def __init__(self, json_record):
#        super(
#            field_body
#            , self).__init__(json_record)


class field_link(_field):
    """assign to self.value the value in top-level link"""
    path = ["link"]
    
#    def __init__(self, json_record):
#        super(
#            field_link
#            , self).__init__(json_record)


class field_generator_displayname(_field):
    """assign to self.value the value in generator.displayName"""
    path = ["generator", "displayName"]
    
#    def __init__(self, json_record):
#        super(
#            field_generator_displayname
#            , self).__init__(json_record)


####################
#   'gnip' fields 
####################
#
# TODO: use self.walk_json(self.value) to get the second-level values (JM) 

class field_gnip_urls(_field):
    """assign to self.value the list of 'expanded_url' values within 'gnip', 'urls'"""
    path = ["gnip", "urls"]
    
    def __init__(self, json_record):
        super(
            field_gnip_urls
            , self).__init__(json_record)
        # self.value is (possibly) a list of url & expanded url dicts
        if self.value != self.default_value:
            self.value = str( [ x["expanded_url"] for x in self.value ] ) 


class _field_twitter_urls(_field):
    """
    Base class for accessing arbitrary url fields within twitter_entities.urls . Takes 
    a key that addresses the particular value within twitter_entities_urls . Assigns 
    to self.value_list a string representation of the corresponding url list (or the 
    default value in a list). 
    """
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
        #
        self.value_list = eval( self.value )


class field_twitter_urls_url(_field_twitter_urls):
    """
    assign to self.value the list of 'url' values within 'twitter_entities', 'urls' dict.
    Inherits from _filed_twitter_urls class.
    """
    
    def __init__(self, json_record, limit=None):
        super(
            field_twitter_urls_url
            , self).__init__(json_record, "url")
        if limit is not None:
            self.value = self.fix_length( self.value, limit )


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
    """Assign to self.value a list of twitter_entities.hashtags 'texts'"""
    path = ["twitter_entities", "hashtags"]

    # consider abstracting the path to a parent class and subclassing for specific fields

    def __init__(self, json_record):
        super(
            field_twitter_hashtags_text
            , self).__init__(json_record)
        # self.value is possibly a list of dicts for each activity hashtag
        if self.value != self.default_value and len(self.value) > 0:
            self.value_list = [ x["text"] for x in self.value ] 
            self.value = str( self.value_list ) 
        # hashtags are an existing feature in gnacs, so extend this class for 
        #   the db-specific configuration...
        #print >>sys.stderr, "self.value_list={} (type={})".format(self.value_list, type(self.value_list))


class field_twitter_hashtags_text_DB(field_twitter_hashtags_text):
    """
    Combine the first 'limit' hashtags found in the payload into a list and assign to 
    self.value. If there are less than 'limit', the list is padded with 
    self.default_value 
    """

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_hashtags_text_DB
            , self).__init__(json_record)
        # self.value is either a list of hashtag texts for each activity hashtag or default_value
        if self.value == self.default_value or len(self.value) == 0:
            self.value = [ self.default_value ]*limit
        else:   # found something in the list
            self.value = self.fix_length( self.value, limit ) 
        # 
        self.value_list = self.value


class field_twitter_symbols_text_DB(_field):
    """
    Assign to self.value a list of twitter_entities.symbols 'text's.
    This one is a little experimental... haven't seen it in the wild (Activity Streams) yet, 
    so using https://blog.twitter.com/2013/symbols-entities-tweets as the template.
    """
    path = ["twitter_entities", "symbols"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_symbols_text_DB
            , self).__init__(json_record)
        # self.value is possibly a list of dicts for each activity symbol 
        if self.value == self.default_value or len(self.value) == 0:
            self.value_list = [ self.default_value ]*limit
        else:   # found something in the list
            current_len = len(self.value)
            if current_len < limit:         # need to pad list
                [ self.value_list.append("None") for _ in range(limit - current_len) ]
            elif current_len > limit:         # need to truncate list
                #self.value = self.value[:current_len]
                self.value_list = self.value_list[:limit]
        # self.value is now a list of length 'limit' with 
        #  some combination of symbol text (str) and "None"
        self.value = str( self.value_list ) 
        #print >>sys.stderr, "self.value_list={} (type={})".format(self.value_list, type(self.value_list))


class field_twitter_mentions_name_id_DB(_field):
    """
    Assign to self.value a list of 'limit' twitter_entities.user_mentions.screen_name and .id pairs 
    (in order, but in a flat list).
    """
    path = ["twitter_entities", "user_mentions"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_mentions_name_id_DB
            , self).__init__(json_record)
#        print >>sys.stderr, "called field_twitter_mentions_name_id_DB"
#        print >>sys.stderr, "self.value={}".format(self.value)
        # self.value is possibly a list of dicts for each activity user mention 
        if self.value == self.default_value or len(self.value) == 0:
            self.value = [ self.default_value ]*(2*limit)
        else:   # found something in the list
            #self.value = [ [ x["screen_name"], x["id_str"] ]  for x in self.value ]
            # couldn't get the nesting correct with inline list comp on self.value... (JM)
            tmp = []
            [ tmp.extend( [ x["screen_name"], x["id_str"] ] ) for x in self.value ]
            self.value = tmp
#            print >>sys.stderr, "self.value={}".format(self.value)
            current_len = len(self.value)
            if current_len < limit:         # need to pad list
                #[ self.value.extend( ["None", "None"] ) for _ in range(limit - current_len) ]
                for _ in range( limit - current_len):
                    self.value += ["None", "None"]
#                print >>sys.stderr, "self.value={}".format(self.value)
            elif current_len > limit:         # need to truncate list
                #self.value = self.value[:current_len]
                self.value = self.value[:limit]
#                print >>sys.stderr, "self.value={}".format(self.value)
            # self.value is now a list of lists, with total length 2*limit. now flatten it:
            #self.value = list( itertools.chain.from_iterable( self.value ) ) 
#        print >>sys.stderr, "self.value={}\n\n".format(self.value)
        self.value_list = self.value
        print >>sys.stderr, "self.value_list={} (type={})".format(self.value_list, type(self.value_list))


class field_twitter_media_id_DB(_field):
    """
    Assign to self.value a list of twitter_entities.media.id
    """
    path = ["twitter_entities", "media"]

    def __init__(self, json_record):
        super(
            field_twitter_media_id_DB 
            , self).__init__(json_record)
        # self.value is possibly a list of dicts for each activity media object 
        if self.value == self.default_value or len(self.value) == 0:
            self.value = [ self.default_value ]*limit
#
# WIP
#







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
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_lang
#            , self).__init__(json_record)


class field_twitter_lang(_field):
    """assign to self.value the value of top-level 'twitter_lang'"""
    path = ["twitter_lang"]
    
#    def __init__(self, json_record):
#        super(
#            field_twitter_lang
#            , self).__init__(json_record)


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
    
#    def __init__(self, json_record):
#        super(
#            field_geo_type
#            , self).__init__(json_record)


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


class field_geo_coords_DB(field_geo_coords):
    """
    Modify self.value assigned in the field_geo_coords class. Assign self.value_list to a list 
    of either  [lat, long] or 2x self.default_value. 
    """
    
    def __init__(self, json_record):
        super(
            field_geo_coords_DB
            , self).__init__(json_record)
        # self.value is a str of either default_value or '[lat, lon]' 
        if self.value == self.default_value:
            self.value_list = [ self.default_value, self.default_value ]
        else:
            self.value_list = eval( self.value )
        #print >>sys.stderr, "field_geo_coords_DB.value_list={} (type={})".format(self.value_list, type(self.value_list))
 

class field_location_type(_field):
    """assign to self.value the value of location.geo.type ."""
    path = ["location", "geo", "type"]
    
#    def __init__(self, json_record):
#        super(
#            field_location_type
#            , self).__init__(json_record)


class field_location_displayname(_field):
    """assign to self.value the value of 'location', 'displayName' """
    path = ["location", "displayName"]
    
#    def __init__(self, json_record):
#        super(
#            field_location_displayname
#            , self).__init__(json_record)


class field_location_coords(_field):
    """
    Assign to self.value the value of location.geo.coordsindates . This the bounding 
    polygon from the original activity payload from Twitter.
    """
    path = ["location", "geo", "coordinates"]

    def __init__(self, json_record):
        super(
            field_location_coords
            , self).__init__(json_record)
        # self.value is either default_value or a list of lists of polygon vertices (lists) 
        if self.value == self.default_value:
            self.value = [ self.default_value ]
        else:
            self.value = str( self.value[0] ) 


class field_location_twittercountry(_field):
    """assign to self.value the value of 'location', 'twitter_country_code' """
    path = ["location", "twitter_country_code"]
    
#    def __init__(self, json_record):
#        super(
#            field_location_twittercountry
#            , self).__init__(json_record)


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
    
#    def __init__(self, json_record):
#        super(
#            field_actor_loc_displayname
#            , self).__init__(json_record)


class field_gnip_pl_displayname(_field):
    """
    Assign to self.value the value of gnip.profileLocation.displayName . Currently only 
    supports one list item, but could add support more in the future.
    """
    path = ["gnip", "profileLocations", "displayName"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_displayname
#            , self).__init__(json_record)
 
class field_gnip_pl_objecttype(_field):
    """Assign to self.value the value of gnip.profileLocations.objectType"""
    path = ["gnip", "profileLocations", "objectType"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_objecttype
#            , self).__init__(json_record)


class field_gnip_pl_country(_field):
    """Assign to self.value the value of gnip.profileLocations.address.country"""
    path = ["gnip", "profileLocations", "address", "country"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_country
#            , self).__init__(json_record)


class field_gnip_pl_region(_field):
    """Assign to self.value the value of gnip.profileLocations.address.region"""
    path = ["gnip", "profileLocations", "address", "region"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_region
#            , self).__init__(json_record)


class field_gnip_pl_countrycode(_field):
    """Assign to self.value the value of gnip.profileLocations.address.countryCode"""
    path = ["gnip", "profileLocations", "address", "countryCode"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_countrycode
#            , self).__init__(json_record)


class field_gnip_pl_locality(_field):
    """Assign to self.value the value of gnip.profileLocations.address.locality"""
    path = ["gnip", "profileLocations", "address", "locality"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_locality
#            , self).__init__(json_record)


class field_gnip_pl_geo_type(_field):
    """Assign to self.value the value of gnip.profileLocations.geo.type"""
    path = ["gnip", "profileLocations", "geo", "type"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_geo_type
#            , self).__init__(json_record)


class field_gnip_pl_geo_coords(_field):
    """Assign to self.value the value of gnip.profileLocations.geo.coordinates"""
    path = ["gnip", "profileLocations", "geo", "coordinates"]
    
#    def __init__(self, json_record):
#        super(
#            field_gnip_pl_geo_coords
#            , self).__init__(json_record)


########
# actor 
class field_actor_displayname(_field):
    """Assign to self.value the value of actor.displayName"""
    path = ["actor", "displayName"]
    
#    def __init__(self, json_record):
#        super(
#            field_actor_displayname
#            , self).__init__(json_record)


class field_actor_preferredusername(_field):
    """Assign to self.value the value of actor.preferredUsername"""
    path = ["actor", "preferredUsername"]
    
#    def __init__(self, json_record):
#        super(
#            field_actor_preferredusername
#            , self).__init__(json_record)


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
    
#    def __init__(self, json_record):
#        super(
#            field_inreplyto_link
#            , self).__init__(json_record)


class field_object_id(_field):
    """Assign to self.value the value of object.id"""
    path = ["object", "id"]
    
#    def __init__(self, json_record):
#        super(
#            field_object_id
#            , self).__init__(json_record)


class field_object_postedtime(_field):
    """Assign to self.value the value of object.postedTime"""
    path = ["object", "postedTime"]
    
#    def __init__(self, json_record):
#        super(
#            field_object_postedtime
#            , self).__init__(json_record)



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
        Takes JSON payload d (as a dictionary), identifies the activity type by its verb, 
        and returns compliance fields if needed. Otherwise, returns the parsed + delimited line, as 
        determined by user-specified options.
        """ 
        record = []
        try:        # try block needs a KeyError exception?
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
            # custom output function
            return self.multi_file_DB(d, record)
        #
        return self.csv(d, record)


    def csv(self, d, record):
        try:                            # KeyError exception at EOF
            # always first 3 items 
            record.append( field_id(d).value )
            record.append( field_postedtime(d).value )
            record.append( field_body(d).value )
            ### reverting my earlier inclination here and removing this code
#            # add some handling so calling gnacs without a pub is still useful
#            #   -put more-specific fields at the beginning to catch them 
#            #   -stocktwits is native, so no 'verb' to get here
#            obj = d["object"]
#            if d["id"].rfind("getglue") != -1 : # getglue 
#                record.append( field_verb(d).value ) 
#            elif "foursquareCategories" in obj or "foursquareCheckinOffset" in obj:      # fsq
#                record.append(str(obj["geo"]["coordinates"]))
#            elif "wpBlogId" in obj:     # wp
#                record.append(str(obj["wpBlogId"]))
#            elif "tumblrType" in obj:   # tumblr
#                record.append(obj["tumblrType"])
#            elif "body" in d:           # tw, disqus, stocktw,  
#                record.append( field_body(d).value  )       
#            elif "link" in d:           # ng
#                record.append(d["link"])
#            else:                       # ? 
#                record.append("None")
            #
            ### begin command line options
            if self.options_urls:
                record.append( field_gnip_urls(d).value ) 
                record.append( field_twitter_urls_url(d).value ) 
                record.append( field_twitter_urls_expanded_url(d).value ) 
                record.append( field_twitter_urls_display_url(d).value )
            if self.options_lang:
                # actor lang
                try: 
                    record.append( field_actor_lang(d).value ) 
                except UnicodeEncodeError, e:
                    record.append("bad-encoding")
                record.append( field_gnip_lang(d).value )
                record.append( field_twitter_lang(d).value )
            if self.options_rules:
                record.append( field_gnip_rules(d).value )
            if self.options_geo:
                record.append( field_geo_coords(d).value ) 
                record.append( field_geo_type(d).value )  
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
            if self.options_user:
                record.append( field_actor_displayname(d).value )  
                record.append( field_actor_preferredusername(d).value )  
            if self.options_influence:
                record.append( field_gnip_kloutscore(d).value )  
                record.append( field_actor_followers(d).value )  
                record.append( field_actor_friends(d).value )  
                record.append( field_actor_lists(d).value )  
                record.append( field_actor_statuses(d).value )  
            if self.options_struct:
                record.append( field_activity_type(d).value )  
                record.append( field_inreplyto_link(d).value )  
                record.append( field_object_id(d).value )  
                record.append( field_object_postedtime(d).value )  
            return record
        except KeyError:
            #sys.stderr.write("Field missing from record (%d), skipping\n"%self.cnt)
            record.append(acscsv.gnipError)
            record.append(acscsv.gnipRemove)
            return record

    def multi_file_DB(self, d, record):
        """
        Custom output format designed for loading multiple database tables.
        Creates 3 separate lists of activity fields, joins them on a GNIPSPLIT to be split 
        at the gnacs.py level and written to separate files.      
        """
        # timestamp format
        t_fmt = "%Y-%m-%dT%H:%M:%S"

        # this is now abstracted to the individual classes (via default constructor args)
        # field limit in various list tables 
        limit = 5
    
        # for convenience (and tidiness) here, some of these new classes will have self.value
        #  be an actual list, so that its length can be arbitrarily defined in one place (just above) 

#
#   replace value with list_value
#   remove empty constructors
#   make the constructor do all the work 
#

        #print >>sys.stderr, "field_twitter_mentions_name_id_DB(d, limit).value={}".format(field_twitter_mentions_name_id_DB(d, limit).value)
        acs_list = [
                    # <class>.value is a string 
                    # <class>.value_list is a list 
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
                    ] \
                    + field_geo_coords_DB(d).value_list \
                    + field_twitter_hashtags_text_DB(d).value_list \
                    + field_twitter_symbols_text_DB(d).value \
                    + field_twitter_mentions_name_id_DB(d).value_list 

#
#   WIP
#



#                    + field_twitter_mentions_name_id_DB(d, limit).value_list 
#                    + itertools.chain.from_iterable(                
#                        zip( self.fix_length( field_twitter_urls_url(d).value, limit ) 
#                            , self.fix_length( field_twitter_urls_expanded_url(d).value, limit ) 
#                        )
#                    )
                    # call the fix_length method in the constructor of the class (pass the length from here)
                    #   (as an optional kwarg)
                    
                    # ^ add the media info


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


