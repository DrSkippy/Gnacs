#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="Simplified BSD"

import sys
import json
import acscsv

# for custom twitter output, import both the fields module and the code module
from twitter_acs_fields import *
import twitter_acs


#
# define any custom field extractor classes here. 
#



class CustomCSV( twitter_acs.TwacsCSV ):
    """
    Test class for experimenting with new output combinations. This class should inherit
    from the appropriate module.class in the core library. Compliance and invalid records 
    are handled by the parent class' procRecord() method. This class should only define a 
    new get_output_list() method which overrides the parent method and determines the 
    custom output. 
    """       
    
    def get_output_list(self, d):
        """
        Use this method to overwrite the output method in the parent class. Append values from 
        desired payload fields to the output list, which is returned at the end of this method. 
        Non-str values (ints, lists, etc), must be cast as str or will return 'None'. 
        
        Take a JSON Activity Streams payload as a Python dictionary. Extract the fields 
        appended to output_list and then return output_list. 
        """
        output_list = [] 

        # twitter country code
        output_list.append( Field_location_twitter_country_code(d).value )

        # matching rules -- note the str cast; value is a list 
        output_list.append( str(Field_gnip_rules(d).value) )

        # username 
        output_list.append( Field_actor_preferredusername(d).value )

        # geo-tag coords (returns a list, cast to str)
        output_list.append( str(Field_geo_coordinates(d).value) )


        # done building output list 
        return output_list 



if __name__ == "__main__":
    """
    Receive data from stdin (decompressed JSON-lines only) and process using the existing 
    code, but let this module's get_output_list() method define the output fields. 
    """

    # Get the appropriate object by mocking the constructor in the main gnacs.py code. most 
    #   common command-line options (flags) don't matter since we're explicitly defining the 
    #   fields to be printed in the method above 
    processing_obj = CustomCSV("|", None, *[True]*7) 

    for line_number, record in processing_obj.file_reader(): 
        # note: this doesn't handle broken pipe errors  
        sys.stdout.write( u"{}\n".format( processing_obj.procRecord(record, emptyField="None") ))

