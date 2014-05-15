# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague"
__license__="Simplified BSD"

import sys
import acscsv
from datetime import datetime
import re

## move to acscsv?
#class _field(object):
#    """
#    Base class for extracting the desired value at the end of a series of keys in a JSON Activity 
#    Streams payload. Set the application-wide default value (for e.g. missing values) here, 
#    but also use child classes to override when necessary. Subclasses also need to define the 
#    key-path (path) to the desired location by overwriting the path attr.
#    """
#    # set some default values; these can be overwritten in custom classes 
#    default_t_fmt = "%Y-%m-%d %H:%M:%S"
#    #default_value = "None"
#    default_value = "\\N"           # escaped \N ==> MySQL NULL
#    value = None                    # str representation of the field, often = str( self.value_list ) 
#    value_list = [ default_value ]  # overwrite when value is most appropriately a list 
#    path = []                       # dict key-path to follow for desired value
#
#    def __init__(self, json_record):
#        self.value = self.walk_path(json_record)
#
#    def __repr__(self):
#        return self.value
#
#    def walk_path(self, json_record):
#        res = json_record
#        for k in self.path:
#            if k not in res:
#                return self.default_value
#            res = res[k]
#        # handle the special case where the walk_path found null (JSON) which converts to 
#        # a Python None. Only use "None" (str version) if it's assigned to self.default_value 
#        res = res if res is not None else self.default_value
#        return res
#
#
#    def fix_length(self, iterable, limit=None):
#        """
#        Take an iterable (typically a list) and an optional maximum length (limit). 
#        If limit is not given, and the input iterable is not equal to self.default_value
#        (typically "None"), the input iterable is returned. If limit is given, the return
#        value is a list that is either truncated to the first limit items, or padded 
#        with self.default_value until it is of size limit. Note: strings are iterables, 
#        so if you pass this function a string, it will (optionally) truncate the 
#        number of characters in the string according to limit. 
#        """
#        res = [] 
#
#        if limit is None:
#            # no limits on the length of the result, so just return the original iterable
#            res = iterable
#        else:
#            #if len(iterable) == 0:
#            if iterable == self.default_value or len(iterable) == 0:
#                # if walk_path() finds the final key, but the value is an empty list 
#                #   (common for e.g. the contents of twitter_entities) 
#                #   overwrite self.value with a list of self.default_value and of length limit
#                res = [ self.default_value ]*limit
#            else:
#                # found something useful in the iterable, either pad the list or truncate 
#                #   to end up with something of the proper length 
#                current_length = len( iterable ) 
#                if current_length < limit:
#                    res = iterable + [ self.default_value 
#                                        for _ in range(limit - current_length) ]
#                else:  
#                    res = iterable[:limit]
#        return res
#
#
#class acscsv._limited_field(acscsv._field):
#    #TODO: is there a better way that this class and the fix_length() method in _field class
#    #       could be combined?
#    """
#    Takes JSON record (in python dict form) and optionally a maximum length (limit, 
#    with default length=5). Uses parent class _field() to assign the appropriate value 
#    to self.value. When self.value is a list of dictionaries, 
#    inheriting from acscsv._limited_field() class allows for the extraction and combination of 
#    an arbitrary number of fields within self.value into self.value_list.
#
#    Ex: if your class would lead to having 
#    self.value = [ {'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6} ], and what you'd like 
#    is a list that looks like [ 1, 2, 4, 5 ], inheriting from acscsv._limited_field() allows you 
#    to overwrite the fields list ( fields=["a", "b"] ) to obtain this result. 
#    Finally, self.value is set to a string representation of the final self.value_list.
#    """
#    fields = None 
#    
#    #TODO: set limit=None by default and just return as many as there are, otherwise (by specifying 
#    #    limit), return a maximum of limit.
#
#    def __init__(self, json_record, limit=1):
#        super(
#            acscsv._limited_field 
#            , self).__init__(json_record)
#        # self.value is possibly a list of dicts for each activity media object 
#        if self.fields:
#            # start with default list full of the default_values
#            self.value_list = [ self.default_value ]*( len(self.fields)*limit )
#            if self.value != self.default_value: 
#                for i,x in enumerate(self.value):   # iterate over the dicts in the list
#                    if i < limit:                   # ... up until you reach limit 
#                        for j,y in enumerate(self.fields):      # iterate over the dict keys 
#                            self.value_list[ len( self.fields )*i + j ] = x[ self.fields[j] ] 
#            # finally, str-ify the list
#            self.value = str( self.value_list )
#
#
## TODO:
## - consolidate acscsv._limited_field() & fix_length() if possible 
## - replace 2-level dict traversal (eg profileLocation base class) with acscsv.walk_path() or 
##       similar helper method 


