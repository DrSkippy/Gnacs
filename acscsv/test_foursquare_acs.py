#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from foursquare_acs import *


# valid activity from source (eg from data/) 
VALID_ACTIVITY = """{"id":"tag:gnip.foursquare.com:2013:checkin/53910e5c498eb98e8cadf5cc","postedTime":"2014-06-06T00:42:04+00:00","verb":"checkin","actor":{"objectType":"person","gender":"male"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d88cbd33acc6dcb3b7d0f1c","displayName":"Planet Fitness","objectType":"place","geo":{"type":"Point","coordinates":[-84.21241229795072,33.71550258242101]},"address":{"locality":"Decatur","region":"GA","postalCode":"30035","country":"United States"},"foursquareCategories":[{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d176941735","displayName":"Gym","image":"https://ss1.4sqi.net/img/categories_v2/building/gym_88.png"}]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":-14400,"gnip":{}}"""


class TestFoursquareACS(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        Foursquare constructor takes seven args - create one example of each for 
        use in all tests (loop over the self.objs list).
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular object cases
        self.objs = { 
                    "base": FsqacsCSV(self.delim, None, False, False, False)
                    , "geo": FsqacsCSV(self.delim, None, True, False, False)
                    , "user": FsqacsCSV(self.delim, None, False, True, False)
                    , "rules": FsqacsCSV(self.delim, None, False, False, True)
                    , "all": FsqacsCSV(self.delim, None, True, True, True)
                    , "keypath": FsqacsCSV(self.delim, "actor:gender", False, False, False) 
                    }

        # set any instance attributes here, avoid hard-coding in test methods 
        self.base_length = 6
        # count of extra fields added by each of these options
        self.keypath_length = 1
        self.geo_length = 4
        self.user_length = 1
        self.rules_length = 1
        self.all_length = self.base_length \
                            + self.geo_length \
                            + self.user_length \
                            + self.rules_length 

    def tearDown(self):
        """Nothing to do here."""
        pass

    
    def test_sample_data(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        foursquare_sample.json example file without raising an Exception.
        """
        # get a temporary object
        tmp = self.objs["base"]

        # grab the correct data file 
        datafile = "./data/foursquare_sample.json" 

        # loop over all test foursquare processing objects
        for o in self.objs.values():
            # loop over records in test file 
            for i, record in o.file_reader(datafile):
                # if there's a problem parsing, this method will raise an Exception
                record_string = o.procRecord(record)


    def test_reader(self):
        """Test that our file_reader method is working as expected."""
        # grab the base instance 
        o = self.objs["base"]
        
        # without eg a for loop, we use the generator's next() method 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

   
    #
    # test the output (length) for each kind of FsqacsCSV object 
    #
    
    def test_base_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the base instance 
        o = self.objs["base"]

        # use sample record in this module 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            # procRecord returns a delimited string
            record_string = o.procRecord(record)
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length 
                            )  


    def test_user_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["user"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.user_length 
                            ) 


    def test_geo_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["geo"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.geo_length 
                            )  

    
    def test_rules_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["rules"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.rules_length 
                            )  

    
    def test_all_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["all"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            loop = True
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.all_length 
                            )  


    def test_keypath_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["keypath"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            record_string = o.procRecord(record)
            # should have 1 extra field now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.keypath_length 
                            )  

    def test_category_field(self):
        """
        Test for the presence of non-"None" values in a good record,
        and "None"s in an intentionally-damaged record.
        """ 
        
        # 
        GOOD_CAT_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"locality":"Ankara","region":"Türkiye","postalCode":"06800","country":"Turkey"},"foursquareCategories":[{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d155941735","displayName":"Gastropub"},{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d16d941735","displayName":"Café"},{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d16e941735","displayName":"Fast Food Restaurant"}]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

        # make fourSquareCategories an empty list
        BAD_CAT_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"locality":"Ankara","region":"Türkiye","postalCode":"06800","country":"Turkey"},"foursquareCategories":[]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

        o = self.objs["base"]

        # this should have data 
        for i, record in o.file_reader( json_string=GOOD_CAT_STRING ):
            record_string = o.procRecord(record)
            self.assertNotEqual( "None", record_string.split(self.delim)[4] )
            self.assertNotEqual( "['None']", record_string.split(self.delim)[4] )
        
        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_CAT_STRING ):
            record_string = o.procRecord(record)
            self.assertEqual( "['None']", record_string.split(self.delim)[4] )

    def test_geo_fields(self):
        """
        Test for the presence of non-"None" values in a good record,
        and "None"s in an intentionally-damaged record.
        """ 

        GOOD_GEO_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"locality":"Ankara","region":"Türkiye","postalCode":"06800","country":"Turkey"},"foursquareCategories":[{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d155941735","displayName":"Gastropub"},{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d16d941735","displayName":"Café"},{"id":"tag:gnip.foursquare.com:2013:category/4bf58dd8d48988d16e941735","displayName":"Fast Food Restaurant"}]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

        BAD_LOCALITY_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"region":"Türkiye","postalCode":"06800","country":"Turkey"},"foursquareCategories":[]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

# missing postal code
        BAD_POSTALCODE_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"locality":"Ankara","region":"Türkiye","country":"Turkey"},"foursquareCategories":[]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

# missing country key
        BAD_COUNTRY_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"locality":"Ankara","region":"Türkiye","postalCode":"06800"},"foursquareCategories":[]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

# region key missing
        BAD_REGION_STRING = """{"id":"tag:gnip.foursquare.com:2013:checkin/51a0afd68bfdb8df55921c1d","postedTime":"2013-05-25T12:34:29+00:00","verb":"checkin","actor":{"objectType":"person","gender":"female"},"object":{"id":"tag:gnip.foursquare.com:2013:venue/4d1778691356a093cc22dc82","displayName":"Leman Kültür","objectType":"place","geo":{"type":"Point","coordinates":[32.688869786457,39.87231478030219]},"address":{"locality":"Ankara","postalCode":"06800","country":"Turkey"},"foursquareCategories":[]},"provider":{"link":"https://foursquare.com","displayName":"Foursquare","objectType":"service"},"foursquareCheckinUtcOffset":10800}"""

        o = self.objs["geo"]

        # this should have data 
        for i, record in o.file_reader( json_string=GOOD_GEO_STRING ):
            record_string = o.procRecord(record)
            self.assertNotEqual( "None", record_string.split(self.delim)[6] )
        
        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_LOCALITY_STRING ):
            record_string = o.procRecord(record)
            self.assertEqual( "None", record_string.split(self.delim)[6] )

        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_POSTALCODE_STRING ):
            record_string = o.procRecord(record)
            self.assertEqual( "None", record_string.split(self.delim)[9] )
        
        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_REGION_STRING ):
            record_string = o.procRecord(record)
            self.assertEqual( "None", record_string.split(self.delim)[7] )
        
        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_COUNTRY_STRING ):
            record_string = o.procRecord(record)
            self.assertEqual( "None", record_string.split(self.delim)[8] )


 
if __name__ == "__main__":
    unittest.main()
