#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Brian Lehman"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from disqus_acs import *


# valid an activity from source (eg from data/) turned into a strong -- so use json.loads(str) to create a dict
VALID_ACTIVITY = """{"body": ">\\"incompetent situations like Benghazi.\\"<\\n\\n\\nBlow it out yourass, Goober\\n\\n\\n(I mean no disrespect by that)\\n\\n\\nThe last GOP administration is responsible for 4,000+ dead American service people, 2,800 dead Americans in NYC and 100,000+ dead Iraqi\'s.\\n\\n\\nAnd you\'rre going to get your panties in a bunch over 4 dead Americans killed in a terrorist attack in the ME -  because you think you can make some political hay over it?\\n\\n\\nWith all due respect - phucque you and the horse you rode in on", "disqusTypePrev": "approved", "inReplyTo": {"objectType": "comment", "id": "tag:gnip.disqus.com:2012:comment/1haa42", "disqusId": "1473071832", "author": {"id": "tag:gnip.disqus.com:2012:account/a8m86y", "disqusId": "64154961"}}, "object": {"link": "http://www.politico.com/story/2014/07/benghazi-trey-gowdy-108625.html#comment-1473078627", "id": "tag:gnip.disqus.com:2012:comment/1hae9j", "disqusId": "1473078627", "objectType": "comment"}, "disqusType": "approved", "verb": "update", "disqusMessageTimestamp": "2014-07-07T23:34:26+00:00", "id": "tag:gnip.disqus.com:2012:comment/1hae9j/update/2014-07-07T19:33:59/ab61a0faa8752910cf949d274bfd51d1090b2dedc63bf7fe5d21a608441f6ac3", "target": {"website": {"id": "tag:gnip.disqus.com:2012:forum/itsy", "disqusId": "1422873"}, "link": "http://www.politico.com/story/2014/07/benghazi-trey-gowdy-108625.html", "disqusId": "2825453635", "postedTime": "2014-07-07T21:59:23+00:00", "id": "tag:gnip.disqus.com:2012:thread/a69my0m", "objectType": "article"}, "gnip": {"language": {"value": "en"}}, "actor": {"preferredUsername": "disqus_xs2HXcqTks", "id": "tag:gnip.disqus.com:2012:account/ani2ch", "disqusId": "95458297", "objectType": "person"}, "postedTime": "2014-07-07T23:33:59+00:00"}"""
        
