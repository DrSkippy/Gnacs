# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="Simplified BSD"

import sys
import acscsv
from twacs_fields import *
import twacscsv     # this is the class whose output we're overwriting
from datetime import datetime
import re

# this needs to inherit from e.g twacscsv (but from the "fixed" version)
class TestClass(acscsv.AcsCSV):
    def __init__(self
            # add more as needed
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
        super(TestClass, self).__init__(delim, options_keypath)
        self.options_geo = options_geo 
        self.options_user = options_user
        self.options_rules = options_rules
        self.options_urls = options_urls
        self.options_lang = options_lang
        self.options_influence = options_influence
        self.options_struct = options_struct
        self.options_db = options_db


    def combine_lists(self, *args):
        """
        Takes an arbitrary number of lists to be combined into a single string for passing back 
        to main gnacs.py and subsequent splitting. The special delimiter for parsing the string 
        back into separate lists is defined in here.
        """
        flag = "GNIPSPLIT"
        
        # append flag to the end of all but last list
        [ x.append(flag) for i,x in enumerate(args) if i < (len(args) - 1) ]
        # combine the lists into one
        combined_list = []
        [ combined_list.extend(x) for x in args ] 
        
        return combined_list

        
    def procRecordToList(self, d):
        """
        Takes JSON payload d (as a dictionary), executes any needed pre-processing code on 
        the record, and then calls the csv parser. 
        """ 
        record = []

        # to start, gut this method. add functionality as needed.
        return self.csv(d, record)


    def csv(self, d, record):
        """
        Extracts desired fields (using classes defined in e.g. twacs_fields.py) and determines 
        output order. For consistency with gnacs.py module, the result is returned as a list
        and split (if needed) in the main gnacs module. 
        """
        # timestamp format
        t_fmt = "%Y-%m-%d %H:%M:%S"

        now = datetime.utcnow().strftime( t_fmt )

        rec_list = [
                    field_id(d).value 
                    , field_gnip_rules(d).value 
                    , now 
                    ]
         
        return rec_list 



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
       
if __name__ == "__main__":
    # $ cat data | ./test_module.py 
    # <correct output>