########################################
#   example class 
########################################
 
class example_user_rainbows(acscsv._field):
    """
    In this ficticious example, take a dict (data) and assign to self.value a pipe-delimited list 
    of the users's rainbow color choices. Values are extracted from the dictionary at the end of 
    the gnip.zig.zag key-path. 

    Your real class should begin with 'field_' in order to be included in the test suite. It should 
    also try to strike a balance between being user-friendly (can the next user figure out what it
    does without reading too much code?) and being 500 characters long. 
    
    ===
    >>> example_user_rainbows(data).value
    blue|red|green 

    >>> example_user_rainbows(data).value_list
    ["blue", "red", "green"]
    """
    # your new classes should overwrite the self.path variable with a list of the appropriate keys
    #   that lead to the field of interest
    path = ["gnip", "zig", "zag"]               

    # if the final result to be used in the custom csv function is most appropriately a list, 
    #   reassign self.value_list so the code is easier to read in the assembly/output portion 
    value_list = []

    def __init__(self, json_record):
        """
        Call the parent constructor which walks the specified dict path to find 
        appropriate value to store in self.value.         

        Note that the explicit inclusion of this constructor is only necessary if additional 
        processing is being done on self.value or .value_list. If the end value is e.g. simply
        the correct string, just inheriting from the parent class (ie. _field ) will assign 
        self.value. 
        """
        super(
                example_user_rainbows
                , self).__init__(json_record)
        #
        # include a short note here for the next user that describes what self.value becomes, 
        #   and then again at the final state, if helpful
        #
        # self.value is now a dictionary of magical unicorns 
        self.value = "|".join( [ x["rainbows"] for x in self.value ] )
        # self.value is now a pipe-delimited str of values corresponding to the unicorns' 'rainbow' keys 
        self.value_list = self.value.split("|")
        # self.value_list is now a list of the 'rainbow' keys (as an example)



########################################
#   activity type 
########################################

class field_activity_type(acscsv._field):
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



########################################
#   top-level fields 
########################################

class field_verb(acscsv._field):
    """Take a dict, assign to self.value the value in the top-level verb key.""" 
    path = ["verb"]
    # overwrite this default value because records missing this field should be called out (badness) 
    default_value = "Unidentified meta message"
    

class field_id(acscsv._field):
    """Take a dict, assign to self.value the value in the top-level id key.""" 
    path = ["id"]
    
    def __init__(self, json_record):
        super(
            field_id
            , self).__init__(json_record)
        # self.value is a str beginning w/ tag:search.twitter..... remove all but the actual id 
        self.value = self.value.split(":")[2]


class field_postedtime(acscsv._field):
    """
    Take a dict, assign to self.value the value in the top-level postedTime key. Timestamp is 
    formatted according to input_fmt, which is set in the constructor.
    """
    path = ["postedTime"]

    # this is the more elegant approach -- replace someday, if needed 
    #dateRE = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}", re.IGNORECASE)

    def __init__(self, json_record):
        super(
            field_postedtime 
            , self).__init__(json_record)
        # self.value is a datetime string 
        input_fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        self.value = datetime.strptime( 
                        self.value, input_fmt 
                        ).strftime( 
                            self.default_t_fmt ) 
   

class field_body(acscsv._field):
    """Take a dict, assign to self.value the value in top-level body key."""
    path = ["body"]
    

class field_link(acscsv._field):
    """Take a dict, assign to self.value the value in top-level link key."""
    path = ["link"]
    

