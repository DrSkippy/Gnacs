#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague, Fiona Pigott"
__license__="Simplified BSD"

import sys
import unittest
from StringIO import StringIO
from stocktwits_native import *


# valid native stocktwits record (from sample data dir), used in a bunch of tests
NICE_STRING = """{"id":12802603,"body":"&quot;Hard knocks have a place and value, but hard thinking goes farther in less time.&quot; - Henry Ford","created_at":"2013-04-01T00:32:06Z","user":{"id":76647,"username":"TradingPlays","name":"Paul Elliott","avatar_url":"http://avatars.stocktwits.net/production/76647/thumb-1348961241.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/76647/thumb-1348961241.png","identity":"User","classification":[],"join_date":"2011-05-07","followers":273,"following":52,"ideas":3002,"following_stocks":0,"location":"USA","bio":"Proprietary stock trader, specializing in active intraday trading strategies.","website_url":"http://www.tradingplays.com","trading_strategy":{"assets_frequently_traded":["Equities"],"approach":"Momentum","holding_period":"Day Trader","experience":"Professional"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"entities":{"sentiment":null}}"""


class TestStocktwitsNative(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        Stocktwits-native constructor takes five args - create one example of each for 
        use in all tests (loop over the self.objs list).
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular cases
        self.objs = { 
                    "base": StocktwitsNative(self.delim, None, False, False, False)
                    , "user": StocktwitsNative(self.delim, None, True, False, False) 
                    , "struct": StocktwitsNative(self.delim, None, False, True, False) 
                    , "influence": StocktwitsNative(self.delim, None, False, False, True) 
                    , "all": StocktwitsNative(self.delim, None, True, True, True) 
                    , "keypath": StocktwitsNative(self.delim, "source:title", False, False, False) 
                    }

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


    def test_sample_data(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        stocktwits_native_sample.json example file without raising an Exception.
        """
        # get a temporary object
        tmp = self.objs["base"]

        # grab the correct data file 
        datafile = "./data/stocktwits_native_sample.json"

        # loop over all test stocktwits processing objects
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
        g = o.file_reader( json_string=NICE_STRING )
        self.assertIsInstance( g.next(), tuple ) 

   
    #
    # test the output (length) for each kind of StocktwitsNative object 
    #
    
    def test_base_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the base instance 
        o = self.objs["base"]

        # use sample record in this module 
        for i, record in o.file_reader( json_string=NICE_STRING ):
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
        g = o.file_reader( json_string=NICE_STRING )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
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
        g = o.file_reader( json_string=NICE_STRING )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.struct_length 
                            )  


    def test_influence_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["influence"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=NICE_STRING )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
            record_string = o.procRecord(record)
            # should have 3 extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.base_length + self.influence_length 
                            )  

    
    def test_all_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["all"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=NICE_STRING )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
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
        g = o.file_reader( json_string=NICE_STRING )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=NICE_STRING ):
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
        GOOD_STRUCT_STRING = """{"id":12802606,"body":"@Pieman @nnsts just curious.  How much did you lose on such yelling of &#39;out for good?&#39;   Did you set a stop loss?","created_at":"2013-04-01T00:33:39Z","user":{"id":216592,"username":"nnsts","name":"nntrader","avatar_url":"http://avatars.stocktwits.net/production/216592/thumb-1361592350.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/216592/thumb-1361592350.png","identity":"User","classification":[],"join_date":"2013-02-22","followers":9,"following":4,"ideas":843,"following_stocks":2,"location":"","bio":null,"website_url":null,"trading_strategy":{"assets_frequently_traded":["Equities","Options","Futures","Bonds"],"approach":"Technical","holding_period":"Swing Trader","experience":"Novice"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"conversation":{"parent_message_id":12802589,"in_reply_to_message_id":12802589,"parent":false,"replies":3},"entities":{"sentiment":null}}"""

        # break the "conversation" key in this activity, so that options_struct fields should all be "None" 
        BAD_STRUCT_STRING = """{"id":12802606,"body":"@Pieman @nnsts just curious.  How much did you lose on such yelling of &#39;out for good?&#39;   Did you set a stop loss?","created_at":"2013-04-01T00:33:39Z","user":{"id":216592,"username":"nnsts","name":"nntrader","avatar_url":"http://avatars.stocktwits.net/production/216592/thumb-1361592350.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/216592/thumb-1361592350.png","identity":"User","classification":[],"join_date":"2013-02-22","followers":9,"following":4,"ideas":843,"following_stocks":2,"location":"","bio":null,"website_url":null,"trading_strategy":{"assets_frequently_traded":["Equities","Options","Futures","Bonds"],"approach":"Technical","holding_period":"Swing Trader","experience":"Novice"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"GNIP_conversation":{"parent_message_id":12802589,"in_reply_to_message_id":12802589,"parent":false,"replies":3},"entities":{"sentiment":null}}"""

        o = self.objs["struct"]

        # this should have data 
        for i, record in o.file_reader( json_string=GOOD_STRUCT_STRING ):
            record_string = o.procRecord(record)
            [ self.assertNotEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.struct_length:] 
            ] 
        
        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_STRUCT_STRING ):
            record_string = o.procRecord(record)
            [ self.assertEqual( "None", x ) 
                for x in record_string.split(self.delim)[-self.struct_length:] 
            ] 


    def test_user_fields(self):
        """
        Test for the presence of non-"None" values in a good record when using the 'user' 
        option, and "None"s in an intentionally-damaged record.
        """ 

        # this activity (chosen from data/) has the user fields in it  
        tmp_url = "http://www.example.com"
        # note: must do the string substition with %s because .format() will look for keys by {}
        GOOD_USER_STRING = """{"id":12802606,"body":"@Pieman @nnsts just curious.  How much did you lose on such yelling of &#39;out for good?&#39;   Did you set a stop loss?","created_at":"2013-04-01T00:33:39Z","user":{"id":216592,"username":"nnsts","name":"nntrader","avatar_url":"http://avatars.stocktwits.net/production/216592/thumb-1361592350.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/216592/thumb-1361592350.png","identity":"User","classification":[],"join_date":"2013-02-22","followers":9,"following":4,"ideas":843,"following_stocks":2,"location":"","bio":null,"website_url":"%s","trading_strategy":{"assets_frequently_traded":["Equities","Options","Futures","Bonds"],"approach":"Technical","holding_period":"Swing Trader","experience":"Novice"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"conversation":{"parent_message_id":12802589,"in_reply_to_message_id":12802589,"parent":false,"replies":3},"entities":{"sentiment":null}}"""%(tmp_url)

        # looks like these fields should always exist, but the 'website_url' could be null. force that & check for "None"
        BAD_USER_STRING = """{"id":12802606,"body":"@Pieman @nnsts just curious.  How much did you lose on such yelling of &#39;out for good?&#39;   Did you set a stop loss?","created_at":"2013-04-01T00:33:39Z","user":{"id":216592,"username":"nnsts","name":"nntrader","avatar_url":"http://avatars.stocktwits.net/production/216592/thumb-1361592350.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/216592/thumb-1361592350.png","identity":"User","classification":[],"join_date":"2013-02-22","followers":9,"following":4,"ideas":843,"following_stocks":2,"location":"","bio":null,"website_url":null,"trading_strategy":{"assets_frequently_traded":["Equities","Options","Futures","Bonds"],"approach":"Technical","holding_period":"Swing Trader","experience":"Novice"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"conversation":{"parent_message_id":12802589,"in_reply_to_message_id":12802589,"parent":false,"replies":3},"entities":{"sentiment":null}}"""

        o = self.objs["user"]

        # this should have data 
        for i, record in o.file_reader( json_string=GOOD_USER_STRING ):
            record_string = o.procRecord(record)
            self.assertNotEqual( "None", record_string.split(self.delim)[-1] )
            self.assertEqual( tmp_url , record_string.split(self.delim)[-1] )
        
        # this should not have data (should have "None" instead) 
        for i, record in o.file_reader( json_string=BAD_USER_STRING ):
            record_string = o.procRecord(record)
            # payload (json) null ==> Python None ==> check in module
            self.assertEqual( "None", record_string.split(self.delim)[-1] )

   
if __name__ == "__main__":
    unittest.main()
