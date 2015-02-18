# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague"
__license__="Simplified BSD"

import sys
import acscsv
from twitter_acs_fields import *

class TwacsCSV(acscsv.AcsCSV):
    """Subset of Twitter fields with specified delimiter.  Please see help for options"""

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
                ):
        super(TwacsCSV, self).__init__(delim, options_keypath)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_lang = options_lang
        self.options_influence = options_influence
        self.options_struct = options_struct
        # pre-create all of teh objects needed for parsing
        #for name, obj in inspect.getmembers(sys.modules[__name__]):
        #    if name.startswith("Field_"):
        #        setattr(self, name.lower()+"_", obj(None))

    def procRecordToList(self, d):
        """
        Take a JSON Activity Streams payload as a Python dictionary. Check activity for system 
        information and compliance handling. If necessary, return the system info or compliance 
        message. Otherwise, if the activity is valid, return the result of calling the 
        appropriate output() method.  
        """
        record = []
        try:
            verb = Field_verb(d).value
            # see: http://support.gnip.com/apis/consuming_streaming_data.html#Consuming 
            system_msgs = ["error", "warning", "info"]
            if verb in system_msgs: 
                msg = "Unidentified meta message"
                for mtype in system_msgs:
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
            elif verb == "delete":
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

        # at this point, verb is an acceptable record 
        return self.get_output_list(d) 


    def get_output_list(self, d):
        """
        Take a JSON Activity Streams payload as a Python dictionary. Specify the particular 
        output fields (and their order) by constructing and returning a list of the 
        desired extractor values. Default values for missing fields are set in the _Field class 
        and can be overridden.  
        """
        output_list = [] 

        # base output = id | timestamp | body
        output_list.append( Field_id(d).value )
        output_list.append( Field_postedtime(d).value )
        output_list.append( Field_body(d).value )

        # urls 
        if self.options_urls:
            #
            # TODO: add back this exception handling for -x option
            # https://github.com/DrSkippy/Gnacs/blob/16dd146fb05d02d7c1e3f282254e6718fd13303f/acscsv/twacscsv.py#L97 
            #
            # gnip 
            val = Field_gnip_urls(d).value
            if isinstance(val, list): 
                try:
                    output_list.append( self.buildListString( [ x["expanded_url"] for x in val ] ) )   
                except KeyError:
                    output_list.append(Field_gnip_urls(d).default_value)
            else: 
                output_list.append( val )  
            # twitter
            val = Field_twitter_entities_urls(d).value  
            if isinstance(val, list):
                url_list = self.buildListString( [ x["url"] for x in val ] ) 
                exp_url_list = self.buildListString( [ x["expanded_url"] for x in val ] ) 
            else:
                url_list = val
                exp_url_list = val 
            output_list.append( url_list )  
            output_list.append( exp_url_list )  
    
        # languages 
        if self.options_lang:
            # actor
            #   - this field has *very* infrequently contained unicode chars. drop them.
            output_list.append( Field_actor_language(d).value.encode('ascii', 'ignore') ) 
            # classifications
            output_list.append( Field_gnip_language_value(d).value ) 
            output_list.append( Field_twitter_lang(d).value ) 
    
        # rules
        if self.options_rules:
            val = Field_gnip_rules(d).value 
            if isinstance(val, list):
                # output: '[" value (tag)", ... ]'
                output_list.append( 
                    self.buildListString( 
                        [ "{} ({})".format( x["value"], x["tag"] ) for x in Field_gnip_rules(d).value ]
                        )
                    ) 
            else: 
                output_list.append( val )  

        # geo-related fields
        if self.options_geo:
            # geo-tag 
            val = Field_geo_coordinates(d).value
            # keep self.geoCoordsList for backward compatibility
            self.geoCoordsList = None
            if isinstance(val, list):
                output_list.append( str(val) ) 
                self.geoCoordsList = val 
            else:
                output_list.append( val ) 
            output_list.append( Field_geo_type(d).value )
            val = Field_location_geo_coordinates(d).value 
            if isinstance(val, list): 
                output_list.append( str(val) )  
            else:
                output_list.append( val )  
            output_list.append( Field_location_geo_type(d).value )
            output_list.append( Field_location_displayname(d).value )  
            output_list.append( Field_location_twitter_country_code(d).value )  
            # user  
            output_list.append( Field_actor_utcoffset(d).value )  
            output_list.append( Field_actor_location_displayname(d).value )  
            # profileLocations
            output_list.append( Field_gnip_profilelocations_displayname(d).value )  
            output_list.append( Field_gnip_profilelocations_objecttype(d).value )  
            output_list.append( Field_gnip_profilelocations_address_country(d).value )  
            output_list.append( Field_gnip_profilelocations_address_region(d).value )  
            output_list.append( Field_gnip_profilelocations_address_countrycode(d).value )  
            output_list.append( Field_gnip_profilelocations_address_locality(d).value )  
            output_list.append( Field_gnip_profilelocations_geo_type(d).value )  
            output_list.append( Field_gnip_profilelocations_geo_coordinates(d).value )  

        # user
        if self.options_user:
            output_list.append( Field_actor_displayname(d).value )  
            output_list.append( Field_actor_preferredusername(d).value )  
            output_list.append( Field_actor_id(d).value )  
            
        # user connections, klout
        if self.options_influence:
            output_list.append( Field_gnip_klout_score(d).value )  
            output_list.append( Field_actor_followerscount(d).value )  
            output_list.append( Field_actor_friendscount(d).value )  
            output_list.append( Field_actor_listedcount(d).value )  
            output_list.append( Field_actor_statusesCount(d).value )  
             
        # structure
        if self.options_struct:
            output_list.append( Field_activity_type(d).value )  

        # done building output list 
        return output_list 

