# -*- coding: UTF-8 -*-
__author__="Josh Montague, Scott Hendrickson"
__license__="Simplified BSD"

import sys
import acscsv
from snowflake import *
from datetime import datetime
import re


########################################
#   activity type 
########################################

class Field_activity_type(acscsv._Field):
    """
    Take a dict, assign to self.value the appropriate value of Tweet, Retweet, or Reply. This 
    class is being held onto for now, but may not be needed in future.
    """
    label = 'Activity Type'
    path = []
    
    def __init__(self, json_record):
        super(
            Field_activity_type
            , self).__init__(json_record)
        # self.value is None
        if json_record is not None:
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
    label = 'Verb'
    path = ['verb']
    # overwrite this default value because records missing this field should be called out (badness) 
    # 2014-05-29, leave this out for new usage (JM)
    #default_value = "Unidentified meta message"
    

class Field_id(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level id key.""" 
    label = 'Tweet ID'
    path = ['id']
    
    def __init__(self, json_record):
        super(
            Field_id
            , self).__init__(json_record)
        tmp = self.value.split(":")
        if len(tmp) >= 3:
            self.value = tmp[2]

class Field_snowflake(Field_id):
    def __init__(self, json_record):
        super(
            Field_snowflake
            , self).__init__(json_record)
        sf = Snowflake(self.value)
        self.value = "_".join([str(sf.id), sf.timeString, str(sf.sample_set)])


class Field_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level objectType key.""" 
    label = 'objectType' 
    path = ['objectType']
    

class Field_object(acscsv._Field):
    """Take a dict, assign to self.value the value in the top-level object key.""" 
    label = 'Object'
    path = ['object']


class Field_postedtime(acscsv._Field):
    """
    Take a dict, assign to self.value the value in the top-level postedTime key. Timestamp is 
    formatted according to input_fmt, which is set in the constructor.
    """
    label = 'Posted Time'
    path = ['postedTime']

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
    label = 'Body'
    path = ['body']
    

class Field_link(acscsv._Field):
    """Take a dict, assign to self.value the value in top-level link key."""
    label = 'Activity URL'
    path = ['link']
    

class Field_twitter_lang(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level twitter_lang key."""
    label = 'Twitter-Inferred Activity Language'
    path = ['twitter_lang']
    

class Field_favoritescount(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level favoritesCount key."""
    label = 'Favorite Count'
    path = ['favoritesCount']


class Field_retweetcount(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level retweetCount key."""
    label = 'Retweet Count'
    path = ['retweetCount']


class Field_twitter_filter_level(acscsv._Field):
    """Take a dict, assign to self.value the value of top-level twitter_filter_level key."""
    label = 'Twitter Filter Level'
    path = ['twitter_filter_level']


class Field_inreplyto_link(acscsv._Field):
    """
    Take a dict, assign to self.value the value of inReplyTo.link. 
    Should only appear in Replies.
    """
    label = 'In-Reply-To URL'
    path = ['inReplyTo', 'link']
    


########################################
#   'provider' fields 
########################################

class Field_provider_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of provider.objectType key."""
    label = 'Provider Object Type'
    path = ['provider', 'objectType']


class Field_provider_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of provider.displayName key."""
    label = 'Provider Name'
    path = ['provider', 'displayName']


class Field_provider_link(acscsv._Field):
    """Take a dict, assign to self.value the value of provider.link key."""
    label = 'Provider Link'
    path = ['provider', 'link']



########################################
#   'generator' fields 
########################################

class Field_generator_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of generator.displayName key."""
    label = 'Generator Name'
    path = ['generator', 'displayName']
    

class Field_generator_link(acscsv._Field):
    """Take a dict, assign to self.value the value of generator.link key."""
    label = 'Generator Link'
    path = ['generator', 'link']



########################################
#   'gnip' fields 
########################################

class Field_gnip_rules(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at gnip.matching_rules"""
    label = 'Matching PT Rules'
    path = ['gnip', 'matching_rules']
    

class Field_gnip_urls(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at gnip.urls"""
    label = 'List of URLs (Gnip)'
    path = ['gnip', 'urls']

# TODO: extractors that use Field_gnip_urls to get both the shortened & unwound URLs
    

class Field_gnip_language_value(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.language.value"""
    label = 'Gnip-Inferred Activity Language'
    path = ['gnip', 'language', 'value']


# klout
class Field_gnip_klout_score(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.klout_score"""
    label = 'User Klout Score'
    path = ['gnip', 'klout_score']


class Field_gnip_klout_profile_topics(acscsv._Field):
    """Take a dict, assign to self.value the list at gnip.klout_profile.topics"""
    label = 'User Klout Topics'
    path = ['gnip', 'klout_profile', 'topics']
    

class Field_gnip_klout_profile_klout_user_id(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.klout_profile.klout_user_id"""
    label = 'User Klout ID'
    path = ['gnip', 'klout_profile', 'klout_user_id']
    

class Field_gnip_klout_profile_link(acscsv._Field):
    """Take a dict, assign to self.value the value of gnip.klout_profile.link"""
    label = 'User Klout Profile Link'
    path = ['gnip', 'klout_profile', 'link']


# profileLocations
class _Field_gnip_profilelocations_base(acscsv._Field):
    """
    Take a dict, assign to self.value the dict at gnip.profileLocations[0]. This class 
    serves as the base for subfields of profileLocations.
    """ 
    label = 'Profile Geo: Data Structure'
    path = ['gnip', 'profileLocations']

    def __init__(self, json_record):
        super(
            _Field_gnip_profilelocations_base 
            , self).__init__(json_record)
        if self.value != self.default_value:
            # if we found the list, we really want the first (only) thing in it
            self.value = self.value[0]


class Field_gnip_profilelocations_displayname(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].displayName."""
    label = 'Profile Geo: Name'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_displayname 
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['displayName'] ) 


class Field_gnip_profilelocations_objecttype(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].objectType"""
    label = 'Profile Geo: Object Type'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_objecttype
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['objectType'] ) 


class Field_gnip_profilelocations_geo_type(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].geo.type"""
    label = 'Profile Geo: Type'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_geo_type
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['geo', 'type'] ) 


class Field_gnip_profilelocations_geo_coordinates(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].geo.coordinates"""
    label = 'Profile Geo: Coordinates'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_geo_coordinates
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['geo', 'coordinates'] ) 


class Field_gnip_profilelocations_address_country(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.country"""
    label = 'Profile Geo: Country'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_country
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['address', 'country'] ) 


class Field_gnip_profilelocations_address_countrycode(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.countryCode"""
    label = 'Profile Geo: Country Code'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_countrycode
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['address', 'countryCode'] ) 


class Field_gnip_profilelocations_address_locality(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.locality"""
    label = 'Profile Geo: Locality'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_locality
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['address', 'locality'] ) 


class Field_gnip_profilelocations_address_region(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.region"""
    label = 'Profile Geo: Region'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_region
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['address', 'region'] ) 


class Field_gnip_profilelocations_address_subregion(_Field_gnip_profilelocations_base):
    """Take a dict, assign to self.value the value of gnip.profileLocations[0].address.subRegion"""
    label = 'Profile Geo: Subregion'

    def __init__(self, json_record):
        super(
            Field_gnip_profilelocations_address_subregion
            , self).__init__(json_record)
        if self.value != self.default_value:
            self.value = self.walk_path( self.value, path = ['address', 'subRegion'] ) 



########################################
#   'actor' fields 
########################################

class Field_actor_id(acscsv._Field):
    """
    Take a dict, assign to self.value the numerical value of actor.id (after stripping off 
    the leading 'id:twitter...' characters).
    """
    label = 'User ID'
    path = ['actor', 'id']
    
    def __init__(self, json_record):
        super(
            Field_actor_id
            , self).__init__(json_record)
        if self.value != self.default_value:
            # self.value has an id:twitter....
            self.value = self.value.split(":")[2]


class Field_actor_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.objecttype """
    label = 'User Object Type'
    path = ['actor', 'objectType']
    

class Field_actor_postedtime(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.postedTime """ 
    label = 'User Account Creation Date'
    path = ['actor', 'postedTime']
    
    def __init__(self, json_record):
        super(
            Field_actor_postedtime 
            , self).__init__(json_record)
        # self.value is a string (of a timestamp) 
        input_fmt = "%Y-%m-%dT%H:%M:%S.000Z"
        try:
            # default_t_fmt defined in _Field constructor
            self.value = datetime.strptime(self.value, input_fmt).strftime(self.default_t_fmt) 
        except ValueError:
            self.value = "INVALID_DATE_FORMAT"


class Field_actor_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.displayName """
    label = 'User Display Name'
    path = ['actor', 'displayName']


class Field_actor_preferredusername(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.preferredUsername"""
    label = 'User Account Name'
    path = ['actor', 'preferredUsername']
 

class Field_actor_summary(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.summary"""
    label = 'User Bio'
    path = ['actor', 'summary']


class Field_actor_link(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.link"""
    label = 'User Account URL'
    path = ['actor', 'link']


class Field_actor_image(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.image"""
    label = 'User Account Image'
    path = ['actor', 'image']


class Field_actor_language(acscsv._Field):
    """
    Take a dict, assign to self.value the first (currently only) value in the list at 
    actor.languages
    """
    label = 'User-chosen Language'
    path = ['actor', 'languages']
    
    def __init__(self, json_record):
        super(
            Field_actor_language
            , self).__init__(json_record)
        # self.value is a list, but have only ever seen it with one value, so take that one. 
        if self.value != self.default_value:
            self.value = self.value[0]


class Field_actor_links(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at actor.links """
    label = 'User Account Bio URLs'
    path = ['actor', 'links']

    def __init__(self, json_record):
        super(
            Field_actor_links
            , self).__init__(json_record)


class Field_actor_twittertimezone(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.twitterTimeZone"""
    label = 'User-chosen Timezone'
    path = ['actor', 'twitterTimeZone']


class Field_actor_utcoffset(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.utcOffset """
    label = 'User-chosen Offset From UTC'
    path = ['actor', 'utcOffset']
    

class Field_actor_verified(acscsv._Field):
    """
    Take a dict, assign to self.value a boolean repr of the value of actor.verified. 
    Default value is False.
    """
    label = 'Actor Verified'
    path = ['actor', 'verified']
    default_value = False


class Field_actor_location_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.location.displayName"""
    label = 'User-chosen Location Name'
    path = ['actor', 'location', 'displayName']


class Field_actor_location_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.location.objectType"""
    label = 'User-chosen Location Type'
    path = ['actor', 'location', 'objectType']


class Field_actor_followerscount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.followersCount."""
    label = 'User Follower Count'
    path = ['actor', 'followersCount']


class Field_actor_friendscount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.friendsCount."""
    label = 'User Following Count'
    path = ['actor', 'friendsCount']

    
class Field_actor_listedcount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.listedCount."""
    label = 'User Listed Count'
    path = ['actor', 'listedCount']


class Field_actor_statusesCount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.statusesCount"""
    label = 'User Statuses Count'
    path = ['actor', 'statusesCount']


class Field_actor_favoritesCount(acscsv._Field):
    """Take a dict, assign to self.value the value of actor.favoritesCount"""
    label = 'User Favorites Count'
    path = ['actor', 'favoritesCount']



########################################
#   'twitter_entities' fields 
########################################

# URLs
class Field_twitter_entities_urls(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.urls"""
    label = 'List of URLs (Twitter)'
    path = ['twitter_entities', 'urls']


# hashtags
class Field_twitter_entities_hashtags(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.hashtags"""
    label = 'List of Hashtags (Twitter)'
    path = ['twitter_entities', 'hashtags']


# symbols
class Field_twitter_entities_symbols(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.symbols"""
    label = 'List of Symbols (Twitter)'
    path = ['twitter_entities', 'symbols']


# mentions
class Field_twitter_entities_user_mentions(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.user_mentions"""
    label = 'List of Mentions (Twitter)'
    path = ['twitter_entities', 'user_mentions']


# media
class Field_twitter_entities_media(acscsv._Field):
    """Take a dict, assign to self.value the list of dicts at twitter_entities.media"""
    label = 'List of Media (Twitter)'
    path = ['twitter_entities', 'media']



########################################
#   'geo' fields 
########################################

class Field_geo_type(acscsv._Field):
    """Take a dict, assign to self.value the value of geo.type"""
    label = 'Geo-tag: Type'
    path = ['geo', 'type']
    

class Field_geo_coordinates(acscsv._Field):
    """
    Take a dict, assign to self.value the list at geo.coordinates. This is the coordinate pair 
    of the user-enabled tweet geotag.
    """
    label = 'Geo-tag: Coordinates'
    path = ['geo', 'coordinates']
   


########################################
#   'location' fields 
########################################

class Field_location_displayname(acscsv._Field):
    """Take a dict, assign to self.value the value of location.displayName"""
    label = 'Geo-tag: Full Name'
    path = ['location', 'displayName']


class Field_location_name(acscsv._Field):
    """Take a dict, assign to self.value the value of location.name"""
    label = 'Geo-tag: Short Name'
    path = ['location', 'name']


class Field_location_objecttype(acscsv._Field):
    """Take a dict, assign to self.value the value of location.objectType"""
    label = 'Geo-tag: Location Type'
    path = ['location', 'objectType']


class Field_location_twitter_country_code(acscsv._Field):
    """Take a dict, assign to self.value the value of location.twitter_country_code."""
    label = 'Geo-tag: Country Code'
    path = ['location', 'twitter_country_code']


class Field_location_country_code(acscsv._Field):
    """Take a dict, assign to self.value the value of location.country_code."""
    label = 'Geo-tag: Country'
    path = ['location', 'country_code']


class Field_location_link(acscsv._Field):
    """Take a dict, assign to self.value the value of location.link."""
    label = 'Geo-tag: Place URL'
    path = ['location', 'link']


# location.geo
class Field_location_geo_type(acscsv._Field):
    """Take a dict, assign to self.value the value of location.geo.type."""
    label = 'Geo-tag: Place Type'
    path = ['location', 'geo', 'type']


class Field_location_geo_coordinates(acscsv._Field):
    """
    Take a dict, assign to self.value the list of coord pairs (vertices) in the value 
    of location.geo.coordinates.
    """
    label = 'Geo-tag: Place Coordinates'
    path = ['location', 'geo', 'coordinates']

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

