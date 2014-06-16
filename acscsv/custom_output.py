#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="Simplified BSD"

import sys
import json
import acscsv

# for custom twitter output, import both the fields module and the code module
from twitter_acs_Fields import *
import twitter_acs


#
# define any custom field extractor classes here. inherit from acscsv.* as needed 
#



#
# edit the subclass here, as needed (eg inherit from twitter_acs.TwacsCSV)
#
class TestCSV( twitter_acs.TwacsCSV ):
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
        
        Take a JSON Activity Streams payload as a Python dictionary. 
        """
        output_list = [] 

        # twitter country code
        output_list.append( Field_location_twitter_country_code(d).value )

        # activity id 
        output_list.append( Field_id(d).value )

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
    processing_obj = TestCSV("|", None, *[True]*7) 

    line_number = 0 
    for r in sys.stdin: 
        line_number += 1
        try:
            recs = [json.loads(r.strip())]
        except ValueError:
            try:
                # maybe a missing line feed?
                recs = [json.loads(x) for x in r.strip().replace("}{", "}GNIP_SPLIT{").split("GNIP_SPLIT")]
            except ValueError:
                sys.stderr.write("Invalid JSON record (%d) %s, skipping\n"%(line_number, r.strip()))
                continue
        for record in recs:
            if len(record) == 0:
                continue
            sys.stdout.write("%s\n"%processing_obj.procRecord(record, emptyField="None"))

