#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from tumblr_acs import *


# valid activity from source (eg from data/) 
VALID_ACTIVITY = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"summary":"","tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFrom":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{}}"""


class TestTumblrACS(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        TblracsCSV constructor takes  args - create one example of each for 
        use in all tests (loop over the self.objs list).
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular object cases
        self.objs = { 
                    "base": TblracsCSV(self.delim, None, False, False, False, False)
                    , "user": TblracsCSV(self.delim, None, True, False, False, False)
                    , "rules": TblracsCSV(self.delim, None, False, True, False, False)
                    , "lang": TblracsCSV(self.delim, None, False, False, True, False)
                    , "struct": TblracsCSV(self.delim, None, False, False, False, True)
                    , "all": TblracsCSV(self.delim, None, True, True, True, True)
                    , "keypath": TblracsCSV(self.delim, "verb", False, False, False, False)
                    }

        # set any instance attributes here, avoid hard-coding in test methods 
        self.base_length = 4
        # count of extra fields added by each of these options
        self.keypath_length = 1
        self.user_length = 2
        self.rules_length = 1
        self.lang_length = 1
        self.struct_length = 3
        self.all_length = self.base_length \
                            + self.user_length \
                            + self.lang_length \
                            + self.struct_length \
                            + self.rules_length 

    def tearDown(self):
        """Nothing to do here."""
        pass

    def test_sample_data(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        tumblr_sample.json example file without raising an Exception.
        """
        # get a temporary object
        tmp = self.objs["base"]

        # grab the correct data file 
        datafile = "./data/tumblr_sample.json"

        # loop over all test tumblr processing objects
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
    # test the output (length) for each kind of TblracsCSV object 
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


    def test_struct_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["struct"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.struct_length 
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

    
    def test_lang_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["lang"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.lang_length 
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

    #
    # test that all of the fields we need to extract from the records actually work
    #

    def test_struct_fields(self):
        """
        Test for the presence of non-"None" values in a good record when using the 'struct' 
        option, and "None"s in an intentionally-damaged record.
        """ 

        # this activity (chosen from data/) has all the struct fields in it  
        GOOD_STRUCT_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"summary":"","tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFrom":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{}}"""

        # break the "tumblrRebloggedFrom" key in this activity, so that options_struct fields should all be "None" 
        BAD_STRUCT_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"summary":"","tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFromBAD":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{}}"""

        o = self.objs["struct"]

        # this should have data 
        for i, record in o.file_reader( json_string=GOOD_STRUCT_STRING ):
            record_string = o.procRecord(record)
            [ self.assertNotEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.struct_length:] 
            ] 
        
        # this should not have data in the 2nd and 3rd struct fields (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_STRUCT_STRING ):
            record_string = o.procRecord(record)
            [ self.assertEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.struct_length+1:] 
            ] 

    def test_summary_content_fields(self):
        """
        Test for the presence of non-"None" values in a good record,
        and "None"s in an intentionally-damaged record.
        """ 

        # this record contains an valid "object:summary" key path
        GOOD_CONTENT_SUMMARY_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"summary":"","tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFrom":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{}}"""

# neither "summary" nor "content" keys are in this record; should return None
        BAD_CONTENT_SUMMARY_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFromBAD":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{}}"""

        o = self.objs["base"]

        # this should have data (an empty string)
        for i, record in o.file_reader( json_string=GOOD_CONTENT_SUMMARY_STRING ):
            record_string = o.procRecord(record)
            self.assertNotEqual( "None", record_string.split(self.delim)[2] )
        
        # this should return "None" because there is no "summary" key in the "object" field
        for i, record in o.file_reader( json_string=BAD_CONTENT_SUMMARY_STRING ):
            record_string = o.procRecord(record)
            #print(record_string)
            self.assertEqual( "None", record_string.split(self.delim)[2] )
   
