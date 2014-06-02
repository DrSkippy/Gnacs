# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="Simplified BSD"

import sys
import acscsv   
from datetime import datetime
import re


#TODO: 
#- rename all field_* classes to Field_* ? 
#- add a helper field_found() boolean method to _field.walk_json() for easier
#    construction of checking for default_value (e.g. if self.found(): ... ) 
#   add a custom version of this method for subsequent checking (eg empty list?) 
#- create a more general class for when the value is a list of things (ie check for len = 0 ) ?
#

########################################
#   activity type 
########################################

class field_activity_type(acscsv._field):
    """Take a dict, assign to self.value the appropriate value of Tweet, Retweet, or Reply"""
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
    # 2014-05-29, leave this out for new usage (JM)
    #default_value = "Unidentified meta message"
    

class field_id(acscsv._field):
    """Take a dict, assign to self.value the value in the top-level id key.""" 
    path = ["id"]
    
    def __init__(self, json_record):
        super(
            field_id
            , self).__init__(json_record)
        # self.value is a str beginning w/ tag:search.twitter..... remove all but the actual id 
        self.value = self.value.split(":")[2]


class field_objecttype(acscsv._field):
    """Take a dict, assign to self.value the value in the top-level objectType key.""" 
    path = ["objectType"]
    

class field_postedtime(acscsv._field):
    """
    Take a dict, assign to self.value the value in the top-level postedTime key. Timestamp is 
    formatted according to input_fmt, which is set in the constructor.
    """
    path = ["postedTime"]

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
    

class field_favoritescount(acscsv._field):
    """Take a dict, assign to self.value the value of top-level favoritesCount key."""
    path = ["favoritesCount"]


class field_retweetcount(acscsv._field):
    """Take a dict, assign to self.value the value of top-level retweetCount key."""
    path = ["retweetCount"]


class field_twitter_filter_level(acscsv._field):
    """Take a dict, assign to self.value the value of top-level twitter_filter_level key."""
    path = ["twitter_filter_level"]


class field_inreplyto_link(acscsv._field):
    """
    Take a dict, assign to self.value the value of inReplyTo.link. 
    Should only appear in Replies.
    """
    path = ["inReplyTo", "link"]
    


########################################
#   'provider' fields 
########################################

class field_provider_objecttype(acscsv._field):
    """Take a dict, assign to self.value the value of provider.objectType key."""
    path = ["provider", "objectType"]


class field_provider_displayname(acscsv._field):
    """Take a dict, assign to self.value the value of provider.displayName key."""
    path = ["provider", "displayName"]


class field_provider_link(acscsv._field):
    """Take a dict, assign to self.value the value of provider.link key."""
    path = ["provider", "link"]



########################################
#   'generator' fields 
########################################

class field_generator_displayname(acscsv._field):
    """Take a dict, assign to self.value the value of generator.displayName key."""
    path = ["generator", "displayName"]
    

class field_generator_link(acscsv._field):
    """Take a dict, assign to self.value the value of generator.link key."""
    path = ["generator", "link"]



########################################
#   'gnip' fields 
########################################