class field_twitter_lang(acscsv._field):
    """Take a dict, assign to self.value the value of top-level twitter_lang key."""
    path = ["twitter_lang"]
    

########################################
#   'actor' fields 
########################################

class field_actor_id(acscsv._field):
    """
    Assign to self.value the numerical value of actor.id (after stripping off 
    the leading 'id:twitter...' characters.
    """
    path = ["actor", "id"]
    
    def __init__(self, json_record):
        super(
            field_actor_id
            , self).__init__(json_record)
        # self.value has an id:twitter....
        self.value = self.value.split(":")[2]


class field_actor_postedtime(acscsv._field):
    """
    Assign to self.value the value of actor.postedTime (input format is defined in the 
    constructor, output format is default unless overwritten).
    """ 
    path = ["actor", "postedTime"]
    
    # this is a more elegant approach -- convert someday, if needed 
    #dateRE = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}", re.IGNORECASE)

    def __init__(self, json_record):
        super(
            field_actor_postedtime 
            , self).__init__(json_record)
        # self.value is a string (of a timestamp) 
        input_fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        self.value = datetime.strptime(self.value, input_fmt).strftime(self.default_t_fmt) 


class field_actor_lang(acscsv._field):
    """Assign to self.value the first value in the list at actor.languages"""
    path = ["actor", "languages"]
    
    def __init__(self, json_record):
        super(
            field_actor_lang
            , self).__init__(json_record)
        # self.value is a list, but have only ever seen it with one value, so take that one. 
        # can use str( self.value ) if more than one appear someday
        self.value = self.value[0]


class field_actor_displayname(acscsv._field):
    """Assign to self.value the value of actor.displayName"""
    path = ["actor", "displayName"]


class field_actor_preferredusername(acscsv._field):
    """Assign to self.value the value of actor.preferredUsername"""
    path = ["actor", "preferredUsername"]
 

class field_actor_summary(acscsv._field):
    """Assign to self.value the value of actor.summary"""
    path = ["actor", "summary"]


class field_actor_acct_link(acscsv._field):
    """Assign to self.value the value of actor.link"""
    path = ["actor", "link"]


class field_actor_links(acscsv._field):
    """
    Assign to self.value a string repr of a list of the links contained in actor.links (or 
    default_value if the corresponding dict is empty). The number of links included in the 
    list is optionally specified in the constructor. 
    """
    path = ["actor", "links"]

    def __init__(self, json_record, limit=2):
        super(
            field_actor_links
            , self).__init__(json_record)
        if self.value != self.default_value:
            # ignore the links that are "null" in the payload ( ==> None in the dict )
            self.value_list = [ x["href"] for x in self.value if x["href"] is not None ] 
            self.value_list = self.fix_length( self.value_list, limit )


class field_actor_twittertimezone(acscsv._field):
    """Assign to self.value the value of actor.twitterTimeZone"""
    path = ["actor", "twitterTimeZone"]


class field_actor_utcoffset_DB(acscsv._field):
    """Assign to self.value the value of actor.utcOffset."""
    path = ["actor", "utcOffset"]
    

class field_actor_utcoffset(field_actor_utcoffset_DB):
    """
    Assign to self.value a string repr of the value of actor.utcOffset. Ensures backward 
    compatibility with classic, stringy, gnacs.py output.
    """
   
    def __init__(self, json_record):
        super(
            field_actor_utcoffset
            , self).__init__(json_record)
        # self.value is a signed integer - str-ify for backward compatibility 
        self.value = str( self.value )


class field_actor_verified(acscsv._field):
    """
    Assign to self.value a 0/1 boolean repr of the value of actor.verified. Default is False (0).
    """
    path = ["actor", "verified"]
    default_value = False

    def __init__(self, json_record):
        super(
            field_actor_verified
            , self).__init__(json_record)
        # self.value is possibly boolean 
        try:
            self.value = int( self.value )
        except ValueError, e:
            sys.stderr.write("Unable to convert Verified field, error={}".format(e))


class field_actor_loc_displayname(acscsv._field):
    """assign to self.value the value of actor.location.displayName"""
    path = ["actor", "location", "displayName"]
    

