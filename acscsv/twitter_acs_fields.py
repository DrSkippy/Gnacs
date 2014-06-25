# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="Simplified BSD"

import sys
import acscsv   
from datetime import datetime
import re


#TODO: 
#- rename all Field_* classes to Field_* ? 
#- add a helper Field_found() boolean method to _Field.walk_json() for easier
#    construction of checking for default_value (e.g. if self.found(): ... ) 
#   add a custom version of this method for subsequent checking (eg empty list?) 
#

########################################
#   activity type 
########################################

class Field_activity_type(acscsv._Field):
    """
    Take a dict, assign to self.value the appropriate value of Tweet, Retweet, or Reply. This 
    class is being held onto for now, but may not be needed in future."""
    path = []
    
    def __init__(self, json_record):
        super(
            Field_activity_type
            , self).__init__(json_record)
        # self.value is None
        verb = Field_verb(json_record).value 
        rec_id = Field_id(json_record).value  
        inReplyTo = "None"
        obj_objtype = "None"
        if "inReplyTo" in json_record:
            # get the url
            inReplyTo = json_record["inReplyTo"]["link"]
            # get the original id from the url
            rec_id = inReplyTo.split("/")[-1]
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
        # tack on the upstream activity id (or this id, for Tweets)  
        self.value += " ({})".format(rec_id)



########################################
#   top-level fields 
########################################