class field_gnip_rules(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at gnip.matching_rules"""
    path = ["gnip", "matching_rules"]
    

class field_gnip_urls(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at gnip.urls"""
    path = ["gnip", "urls"]
    

class field_gnip_language_value(acscsv._field):
    """Take a dict, assign to self.value the value of gnip.language.value"""
    path = ["gnip", "language", "value"]


# klout
class field_gnip_klout_score(acscsv._field):
    """Take a dict, assign to self.value the value of gnip.klout_score"""
    path = ["gnip", "klout_score"]
    #default_value = 0


class field_gnip_klout_profile_topics(acscsv._field):
    """Take a dict, assign to self.value the list at gnip.klout_profile.topics"""
    path = ["gnip", "klout_profile", "topics"]
    

class field_gnip_klout_profile_klout_user_id(acscsv._field):
    """Take a dict, assign to self.value the value of gnip.klout_profile.klout_user_id"""
    path = ["gnip", "klout_profile", "klout_user_id"]
    

class field_gnip_klout_profile_link(acscsv._field):
    """Take a dict, assign to self.value the value of gnip.klout_profile.link"""
    path = ["gnip", "klout_profile", "link"]


# profileLocations
class _field_gnip_profilelocations_base(acscsv._field):
    """Take a dict, assign to self.value the dict at gnip.profileLocations[0]""" 
    path = ["gnip", "profileLocations"]

    def __init__(self, json_record):
        super(
            _field_gnip_profilelocations_base 
            , self).__init__(json_record)
        if self.value != self.default_value:
            # if we found the list, we really want the first (only) thing in it
            self.value = self.value[0]


#TODO: if this one-more-level-walk_path() pattern appears often, abstract it to a general method
class field_gnip_profilelocations_displayname(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].displayName."""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_displayname 
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["displayName"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_objecttype(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].objectType"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_objecttype
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["objectType"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_geo_type(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].geo.type"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_geo_type
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["geo", "type"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_geo_coordinates(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].geo.coordinates"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_geo_coordinates
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["geo", "coordinates"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_address_country(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.country"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_address_country
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "country"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_address_countrycode(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.countryCode"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_address_countrycode
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "countryCode"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_address_locality(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.locality"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_address_locality
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "locality"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_address_region(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.region"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_address_region
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "region"] 
            self.walk_path( self.value ) 


class field_gnip_profilelocations_address_subregion(_field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.subRegion"""

    def __init__(self, json_record):
        super(
            field_gnip_profilelocations_address_subregion
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.path = ["address", "subRegion"] 
            self.walk_path( self.value ) 



########################################
#   'actor' fields 
########################################

class field_actor_id(acscsv._field):
    """
    Take a dict, assign to self.value the numerical value of actor.id (after stripping off 
    the leading 'id:twitter...' characters).
    """
    path = ["actor", "id"]
    
    def __init__(self, json_record):
        super(
            field_actor_id
            , self).__init__(json_record)
        if self.value != self.default_value:
            # self.value has an id:twitter....
            self.value = self.value.split(":")[2]


class field_actor_objecttype(acscsv._field):
    """Take a dict, assign to self.value the value of actor.objecttype """
    path = ["actor", "objectType"]
    

class field_actor_postedtime(acscsv._field):
    """Take a dict, assign to self.value the value of actor.postedTime """ 
    path = ["actor", "postedTime"]
    
    def __init__(self, json_record):
        super(
            field_actor_postedtime 
            , self).__init__(json_record)
        # self.value is a string (of a timestamp) 
        input_fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        # default_t_fmt defined in _field constructor
        self.value = datetime.strptime(self.value, input_fmt).strftime(self.default_t_fmt) 


class field_actor_displayname(acscsv._field):
    """Take a dict, assign to self.value the value of actor.displayName """
    path = ["actor", "displayName"]


class field_actor_preferredusername(acscsv._field):
    """Take a dict, assign to self.value the value of actor.preferredUsername"""
    path = ["actor", "preferredUsername"]
 

class field_actor_summary(acscsv._field):
    """Take a dict, assign to self.value the value of actor.summary"""
    path = ["actor", "summary"]


class field_actor_link(acscsv._field):
    """Take a dict, assign to self.value the value of actor.link"""
    path = ["actor", "link"]


class field_actor__image(acscsv._field):
    """Take a dict, assign to self.value the value of actor.image"""
    path = ["actor", "image"]


class field_actor_language(acscsv._field):
    """
    Take a dict, assign to self.value the first (currently only) value in the list at 
    actor.languages
    """
    path = ["actor", "languages"]
    
    def __init__(self, json_record):
        super(
            field_actor_language
            , self).__init__(json_record)
        # self.value is a list, but have only ever seen it with one value, so take that one. 
        if self.value != self.default_value:
            self.value = self.value[0]


class field_actor_links(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at actor.links """
    path = ["actor", "links"]

    def __init__(self, json_record):
        super(
            field_actor_links
            , self).__init__(json_record)
        # should be handled by acscsv._field.walk_json()
#        if self.value != self.default_value and len( self.value ) == 0:
#            # found the list but it's empty -- how often does this happen?
#            self.value = self.default_value


class field_actor_twittertimezone(acscsv._field):
    """Take a dict, assign to self.value the value of actor.twitterTimeZone"""
    path = ["actor", "twitterTimeZone"]


class field_actor_utcoffset(acscsv._field):
    """Take a dict, assign to self.value the value of actor.utcOffset """
    path = ["actor", "utcOffset"]
    

class field_actor_verified(acscsv._field):
    """
    Take a dict, assign to self.value a boolean repr of the value of actor.verified. 
    Default value is False.
    """
    path = ["actor", "verified"]
    default_value = False


class field_actor_location_displayname(acscsv._field):
    """Take a dict, assign to self.value the value of actor.location.displayName"""
    path = ["actor", "location", "displayName"]


class field_actor_location_objecttype(acscsv._field):
    """Take a dict, assign to self.value the value of actor.location.objectType"""
    path = ["actor", "location", "objectType"]


class field_actor_followerscount(acscsv._field):
    """Take a dict, assign to self.value the value of actor.followersCount."""
    path = ["actor", "followersCount"]


class field_actor_friendscount(acscsv._field):
    """Take a dict, assign to self.value the value of actor.friendsCount."""
    path = ["actor", "friendsCount"]

    
class field_actor_listedcount(acscsv._field):
    """Take a dict, assign to self.value the value of actor.listedCount."""
    path = ["actor", "listedCount"]


class field_actor_statusesCount(acscsv._field):
    """Take a dict, assign to self.value the value of actor.statusesCount"""
    path = ["actor", "statusesCount"]


class field_actor_favoritesCount(acscsv._field):
    """Take a dict, assign to self.value the value of actor.favoritesCount"""
    path = ["actor", "favoritesCount"]



########################################
#   'twitter_entities' fields 
########################################

#TODO: refactor these to another acscsv class that does the length check 

# URLs
class field_twitter_entities_urls(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.urls"""
    path = ["twitter_entities", "urls"]

    def __init__(self, json_record):
        super(
            field_twitter_entities_urls 
            , self).__init__(json_record)
#        # self.value is possibly a list of dicts for each activity url 
#        if self.value != self.default_value and len( self.value ) == 0:
#            self.value = self.default_value


# hashtags
class field_twitter_entities_hashtags(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.hashtags"""
    path = ["twitter_entities", "hashtags"]

    def __init__(self, json_record):
        super(
            field_twitter_entities_hashtags 
            , self).__init__(json_record)
#        # self.value is possibly a list of dicts for each activity hashtag 
#        if self.value != self.default_value and len( self.value ) == 0:
#            self.value = self.default_value


# symbols
class field_twitter_entities_symbols(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.symbols"""
    path = ["twitter_entities", "symbols"]

    def __init__(self, json_record):
        super(
            field_twitter_entities_symbols 
            , self).__init__(json_record)
#        # self.value is possibly a list of dicts for each activity symbol 
#        if self.value != self.default_value and len( self.value ) == 0:
#            self.value = self.default_value


# mentions
class field_twitter_entities_user_mentions(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.user_mentions"""
    path = ["twitter_entities", "user_mentions"]

    def __init__(self, json_record):
        super(
            field_twitter_entities_user_mentions 
            , self).__init__(json_record)
#        # self.value is possibly a list of dicts for each activity user_mention 
#        if self.value != self.default_value and len( self.value ) == 0:
#            self.value = self.default_value


# media
class field_twitter_entities_media(acscsv._field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.media"""
    path = ["twitter_entities", "media"]

    def __init__(self, json_record):
        super(
            field_twitter_entities_media 
            , self).__init__(json_record)
#        # self.value is possibly a list of dicts for each activity media 
#        if self.value != self.default_value and len( self.value ) == 0:
#            self.value = self.default_value



########################################
#   'geo' fields 
########################################

class field_geo_type(acscsv._field):
    """Take a dict, assign to self.value the value of geo.type"""
    path = ["geo", "type"]
    

class field_geo_coordinates(acscsv._field):
    """
    Take a dict, assign to self.value the list at geo.coordinates. This is the coordinate pair 
    of the user-enabled tweet geotag.
    """
    path = ["geo", "coordinates"]
   


########################################
#   'location' fields 
########################################

class field_location_displayname(acscsv._field):
    """Take a dict, assign to self.value the value of location.displayName"""
    path = ["location", "displayName"]


class field_location_name(acscsv._field):
    """Take a dict, assign to self.value the value of location.name"""
    path = ["location", "name"]


class field_location_objecttype(acscsv._field):
    """Take a dict, assign to self.value the value of location.objectType"""
    path = ["location", "objectType"]


class field_location_twitter_country_code(acscsv._field):
    """Take a dict, assign to self.value the value of location.twitter_country_code."""
    path = ["location", "twitter_country_code"]


class field_location_country_code(acscsv._field):
    """Take a dict, assign to self.value the value of location.country_code."""
    path = ["location", "country_code"]


class field_location_link(acscsv._field):
    """Take a dict, assign to self.value the value of location.link."""
    path = ["location", "link"]


# location.geo
class field_location_geo_type(acscsv._field):
    """Take a dict, assign to self.value the value of location.geo.type."""
    path = ["location", "geo", "type"]


class field_location_geo_coordinates(acscsv._field):
    """
    Take a dict, assign to self.value the list of coord pairs (vertices) in the value 
    of location.geo.coordinates.
    """
    path = ["location", "geo", "coordinates"]




########################################
#   'object' fields 
########################################

# these fields appear to be redundant with the fields already defined 




