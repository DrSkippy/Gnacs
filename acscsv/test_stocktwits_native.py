#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague, Fiona Pigott"
__license__="Simplified BSD"

import sys
import unittest
from StringIO import StringIO
from stocktwits_native import *


# valid native stocktwits record
NICE_STRING = """{"id":12802603,"body":"&quot;Hard knocks have a place and value, but hard thinking goes farther in less time.&quot; - Henry Ford","created_at":"2013-04-01T00:32:06Z","user":{"id":76647,"username":"TradingPlays","name":"Paul Elliott","avatar_url":"http://avatars.stocktwits.net/production/76647/thumb-1348961241.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/76647/thumb-1348961241.png","identity":"User","classification":[],"join_date":"2011-05-07","followers":273,"following":52,"ideas":3002,"following_stocks":0,"location":"USA","bio":"Proprietary stock trader, specializing in active intraday trading strategies.","website_url":"http://www.tradingplays.com","trading_strategy":{"assets_frequently_traded":["Equities"],"approach":"Momentum","holding_period":"Day Trader","experience":"Professional"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"entities":{"sentiment":null}}"""


class TestStocktwitsNative(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        Stocktwits-native constructor takes five args - create one example of each for 
        use in all tests (loop over the self.objs list).
        """ 
        self.delim = '|'
        self.objs = [ 
                    # base object
                    StocktwitsNative(self.delim, None, False, False, False)
                    # individual options 
                    , StocktwitsNative(self.delim, None, True, False, False)
                    , StocktwitsNative(self.delim, None, False, True, False)
                    , StocktwitsNative(self.delim, None, False, False, True) 
                    # all options
                    , StocktwitsNative(self.delim, None, True, True, True) 
                    # arbitrary keypath 
                    , StocktwitsNative(self.delim, "source:title", False, False, False) 
                    ]
        ## set some vars once, update when needed
        self.base_length = 3
        # count of extra fields added by each of these options
        self.keypath_length = 1
        self.user_length = 3 
        self.struct_length = 3 
        self.influence_length = 3 
        self.all_length = self.base_length \
                            + self.user_length \
                            + self.struct_length \
                            + self.influence_length
        

    def tearDown(self):
        """Nothing to do here."""
        pass


    def test_sampleData(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        stocktwits_native_sample.json example file without raising an Exception.
        """
        # get a temporary object
        tmp = self.objs[0]

        # grab the correct data file 
        # TODO: replace hard-coded path to file -- requires running test from acscsv/ dir
        datafile = "../data/{}_sample.json".format(tmp.__module__)  

        # loop over all test stocktwits processing objects
        for o in self.objs:
            # loop over records in test file 
            for i, record in o.file_reader(datafile):
                record_string = o.procRecord(record)


    #
    # test the output (length) for each kind of StocktwitsNative object 
    #
    
    def test_base_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the base instance 
        o = self.objs[0]
        
        # precaution against failure of o.file_reader to iterate
        loop = False

        # use sample record in this module 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            loop = True
            # procRecord returns a delimited string
            record_string = o.procRecord(record)
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length 
                            )  
        self.assertTrue( loop )


    def test_user(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs[1]
        
        # precaution against failure of o.file_reader to iterate
        loop = False

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            loop = True
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.user_length 
                            ) 
        self.assertTrue( loop )


    def test_struct(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs[2]
        
        # precaution against failure of o.file_reader to iterate
        loop = False

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            loop = True
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.struct_length 
                            )  
        self.assertTrue( loop )


    def test_influence(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs[3]
        
        # precaution against failure of o.file_reader to iterate
        loop = False

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            loop = True
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.influence_length 
                            )  
        self.assertTrue( loop )

    
    def test_all(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs[4]
        
        # precaution against failure of o.file_reader to iterate
        loop = False

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            loop = True
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.all_length 
                            )  
        self.assertTrue( loop )


    def test_keypath(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs[5]
        
        # precaution against failure of o.file_reader to iterate
        loop = False

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            loop = True
            record_string = o.procRecord(record)
            # should have 1 extra field now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.keypath_length 
                            )  
        self.assertTrue( loop )

   
    def test_extractors(self):
        """
        There aren't extractors for the stocktwits_native module, so all we can really do is
        test that the number of fields being extracted is correct (previous tests). 
        """
        pass

        

if __name__ == "__main__":
    unittest.main()