class TestDisqus(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        DiacsCSV constructor takes  args - create one example of each for 
        use in all tests (loop over the self.objs list).
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular object cases
        #class DiacsCSV(acscsv.AcsCSV): def __init__(self, delim, options_keypath, options_user, options_rules, options_lang, options_struct, options_status)
        self.objs = { 
                    "base": DiacsCSV(self.delim,None,False,False,False,False,False) 
                    , "keypath": DiacsCSV(self.delim,"verb",False,False,False,False,False) 
                    , "user": DiacsCSV(self.delim,None,True,False,False,False,False) 
                    , "rules": DiacsCSV(self.delim,None,False,True,False,False,False) 
                    , "lang": DiacsCSV(self.delim,None,False,False,True,False,False) 
                    , "struct": DiacsCSV(self.delim,None,False,False,False,True,False) 
                    , "status": DiacsCSV(self.delim,None,False,False,False,False,True) 
                    , "all": DiacsCSV(self.delim,None,True,True,True,True,True) 
                    }

        # set any instance attributes here, avoid hard-coding in test methods 
        self.base_length = 3
        # count of extra fields added by each of these options
        self.keypath_length = 1
        self.user_length = 1
        self.rules_length = 1
        self.lang_length = 1
        self.struct_length = 5
        self.status_length = 3
        self.all_length = self.base_length \
                            + self.user_length \
                            + self.rules_length \
                            + self.lang_length \
                            + self.struct_length \
                            + self.status_length \
                                
    def tearDown(self):
        """
        Nothing to do here.
        """
        pass
    
    #
    # helpful to group test methods that are related into sections
    #

    def test_sample_data(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        disqus_sample.json example file without raising an Exception.
        """

        # get a temporary object
        tmp = self.objs["base"]

        # grab the correct data file 
        datafile = "./data/disqus_sample.json"

        # loop over all test disqus  processing objects
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
    # test the output (length) for each kind of DiacsCSV object 
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

    def test_struct_fields(self):
        """
        Test for the presence of non-"None" values in a good record when using the 'struct' 
        option, and "None"s in an intentionally-damaged record.
        """ 
        
        # this activity (chosen from data/) has all the struct fields in it  
        GOOD_STRUCT_STRING = VALID_ACTIVITY

        # remove the "inReplyTo" key in this activity, so that the last two options_struct fields should be "None" 
        BAD_STRUCT_STRING = """{"body": ">\\"incompetent situations like Benghazi.\\"<\\n\\n\\nBlow it out yourass, Goober\\n\\n\\n(I mean no disrespect by that)\\n\\n\\nThe last GOP administration is responsible for 4,000+ dead American service people, 2,800 dead Americans in NYC and 100,000+ dead Iraqi\'s.\\n\\n\\nAnd you\'rre going to get your panties in a bunch over 4 dead Americans killed in a terrorist attack in the ME -  because you think you can make some political hay over it?\\n\\n\\nWith all due respect - phucque you and the horse you rode in on", "disqusTypePrev": "approved", "object": {"link": "http://www.politico.com/story/2014/07/benghazi-trey-gowdy-108625.html#comment-1473078627", "id": "tag:gnip.disqus.com:2012:comment/1hae9j", "disqusId": "1473078627", "objectType": "comment"}, "disqusType": "approved", "verb": "update", "gnip": {"language": {"value": "en"}}, "id": "tag:gnip.disqus.com:2012:comment/1hae9j/update/2014-07-07T19:33:59/ab61a0faa8752910cf949d274bfd51d1090b2dedc63bf7fe5d21a608441f6ac3", "target": {"website": {"id": "tag:gnip.disqus.com:2012:forum/itsy", "disqusId": "1422873"}, "link": "http://www.politico.com/story/2014/07/benghazi-trey-gowdy-108625.html", "disqusId": "2825453635", "postedTime": "2014-07-07T21:59:23+00:00", "id": "tag:gnip.disqus.com:2012:thread/a69my0m", "objectType": "article"}, "disqusMessageTimestamp": "2014-07-07T23:34:26+00:00", "actor": {"preferredUsername": "disqus_xs2HXcqTks", "id": "tag:gnip.disqus.com:2012:account/ani2ch", "disqusId": "95458297", "objectType": "person"}, "postedTime": "2014-07-07T23:33:59+00:00"}"""
        
        o = self.objs["struct"]

        # these 5 values should have data 
        for i, record in o.file_reader( json_string=GOOD_STRUCT_STRING ):
            record_string = o.procRecord(record)
            [ self.assertNotEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.struct_length:] 
            ] 
        
        # these 2 values should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_STRUCT_STRING ):
            record_string = o.procRecord(record)
            [ self.assertEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.struct_length+3:] 
            ] 

    def test_status_fields(self):
        """
        Test for the presence of non-"None" values in a good record when using the 'struct' 
        option, and "None"s in an intentionally-damaged record.
        """ 
        
        # this activity (chosen from data/) has all the struct fields in it  
        GOOD_STATUS_STRING = VALID_ACTIVITY

        # remove the "inReplyTo" key in this activity, so that the last two options_struct fields should be "None" 
        BAD_STATUS_STRING = """{"body": ">\\"incompetent situations like Benghazi.\\"<\\n\\n\\nBlow it out yourass, Goober\\n\\n\\n(I mean no disrespect by that)\\n\\n\\nThe last GOP administration is responsible for 4,000+ dead American service people, 2,800 dead Americans in NYC and 100,000+ dead Iraqi\'s.\\n\\n\\nAnd you\'rre going to get your panties in a bunch over 4 dead Americans killed in a terrorist attack in the ME -  because you think you can make some political hay over it?\\n\\n\\nWith all due respect - phucque you and the horse you rode in on", "inReplyTo": {"author": {"id": "tag:gnip.disqus.com:2012:account/a8m86y", "disqusId": "64154961"}, "id": "tag:gnip.disqus.com:2012:comment/1haa42", "disqusId": "1473071832", "objectType": "comment"}, "object": {"link": "http://www.politico.com/story/2014/07/benghazi-trey-gowdy-108625.html#comment-1473078627", "id": "tag:gnip.disqus.com:2012:comment/1hae9j", "disqusId": "1473078627", "objectType": "comment"}, "verb": "update", "disqusMessageTimestamp": "2014-07-07T23:34:26+00:00", "id": "tag:gnip.disqus.com:2012:comment/1hae9j/update/2014-07-07T19:33:59/ab61a0faa8752910cf949d274bfd51d1090b2dedc63bf7fe5d21a608441f6ac3", "target": {"website": {"id": "tag:gnip.disqus.com:2012:forum/itsy", "disqusId": "1422873"}, "link": "http://www.politico.com/story/2014/07/benghazi-trey-gowdy-108625.html", "disqusId": "2825453635", "postedTime": "2014-07-07T21:59:23+00:00", "id": "tag:gnip.disqus.com:2012:thread/a69my0m", "objectType": "article"}, "gnip": {"language": {"value": "en"}}, "actor": {"preferredUsername": "disqus_xs2HXcqTks", "id": "tag:gnip.disqus.com:2012:account/ani2ch", "disqusId": "95458297", "objectType": "person"}, "postedTime": "2014-07-07T23:33:59+00:00"}"""
        
        o = self.objs["status"]

        # these 3 values should have data 
        for i, record in o.file_reader( json_string=GOOD_STATUS_STRING ):
            record_string = o.procRecord(record)
            [ self.assertNotEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.status_length:] 
            ] 
        
        # these 2 values should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_STATUS_STRING ):
            record_string = o.procRecord(record)
            [ self.assertEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.status_length+1:] 
            ]
    
    
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



 
if __name__ == "__main__":
    unittest.main()