class field_actor_followers_DB(acscsv._field):
    """Assign to self.value the value of actor.followersCount."""
    path = ["actor", "followersCount"]
    # self.value is an int  
 

class field_actor_followers(field_actor_followers_DB):
    """Assign to self.value a str-ified repr of the value of actor.followersCount"""
    
    def __init__(self, json_record):
        super(
            field_actor_followers
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )
  
 
class field_actor_friends_DB(acscsv._field):
    """Assign to self.value the value of actor.friendsCount."""
    path = ["actor", "friendsCount"]
    # self.value is an int


class field_actor_friends(field_actor_friends_DB):
    """Assign to self.value a str-ified repr of the value of actor.friendsCount."""
    
    def __init__(self, json_record):
        super(
            field_actor_friends
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


class field_actor_listed_DB(acscsv._field):
    """Assign to self.value the value of actor.listedCount"""
    path = ["actor", "listedCount"]
    # self.value is an int


class field_actor_listed(field_actor_listed_DB):
    """Assign to self.value a str-ified repr of the value of actor.listedCount"""
    
    def __init__(self, json_record):
        super(
            field_actor_listed
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )


class field_actor_statuses_DB(acscsv._field):
    """Assign to self.value the value of actor.statusesCount"""
    path = ["actor", "statusesCount"]
    # self.value is an int 
    # nb: for file output, this distinction may not be necessary (JM) 


class field_actor_statuses(field_actor_statuses_DB):
    """Assign to self.value a str-ified repr of the value of actor.statusesCount"""
    
    def __init__(self, json_record):
        super(
            field_actor_statuses
            , self).__init__(json_record)
        # self.value is an int 
        self.value = str( self.value )



########################################
#   'generator' fields 
########################################

class field_generator_displayname(acscsv._field):
    """Assign to self.value the value of generator.displayName"""
    path = ["generator", "displayName"]
    


########################################
#   'gnip' fields 
########################################

class field_gnip_rules(acscsv._field):
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


class field_gnip_urls(acscsv._field):
    """Assign to self.value the list of 'expanded_url' values within 'gnip', 'urls'"""
    path = ["gnip", "urls"]
    
    def __init__(self, json_record):
        super(
            field_gnip_urls
            , self).__init__(json_record)
        # self.value is possibly a list of url & expanded url dicts
        if self.value != self.default_value:
            self.value_list = [ x["expanded_url"] for x in self.value ]
            self.value = str( self.value_list ) 


class field_gnip_lang(acscsv._field):
    path = ["gnip","language","value"]
    

# profileLocations

class field_gnip_pl_displayname(acscsv._limited_field):
    """Assign to self.value the value of gnip.profileLocation.displayName."""
    path = ["gnip", "profileLocations"]
    fields = ["displayName"]
    # use default limit=1 in acscsv._limited_field constructor
    def __init__(self, json_record):
        super(
            field_gnip_pl_displayname 
            , self).__init__(json_record)
        # self.value is possibly a str repr of self.value_list
        if self.value != self.default_value:
            self.value = self.value_list[0]


class field_gnip_pl_objecttype(acscsv._limited_field):
    """Assign to self.value the value of gnip.profileLocations.objectType."""
    path = ["gnip", "profileLocations"]
    fields = ["objectType"]

# for nested dicts, use one-level-deeper "subfield" 
class _field_gnip_pl_base(acscsv._limited_field):
    """
    Abstract a bunch of the boilerplate needed to check for and extract the things in 
    in gnip.profileLocations. 
    """
    path = ["gnip", "profileLocations"]
    fields = None 
    subfield = None    # use this to look for the next-level key

    def __init__(self, json_record):
        super(
            _field_gnip_pl_base 
            , self).__init__(json_record)
        # self.value is possibly a dict
        if self.value != self.default_value \
                and self.fields is not None \
                and self.subfield is not None \
                and self.subfield in self.value:
            # acscsv._limited_field constructor builds self.value_list
            self.value = self.value_list[0][self.subfield]
            #self.value = self.value[self.subfield] 
        else:
            self.value = self.default_value


class field_gnip_pl_country(_field_gnip_pl_base):
    """Assign to self.value the value of gnip.profileLocations.address.country."""
    fields = ["address"]
    subfield = "country"


class field_gnip_pl_region(_field_gnip_pl_base):
    """Assign to self.value the value of gnip.profileLocations.address.region."""
    fields = ["address"]
    subfield = "region"


class field_gnip_pl_subregion(_field_gnip_pl_base):
    """Assign to self.value the value of gnip.profileLocations.address.subRegion."""
    fields = ["address"]
    subfield = "subRegion"
    

class field_gnip_pl_countrycode(_field_gnip_pl_base):
    """Assign to self.value the value of gnip.profileLocations.address.countryCode."""
    fields = ["address"]
    subfield = "countryCode"


class field_gnip_pl_locality(_field_gnip_pl_base):
    """Assign to self.value the value of gnip.profileLocations.address.locality."""
    fields = ["address"]
    subfield = "locality"


class field_gnip_pl_geo_type(_field_gnip_pl_base):
    """Assign to self.value the value of gnip.profileLocations.geo.type."""
    fields = ["geo"]
    subfield = "type" 


class field_gnip_pl_geo_coords(_field_gnip_pl_base):
    """Assign to self.value the coordinate list in gnip.profileLocations.geo.coordinates."""
    fields = ["geo"]
    subfield = "coordinates"
    
    def __init__(self, json_record):
        super(
            field_gnip_pl_geo_coords 
            , self).__init__(json_record)
        # self.value is possibly a list 
        if self.value == self.default_value:
            self.value_list = self.fix_length( [], limit=2 ) 
        else:
            self.value_list = self.value
        self.value = str( self.value_list ) 


# klout 

class field_gnip_klout_score(acscsv._field):
    """Assign to self.value the value of gnip.klout_score."""
    path = ["gnip", "klout_score"]
    default_value = 0
    
    def __init__(self, json_record):
        super(
            field_gnip_klout_score
            , self).__init__(json_record)
        # self.value is possibly an int
        if self.value != self.default_value:
            self.value = str( self.value )


class field_gnip_klout_user_id(acscsv._field):
    """Assign to self.value the value of gnip.klout_user_id"""
    path = ["gnip", "klout_profile"]
    
    def __init__(self, json_record):
        super(
            field_gnip_klout_user_id 
            , self).__init__(json_record)
        # self.value is possibly a dict of klouty things 
        if self.value != self.default_value and "klout_user_id" in self.value:
            self.value = self.value["klout_user_id"]
    

class field_gnip_klout_topics(acscsv._limited_field):
    """
    Assign to self.value_list (and .value) pairs of gnip.klout_profile.displayName 
    and .klout_topic_id. Up to limit number of these combinations. 
    """
    path = ["gnip", "klout_profile", "topics"]
    fields = ["klout_topic_id", "displayName"]
    
    def __init__(self, json_record, limit=2):
        super(
            field_gnip_klout_topics
            , self).__init__(json_record, limit=limit)
      


########################################
#   'twitter_entities' fields 
########################################

# URLs

class field_twitter_urls_url(acscsv._limited_field):
    """
    """
    path = ["twitter_entities", "urls"]
    fields = ["url"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_urls_url
            , self).__init__(json_record, limit=limit)
 

class field_twitter_urls_expanded_url(acscsv._limited_field):
    """    
    """
    path = ["twitter_entities", "urls"]
    fields = ["expanded_url"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_urls_expanded_url
            , self).__init__(json_record, limit=limit)


class field_twitter_urls_display_url(acscsv._limited_field):
    """
    """
    path = ["twitter_entities", "urls"]
    fields = ["display_url"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_urls_display_url
            , self).__init__(json_record, limit=limit)


class field_twitter_urls_tco_expanded_DB(acscsv._limited_field):
    """
    combination of two classes above
    """
    path = ["twitter_entities", "urls"]
    fields = ["url", "expanded_url"] 

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_urls_tco_expanded_DB 
            , self).__init__(json_record, limit=limit)