#
    def test_language_field(self):
        """
        Test for the presence of non-"None" values in a good record,
        and "None"s in an intentionally-damaged record.
        """ 

        # this record contains an valid language key:value pair 
        GOOD_LANG_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266561/post","verb":"post","target":{"link":"http://m2lm-photography.tumblr.com/","displayName":"m2lm-photography","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/99030041"},"object":{"summary":"<p>Blé</p><p><a href=\\"http://m2lm-photography.tumblr.com\\">http://m2lm-photography.tumblr.com</a></p>","tags":[{"displayName":"M2LM-photography"},{"displayName":"Blé"}],"id":"tag:gnip.tumblr.com:2012:post/45837266561","tumblrReblogKey":"uBR5KD9F","items":[{"summary":"","image":{"height":75,"width":75,"link":"http://24.media.tumblr.com/e3e1d83c86585d9288f443bc2a4f1461/tumblr_mjyss26sZD1s92ligo1_75sq.jpg"},"objectType":"image","fullImage":{"height":853,"width":1280,"link":"http://25.media.tumblr.com/e3e1d83c86585d9288f443bc2a4f1461/tumblr_mjyss26sZD1s92ligo1_1280.jpg"}}],"objectTypes":["image"],"link":"http://m2lm-photography.tumblr.com/post/45837266561/ble-http-m2lm-photography-tumblr-com","totalItems":1,"tumblrType":"photo","postedTime":"2013-03-20T15:09:38+00:00","tumblrFormat":"html","objectType":"photo-album"},"gnip":{"urls":[{"url":"http://m2lm-photography.tumblr.com","expanded_url":"http://m2lm-photography.tumblr.com"}],"language":{"value":"en"}}}"""

        # this record has a bad language key 
        BAD_LANG_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266561/post","verb":"post","target":{"link":"http://m2lm-photography.tumblr.com/","displayName":"m2lm-photography","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/99030041"},"object":{"summary":"<p>Blé</p><p><a href=\\"http://m2lm-photography.tumblr.com\\">http://m2lm-photography.tumblr.com</a></p>","tags":[{"displayName":"M2LM-photography"},{"displayName":"Blé"}],"id":"tag:gnip.tumblr.com:2012:post/45837266561","tumblrReblogKey":"uBR5KD9F","items":[{"summary":"","image":{"height":75,"width":75,"link":"http://24.media.tumblr.com/e3e1d83c86585d9288f443bc2a4f1461/tumblr_mjyss26sZD1s92ligo1_75sq.jpg"},"objectType":"image","fullImage":{"height":853,"width":1280,"link":"http://25.media.tumblr.com/e3e1d83c86585d9288f443bc2a4f1461/tumblr_mjyss26sZD1s92ligo1_1280.jpg"}}],"objectTypes":["image"],"link":"http://m2lm-photography.tumblr.com/post/45837266561/ble-http-m2lm-photography-tumblr-com","totalItems":1,"tumblrType":"photo","postedTime":"2013-03-20T15:09:38+00:00","tumblrFormat":"html","objectType":"photo-album"},"gnip":{"urls":[{"url":"http://m2lm-photography.tumblr.com","expanded_url":"http://m2lm-photography.tumblr.com"}]}}"""

        o = self.objs["lang"]

        # this should have data (an empty string)
        for i, record in o.file_reader( json_string=GOOD_LANG_STRING ):
            record_string = o.procRecord(record)
            self.assertNotEqual( u"None", record_string.split(self.delim)[4] )
        
        # this should not have data in the 2nd and 3rd struct fields (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_LANG_STRING ):
            record_string = o.procRecord(record)
            #print(record_string)
            self.assertEqual( u"None", record_string.split(self.delim)[4] )


    def test_rules_field(self):
        """
        Test for the presence of non-"None" values in a good record,
        and "None"s in an intentionally-damaged record.
        """ 

        # this record contains an valid "gnip:matching_rules" key path, 
        GOOD_RULES_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"summary":"","tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFrom":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{"matching_rules":[{"value": "startdustgrass","tag":"test"}]}}"""

# no "matching_rules" key in the "gnip" field in this record; should return "[]"
        BAD_RULES_STRING = """{"id":"tag:gnip.tumblr.com:2012:post/45837266698/post","tumblrRebloggedRoot":{"author":{"link":"http://the-personal-quotes.tumblr.com/","displayName":"the personal quotes"},"link":"http://the-personal-quotes.tumblr.com/post/18729698371"},"verb":"post","target":{"link":"http://stardustgrass.tumblr.com/","displayName":"stardustgrass","objectType":"blog"},"postedTime":"2013-03-20T15:09:40+00:00","actor":{"id":"tag:gnip.tumblr.com:2012:blog/76962586"},"object":{"tags":[{"displayName":"the help"},{"displayName":"gif"}],"summary":"","tumblrNoteCount":303949,"objectTypes":["image"],"link":"http://stardustgrass.tumblr.com/post/45837266698","postedTime":"2013-03-20T15:09:40+00:00","tumblrFormat":"html","id":"tag:gnip.tumblr.com:2012:post/45837266698","source":{"link":"http://the-personal-quotes.tumblr.com/post/18729698371","displayName":"the-personal-quotes"},"items":[{"summary":"","image":{"height":52,"width":100,"link":"http://25.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_100.gif"},"objectType":"image","fullImage":{"height":260,"width":500,"link":"http://24.media.tumblr.com/tumblr_m0dbepbg1B1qfdwsio1_500.gif"}}],"tumblrReblogKey":"57dc6dOl","totalItems":1,"tumblrType":"photo","objectType":"photo-album"},"tumblrRebloggedFrom":{"author":{"link":"http://illllest.tumblr.com/","displayName":"Unknown Pleasures"},"link":"http://illllest.tumblr.com/post/45832750088"},"gnip":{}}"""

        o = self.objs["rules"]

        # this should have data (an empty string)
        for i, record in o.file_reader( json_string=GOOD_RULES_STRING ):
            record_string = o.procRecord(record)
            self.assertNotEqual( "None", record_string.split(self.delim)[4] )
            self.assertNotEqual( "[]", record_string.split(self.delim)[4] )
        
        # this should not have data in the 2nd and 3rd struct fields (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_RULES_STRING ):
            record_string = o.procRecord(record)
            self.assertEqual( "[]", record_string.split(self.delim)[4] )


if __name__ == "__main__":
    unittest.main()