class Field_verb(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level verb key.""" 
    path = ["verb"]
    # overwrite this default value because records missing this field should be called out (badness) 
    # 2014-05-29, leave this out for new usage (JM)
    #default_value = "Unidentified meta message"
    

class Field_id(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level id key.""" 
    path = ["id"]
    
    def __init__(self, json_record):
        super(
            Field_id
            , self).__init__(json_record)
        # self.value is a str beginning w/ tag:search.twitter..... remove all but the actual id 
        self.value = self.value.split(":")[2]


class Field_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level objectType key.""" 
    path = ["objectType"]
    

class Field_object(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level object key.""" 
    path = ["object"]


class Field_postedtime(acscsv._Field):
    """
    Take a dict, assign to self.value the value in the top-level postedTime key. Timestamp is 
    formatted according to input_fmt, which is set in the constructor.
    """
    path = ["postedTime"]

    # keep this around for possible regex+uniform output extension
#    def __init__(self, json_record):
#        super(
#            Field_postedtime 
#            , self).__init__(json_record)
#        # self.value is a datetime string 
#        input_fmt = "%Y-%m-%dT%H:%M:%S.000Z"
#        # add a regex match on the input to have consistent output across all input streams? 
#        self.value = datetime.strptime( 
#                        self.value, input_fmt 
#                        ).strftime( 
#                            self.default_t_fmt ) 


class Field_body(acscsv._Field):
    """Take a dict, assign to self.value the value in top-level body key."""
    path = ["body"]
    

class Field_link(acscsv._Field):
    """Take a dict, assign to self.value the value in top-level link key."""
    path = ["link"]
    

class Field_twitter_lang(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level twitter_lang key."""
    path = ["twitter_lang"]
    

class Field_favoritescount(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level favoritesCount key."""
    path = ["favoritesCount"]


class Field_retweetcount(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level retweetCount key."""
    path = ["retweetCount"]


class Field_twitter_filter_level(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level twitter_filter_level key."""
    path = ["twitter_filter_level"]


class Field_inreplyto_link(acscsv._Field):
    """
    Take a dict, assign to self.value the value of inReplyTo.link. 
    Should only appear in Replies.
    """
    path = ["inReplyTo", "link"]
    


########################################
#   'provider' fields 
########################################

class Field_provider_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of provider.objectType key."""
    path = ["provider", "objectType"]


class Field_provider_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of provider.displayName key."""
    path = ["provider", "displayName"]


class Field_provider_link(acscsv._Field):
    """Take a dict, assign to self.value the value of provider.link key."""
    path = ["provider", "link"]



########################################
#   'generator' fields 
########################################

class Field_generator_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of generator.displayName key."""
    path = ["generator", "displayName"]
    

class Field_generator_link(acscsv._Field):
    """Take a dict, assign to self.value the value of generator.link key."""
    path = ["generator", "link"]



########################################
#   'gnip' fields 
########################################

class Field_gnip_rules(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at gnip.matching_rules"""
    path = ["gnip", "matching_rules"]
    

class Field_gnip_urls(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at gnip.urls"""
    path = ["gnip", "urls"]
    

class Field_gnip_language_value(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.language.value"""
    path = ["gnip", "language", "value"]


# klout
class Field_gnip_klout_score(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.klout_score"""
    path = ["gnip", "klout_score"]
    #default_value = 0


class Field_gnip_klout_profile_topics(acscsv._Field):
    """Take a dict, assign to self.value the list at gnip.klout_profile.topics"""
    path = ["gnip", "klout_profile", "topics"]
    

class Field_gnip_klout_profile_klout_user_id(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.klout_profile.klout_user_id"""
    path = ["gnip", "klout_profile", "klout_user_id"]
    

class Field_gnip_klout_profile_link(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.klout_profile.link"""
    path = ["gnip", "klout_profile", "link"]


# profileLocations
class _Field_gnip_profilelocations_base(acscsv._Field):
    """
    Take a dict, assign to self.value the dict at gnip.profileLocations[0]. This class 
    serves as the base for subfields of profileLocations.
    """ 
    path = ["gnip", "profileLocations"]

    def __init__(self, json_record):
        super(
            _Field_gnip_profilelocations_base 
            , self).__init__(json_record)
        if self.value != self.default_value:
            # if we found the list, we really want the first (only) thing in it
            self.value = self.value[0]


class Field_gnip_profilelocations_displayname(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].displayName."""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_displayname 
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["displayName"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_objecttype(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].objectType"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_objecttype
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["objectType"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_geo_type(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].geo.type"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_geo_type
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["geo", "type"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_geo_coordinates(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].geo.coordinates"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_geo_coordinates
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["geo", "coordinates"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_address_country(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.country"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_country
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "country"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_address_countrycode(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.countryCode"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_countrycode
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "countryCode"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_address_locality(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.locality"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_locality
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "locality"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_address_region(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.region"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_region
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "region"] 
            self.value = self.walk_path( self.value ) 


class Field_gnip_profilelocations_address_subregion(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.subRegion"""

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_subregion
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "subRegion"] 
            self.value = self.walk_path( self.value ) 



########################################
#   'actor' fields 
########################################

class Field_actor_id(acscsv._Field):
    """
    Take a dict, assign to self.value the numerical value of actor.id (after stripping off 
    the leading 'id:twitter...' characters).
    """
    path = ["actor", "id"]
    
    def __init__(self, json_record):
        super(
            Field_actor_id
            , self).__init__(json_record)
        if self.value != self.default_value:
            # self.value has an id:twitter....
            self.value = self.value.split(":")[2]


class Field_actor_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.objecttype """
    path = ["actor", "objectType"]
    

class Field_actor_postedtime(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.postedTime """ 
    path = ["actor", "postedTime"]
    
    def __init__(self, json_record):
        super(
            Field_actor_postedtime 
            , self).__init__(json_record)
        # self.value is a string (of a timestamp) 
        input_fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        # default_t_fmt defined in _Field constructor
        self.value = datetime.strptime(self.value, input_fmt).strftime(self.default_t_fmt) 


class Field_actor_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.displayName """
    path = ["actor", "displayName"]


class Field_actor_preferredusername(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.preferredUsername"""
    path = ["actor", "preferredUsername"]
 

class Field_actor_summary(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.summary"""
    path = ["actor", "summary"]


class Field_actor_link(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.link"""
    path = ["actor", "link"]


class Field_actor_image(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.image"""
    path = ["actor", "image"]


class Field_actor_language(acscsv._Field):
    """
    Take a dict, assign to self.value the first (currently only) value in the list at 
    actor.languages
    """
    path = ["actor", "languages"]
    
    def __init__(self, json_record):
        super(
            Field_actor_language
            , self).__init__(json_record)
        # self.value is a list, but have only ever seen it with one value, so take that one. 
        if self.value != self.default_value:
            self.value = self.value[0]


class Field_actor_links(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at actor.links """
    path = ["actor", "links"]

    def __init__(self, json_record):
        super(
            Field_actor_links
            , self).__init__(json_record)
        # should be handled by acscsv._Field.walk_json()
#        if self.value != self.default_value and len( self.value ) == 0:
#            # found the list but it's empty -- how often does this happen?
#            self.value = self.default_value


class Field_actor_twittertimezone(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.twitterTimeZone"""
    path = ["actor", "twitterTimeZone"]


class Field_actor_utcoffset(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.utcOffset """
    path = ["actor", "utcOffset"]
    

class Field_actor_verified(acscsv._Field):
    """
    Take a dict, assign to self.value a boolean repr of the value of actor.verified. 
    Default value is False.
    """
    path = ["actor", "verified"]
    default_value = False


class Field_actor_location_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.location.displayName"""
    path = ["actor", "location", "displayName"]


class Field_actor_location_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.location.objectType"""
    path = ["actor", "location", "objectType"]


class Field_actor_followerscount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.followersCount."""
    path = ["actor", "followersCount"]


class Field_actor_friendscount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.friendsCount."""
    path = ["actor", "friendsCount"]

    
class Field_actor_listedcount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.listedCount."""
    path = ["actor", "listedCount"]


class Field_actor_statusesCount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.statusesCount"""
    path = ["actor", "statusesCount"]


class Field_actor_favoritesCount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.favoritesCount"""
    path = ["actor", "favoritesCount"]



########################################
#   'twitter_entities' fields 
########################################

#TODO: refactor these to another acscsv class that does the length check 

# URLs
class Field_twitter_entities_urls(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.urls"""
    path = ["twitter_entities", "urls"]


# hashtags
class Field_twitter_entities_hashtags(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.hashtags"""
    path = ["twitter_entities", "hashtags"]


# symbols
class Field_twitter_entities_symbols(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.symbols"""
    path = ["twitter_entities", "symbols"]


# mentions
class Field_twitter_entities_user_mentions(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.user_mentions"""
    path = ["twitter_entities", "user_mentions"]


# media
class Field_twitter_entities_media(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.media"""
    path = ["twitter_entities", "media"]



########################################
#   'geo' fields 
########################################

class Field_geo_type(acscsv._Field):
    """Take a dict, assign to self.value the value of geo.type"""
    path = ["geo", "type"]
    

class Field_geo_coordinates(acscsv._Field):
    """
    Take a dict, assign to self.value the list at geo.coordinates. This is the coordinate pair 
    of the user-enabled tweet geotag.
    """
    path = ["geo", "coordinates"]
   


########################################
#   'location' fields 
########################################

class Field_location_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of location.displayName"""
    path = ["location", "displayName"]


class Field_location_name(acscsv._Field):
    """Take a dict, assign to self.value the value of location.name"""
    path = ["location", "name"]


class Field_location_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of location.objectType"""
    path = ["location", "objectType"]


class Field_location_twitter_country_code(acscsv._Field):
    """Take a dict, assign to self.value the value of location.twitter_country_code."""
    path = ["location", "twitter_country_code"]


class Field_location_country_code(acscsv._Field):
    """Take a dict, assign to self.value the value of location.country_code."""
    path = ["location", "country_code"]


class Field_location_link(acscsv._Field):
    """Take a dict, assign to self.value the value of location.link."""
    path = ["location", "link"]


# location.geo
class Field_location_geo_type(acscsv._Field):
    """Take a dict, assign to self.value the value of location.geo.type."""
    path = ["location", "geo", "type"]


class Field_location_geo_coordinates(acscsv._Field):
    """
    Take a dict, assign to self.value the list of coord pairs (vertices) in the value 
    of location.geo.coordinates.
    """
    path = ["location", "geo", "coordinates"]

    def __init__(self, json_record):
        super(
            Field_location_geo_coordinates 
            , self).__init__(json_record)
        # this list has only been observed to contain another list of the bounding vertices 
        if self.value != self.default_value:
            self.value = self.value[0]



########################################
#   'object' fields 
########################################

# these fields appear to be redundant with the fields already defined 