# hashtags

class field_twitter_hashtags_text(acscsv._field):
    """
    Assign to self.value a list of twitter_entities.hashtags.text. This class maintains 
    consistency with classic Gnacs behavior.
    """
    path = ["twitter_entities", "hashtags"]

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


class field_twitter_hashtags_text_DB(acscsv._limited_field):
    """
    Combine the first 'limit' hashtags found in the payload into a list and assign to 
    self.value. If there are less than 'limit', the list is padded with 
    self.default_value 
    """
    path = ["twitter_entities", "hashtags"]
    fields = ["text"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_hashtags_text_DB
            , self).__init__(json_record, limit=limit)

# symbols

class field_twitter_symbols_text_DB(acscsv._limited_field):
    """
    Assign to self.value a list of twitter_entities.symbols 'text's.
    This one is a little experimental... haven't seen it in the wild (Activity Streams) yet, 
    so using https://blog.twitter.com/2013/symbols-entities-tweets as the template.
    """
    path = ["twitter_entities", "symbols"]
    fields = ["text"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_symbols_text_DB
            , self).__init__(json_record, limit=limit)

# mentions

class field_twitter_mentions_id_name_DB(acscsv._limited_field):
    """
    Assign to self.value a list of 'limit' twitter_entities.user_mentions.screen_name and .id pairs 
    (in order, but in a flat list).
    """
    path = ["twitter_entities", "user_mentions"]
    fields = ["id", "screen_name"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_mentions_id_name_DB
            , self).__init__(json_record, limit=limit)

