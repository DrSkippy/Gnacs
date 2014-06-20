#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague, Fiona Pigott"
__license__="Simplified BSD"

import sys
import unittest
from StringIO import StringIO
from stocktwits_native import *


# default output for all pubs is 3 fields
BASE_LENGTH = 3

# valid native stocktwits record
NICE_STRING = """{"id":12802603,"body":"&quot;Hard knocks have a place and value, but hard thinking goes farther in less time.&quot; - Henry Ford","created_at":"2013-04-01T00:32:06Z","user":{"id":76647,"username":"TradingPlays","name":"Paul Elliott","avatar_url":"http://avatars.stocktwits.net/production/76647/thumb-1348961241.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/76647/thumb-1348961241.png","identity":"User","classification":[],"join_date":"2011-05-07","followers":273,"following":52,"ideas":3002,"following_stocks":0,"location":"USA","bio":"Proprietary stock trader, specializing in active intraday trading strategies.","website_url":"http://www.tradingplays.com","trading_strategy":{"assets_frequently_traded":["Equities"],"approach":"Momentum","holding_period":"Day Trader","experience":"Professional"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"entities":{"sentiment":null}}"""

# modified record for testing
EVIL_STRING = """{"id":12802603,"EVIL_body":"&quot;Hard knocks have a place and value, but hard thinking goes farther in less time.&quot; - Henry Ford","created_at":"2013-04-01T00:32:06Z","user":{"id":76647,"username":"TradingPlays","name":"Paul Elliott","avatar_url":"http://avatars.stocktwits.net/production/76647/thumb-1348961241.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/76647/thumb-1348961241.png","identity":"User","classification":[],"join_date":"2011-05-07","followers":273,"following":52,"ideas":3002,"following_stocks":0,"location":"USA","bio":"Proprietary stock trader, specializing in active intraday trading strategies.","website_url":"http://www.tradingplays.com","trading_strategy":{"assets_frequently_traded":["Equities"],"approach":"Momentum","holding_period":"Day Trader","experience":"Professional"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"entities":{"sentiment":null}}"""


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
                    , StocktwitsNative(self.delim, "source:title", True, True, True) 
                    ]
        #print >>sys.stderr, "*** objs={}".format(self.objs)
        

    def tearDown(self):
        """Nothing to do here."""
        pass

#
#    def test_sampleData(self):
#        """
#        Check that we can use each test object's procRecord method on each record in the 
#        stocktwits_native_sample.json example file without raising an Exception.
#        """
#        # get a temporary object
#        tmp = self.objs[0]
#
#        # grab the correct data file 
#        # TODO: replace hard-coded path to file -- requires running test from acscsv/ dir
#        datafile = "../data/{}_sample.json".format(tmp.__module__)  
#
#        # loop over all test stocktwits processing objects
#        for o in self.objs:
#            # loop over records in test file 
#            for i, record in o.file_reader(datafile):
#                foo = o.procRecord(record)


    def test_base_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the base instance 
        o = self.objs[0]

        # has the right contents?
        #sio = StringIO( NICE_STRING )
        #print >>sys.stderr, "*** sio={}".format(sio.getvalue())

        #print >>sys.stderr, "*** {}".format(o.file_reader( StringIO( NICE_STRING ) ))

#        # use sample record in this module 
#        for i, record in o.file_reader( StringIO( NICE_STRING ) ):
#            #print >>sys.stderr, "*** i={}, record={}".format(i, record)
#            # procRecord returns a delimited string
#            foo = o.procRecord(record)
#            self.assertEqual( len(foo.split( self.delim )), BASE_LENGTH )  

       
#
#    def test_user(self):
#        """
#        Check the number of fields being output. (Update the expected results when new 
#        features are added to the module.)
#        """
#        # grab the right instance 
#        o = self.objs[1]
#        # use sample record above 
#        for i, record in o.file_reader( StringIO( NICE_STRING ) ):
#            foo = o.procRecord(record)
#            # should have 1 extra field now 
#            self.assertEqual( len(foo.split( self.delim )), BASE_LENGTH + 1 )  
#
#
#    def test_struct(self):
#        """
#        Check the number of fields being output. (Update the expected results when new 
#        features are added to the module.)
#        """
#        # grab the right instance 
#        o = self.objs[2]
#        # use sample record above 
#        for i, record in o.file_reader( StringIO( NICE_STRING ) ):
#            foo = o.procRecord(record)
#            #print >>sys.stderr, "*** foo={}".format(foo)
#            # should have 1 extra field now 
#            self.assertEqual( len(foo.split( self.delim )), BASE_LENGTH + 1 )  
#
#
#    def test_influence(self):
#        """
#        Check the number of fields being output. (Update the expected results when new 
#        features are added to the module.)
#        """
#        # grab the right instance 
#        o = self.objs[3]
#        # use sample record above 
#        for i, record in o.file_reader( StringIO( NICE_STRING ) ):
#            foo = o.procRecord(record)
#            # should have 1 extra field now 
#            self.assertEqual( len(foo.split( self.delim )), BASE_LENGTH + 27 )  
#
#    
#    def test_keypath(self):
#        """Does this constructor arg need to be here? Doesn't get used anywhere in this module.""" 
#        pass 


# test broken fields

    def test_body(self):
        """Maybe this method should just test all of the extractors, one by one?"""
        

        for obj in self.objs:
            for i, record in obj.file_reader(StringIO(EVIL_STRING)):
                self.assertEqual(12802603, record["id"]) 
                self.assertEqual("None", record["body"]) 
        
        
        



if __name__ == "__main__":
    unittest.main()