# media

class field_twitter_media_id_url_DB(acscsv._limited_field):
    """
    Assign to self.value a list of twitter_entities.media.id and .expanded_url pairs
    """
    path = ["twitter_entities", "media"]
    fields = ["id", "expanded_url"]

    def __init__(self, json_record, limit=5):
        super(
            field_twitter_media_id_url_DB 
            , self).__init__(json_record, limit=limit)
       

########################################
#   'geo' & 'location' fields (related) 
########################################

class field_geo_type(acscsv._field):
    """Assign to self.value the value of geo.type."""
    path = ["geo", "type"]
    

class field_geo_coords(acscsv._field):
    """
    Assign to self.value the value of geo.coordinates. This is the coordinate pair 
    of the user-enabled tweet geotag.
    """
    path = ["geo", "coordinates"]
    
    def __init__(self, json_record):
        super(
            field_geo_coords
            , self).__init__(json_record)
        if self.value == self.default_value:
            #self.value_list = [ self.default_value, self.default_value ]
            self.value_list = self.fix_length([], limit=2) 
        else: 
            self.value_list = self.value
        self.value = str( self.value )


class field_location_type(acscsv._field):
    """Assign to self.value the value of location.geo.type."""
    path = ["location", "geo", "type"]


class field_location_displayname(acscsv._field):
    """Assign to self.value the value of location.displayName"""
    path = ["location", "displayName"]


class field_location_coords(acscsv._field):
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


class field_location_twittercountry(acscsv._field):
    """Assign to self.value the value of location.twitter_country_code."""
    path = ["location", "twitter_country_code"]



########################################
#   other top-level fields 
########################################

class field_inreplyto_link(acscsv._field):
    """Assign to self.value the value of inReplyTo.link"""
    path = ["inReplyTo", "link"]
    

class field_object_id(acscsv._field):
    """Assign to self.value the value of object.id"""
    path = ["object", "id"]
    


class field_object_postedtime(acscsv._field):
    """Assign to self.value the value of object.postedTime"""
    path = ["object", "postedTime"]
    


############################
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
        super(Twacs, self).__init__(delim, options_keypath)
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

    def combine_lists(self, *args):
        """
        Takes an arbitrary number of lists to be combined into a single string for passing back 
        to main gnacs.py and subsequent splitting. The special delimiter for parsing the string 
        back into separate lists is defined in here.
        """
        flag = "GNIPSPLIT"
        #
        # append flag to the end of all but last list
        [ x.append(flag) for i,x in enumerate(args) if i < (len(args) - 1) ]
        # combine the lists into one
        combined_list = []
        [ combined_list.extend(x) for x in args ] 
        #
        # this feels like the right approach, but won't pass through procRecord without
        #   some more effort (JM)
        #return ( combined_list, flag )
        return combined_list

    def csv(self, d, record):
        try:                            # KeyError exception at EOF
            # always first 3 items 
            record.append( field_id(d).value )
            record.append( field_postedtime(d).value )
            record.append( field_body(d).value )
            # begin command line options
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
                record.append( field_gnip_klout_score(d).value )  
                record.append( field_actor_followers(d).value )  
                record.append( field_actor_friends(d).value )  
                record.append( field_actor_listed(d).value )  
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
        Custom output format designed for loading multiple database tables. Creates N separate 
        lists of activity fields, joins them on a GNIPSPLIT to be split at the gnacs.py level 
        and written to separate files.      
        """
        # timestamp format
        t_fmt = "%Y-%m-%d %H:%M:%S"
        now = datetime.utcnow().strftime( t_fmt )

        default_value = acscsv._field({}).default_value

        # hash_list will be [ id, tag1, id, tag2, ... ] and will be split in gnacs.py
        hash_list = [] 
        for i in field_twitter_hashtags_text_DB(d).value_list:
            if i != default_value:      # temporary hack to exclude all the "NULL" values
                hash_list.extend( [ field_id(d).value, i ] ) 

        acs_list = [
                    field_id(d).value 
                    , field_gnip_rules(d).value 
                    , now 
                    , field_postedtime(d).value 
                    , field_verb(d).value 
                    , field_actor_id(d).value 
                    , field_body(d).value 
                    , field_twitter_lang(d).value 
                    , field_gnip_lang(d).value 
                    , field_link(d).value 
                    , field_generator_displayname(d).value 
                    ] \
                    + field_geo_coords(d).value_list \
                    + field_twitter_symbols_text_DB(d).value_list \
                    + field_twitter_mentions_id_name_DB(d).value_list \
                    + field_twitter_urls_tco_expanded_DB(d).value_list \
                    + field_twitter_media_id_url_DB(d).value_list 

        ustatic_list = [
                    now 
                    , field_actor_id(d).value 
                    , field_id(d).value         # needs to be updated programatically in an actual app 
                    , field_actor_postedtime(d).value 
                    , field_actor_preferredusername(d).value 
                    , field_actor_displayname(d).value 
                    , field_actor_acct_link(d).value 
                    , field_actor_summary(d).value 
                    ] \
                    + field_actor_links(d, limit=2).value_list \
                    + [ 
                    field_actor_twittertimezone(d).value 
                    , field_actor_utcoffset_DB(d).value 
                    , field_actor_verified(d).value 
                    , field_actor_lang(d).value 
                    ] \
                    + field_gnip_pl_geo_coords(d).value_list \
                    + [ 
                    field_gnip_pl_countrycode(d).value
                    , field_gnip_pl_locality(d).value
                    , field_gnip_pl_region(d).value
                    , field_gnip_pl_subregion(d).value
                    , field_gnip_pl_displayname(d).value
                    , field_gnip_klout_user_id(d).value
                    ]

        udyn_list = [ 
                    field_actor_id(d).value 
                    , field_id(d).value         # needs to be updated programatically in an actual app 
                    , field_gnip_klout_score(d).value 
                    ] \
                    + field_gnip_klout_topics(d).value_list \
                    + [
                    field_actor_statuses_DB(d).value 
                    , field_actor_followers_DB(d).value  
                    , field_actor_friends_DB(d).value  
                    , field_actor_listed_DB(d).value  
                    ]

        return self.combine_lists(
                    acs_list
                    , ustatic_list
                    , udyn_list
                    , hash_list 
                    )
       

#TODO: possible future extension of ^
#        # this is the acs_list if all twitter entities are stripped out into separate tables
#        acs_list = [
#                    field_id(d).value 
#                    , field_gnip_rules(d).value 
#                    , now 
#                    , field_postedtime(d).value 
#                    , field_verb(d).value 
#                    , field_actor_id(d).value 
#                    , field_body(d).value 
#                    , field_twitter_lang(d).value 
#                    , field_gnip_lang(d).value 
#                    , field_link(d).value 
#                    , field_generator_displayname(d).value 
#                    ] \
#                    + field_geo_coords(d).value_list \
#
#
#        #
#        sym_list = []
#        for i in field_twitter_symbols_text_DB(d).value_list:
#            sym_list.extend( [ field_id(d).value, i ] ) 
#        #
#        # nb: this isn't going to work yet. need to split out the actId, uid, uname triplets
#        mentions_list = []
#        for i in field_twitter_mentions_id_name_DB(d).value_list: 
#            mentions_list.extend( [ field_id(d).value, i ] ) 
#        #
#        urls_list = []
#        media_list = []





    def multi_file_DB_1(self, d, record):
        """
        Custom output format designed for loading multiple database tables.
        Creates 3 separate lists of activity fields, joins them on a GNIPSPLIT to be split 
        at the gnacs.py level and written to separate files.      
    
        Superceded 2014-05-12 for more star-schema approach of e.g. hashtag/mention/link/... tables
        (JM) 
        """
        # timestamp format
        t_fmt = "%Y-%m-%d %H:%M:%S"
        now = datetime.utcnow().strftime( t_fmt )

        # the explicit .value attr reference is needed
        acs_list = [
                    field_id(d).value 
                    , field_gnip_rules(d).value 
                    , now 
                    , field_postedtime(d).value 
                    , field_verb(d).value 
                    , field_actor_id(d).value 
                    , field_body(d).value 
                    , field_twitter_lang(d).value 
                    , field_gnip_lang(d).value 
                    , field_link(d).value 
                    , field_generator_displayname(d).value 
                    ] \
                    + field_geo_coords(d).value_list \
                    + field_twitter_hashtags_text_DB(d).value_list \
                    + field_twitter_symbols_text_DB(d).value_list \
                    + field_twitter_mentions_id_name_DB(d).value_list \
                    + field_twitter_urls_tco_expanded_DB(d).value_list \
                    + field_twitter_media_id_url_DB(d).value_list 

        ustatic_list = [
                    now 
                    , field_actor_id(d).value 
                    , field_id(d).value         # needs to be updated programatically in an actual app 
                    , field_actor_postedtime(d).value 
                    , field_actor_preferredusername(d).value 
                    , field_actor_displayname(d).value 
                    , field_actor_acct_link(d).value 
                    , field_actor_summary(d).value 
                    ] \
                    + field_actor_links(d, limit=2).value_list \
                    + [ 
                    field_actor_twittertimezone(d).value 
                    , field_actor_utcoffset_DB(d).value 
                    , field_actor_verified(d).value 
                    , field_actor_lang(d).value 
                    ] \
                    + field_gnip_pl_geo_coords(d).value_list \
                    + [ 
                    field_gnip_pl_countrycode(d).value
                    , field_gnip_pl_locality(d).value
                    , field_gnip_pl_region(d).value
                    , field_gnip_pl_subregion(d).value
                    , field_gnip_pl_displayname(d).value
                    , field_gnip_klout_user_id(d).value
                    ]

        udyn_list = [ 
                    field_actor_id(d).value 
                    , field_id(d).value         # needs to be updated programatically in an actual app 
                    , field_gnip_klout_score(d).value 
                    ] \
                    + field_gnip_klout_topics(d).value_list \
                    + [
                    field_actor_statuses_DB(d).value 
                    , field_actor_followers_DB(d).value  
                    , field_actor_friends_DB(d).value  
                    , field_actor_listed_DB(d).value  
                    ]
        #
        #TODO: replace with combine_lists() method above
        #
        # consider instead sending the combined list and an arbitrary list of positions to split it
        flag = "GNIPSPLIT"  # this is hardcoded into gnacs.py, as well. change both if needed!
        # only need mortar on first two bricks 
        [ x.append(flag) for x in acs_list, ustatic_list ]
        combined_list = [] 
        combined_list.extend(acs_list)
        combined_list.extend(ustatic_list)
        combined_list.extend(udyn_list)
        #
        return combined_list 


