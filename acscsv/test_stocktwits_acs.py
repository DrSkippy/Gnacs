#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from stocktwits_acs import *


# valid activity from source (eg from data/) 
VALID_ACTIVITY = """{"id":"tag:gnip.stocktwits.com:2012:note/24443686","verb":"post","body":"Today&#39;s w/l $txmd $nuro $achn $royl $useg $dgaz $grpn $live $oncy $camt","actor":{"id":"person:stocktwits:358559","objectType":"person","displayName":"Relentless","preferredUsername":"Relentlessiam","followersCount":63,"followingCount":40,"followingStocksCount":0,"statusesCount":632,"summary":null,"links":[{"href":null,"rel":"me"}],"link":"http://stocktwits.com/Relentlessiam","image":"http://avatars.stocktwits.net/production/358559/thumb-1401411068.png","tradingStrategy":{"approach":"Momentum","holdingPeriod":"Day Trader","experience":null,"assetsFrequentlyTraded":["Equities","Options"]},"classification":[]},"object":{"id":"note:stocktwits:24443686","objectType":"note","postedTime":"2014-07-08T12:03:04Z","updatedTime":"2014-07-08T12:03:04Z","summary":"Today&#39;s w/l $txmd $nuro $achn $royl $useg $dgaz $grpn $live $oncy $camt","link":"http://stocktwits.com/Relentlessiam/message/24443686"},"provider":{"displayName":"StockTwits","link":"http://stocktwits.com"},"link":"http://stocktwits.com/Relentlessiam/message/24443686","entities":{"stocks":[{"displayName":"Achillion Pharmaceuticals, Inc.","stocktwits_id":718,"symbol":"ACHN","exchange":"NASDAQ","industry":"Biotechnology","sector":"Healthcare","trending":false},{"displayName":"Camtek Ltd.","stocktwits_id":1192,"symbol":"CAMT","exchange":"NASDAQ","industry":"Semiconductor - Integrated Circuits","sector":"Technology","trending":false},{"displayName":"LiveDeal, Inc.","stocktwits_id":2508,"symbol":"LIVE","exchange":"NASDAQ","industry":"Internet Information Providers","sector":"Technology","trending":false},{"displayName":"NeuroMetrix Inc.","stocktwits_id":2920,"symbol":"NURO","exchange":"NASDAQ","industry":"Medical Instruments & Supplies","sector":"Healthcare","trending":false},{"displayName":"Oncolytics Biotech Inc.","stocktwits_id":2983,"symbol":"ONCY","exchange":"NASDAQ","industry":"Biotechnology","sector":"Healthcare","trending":false},{"displayName":"Royale Energy Inc.","stocktwits_id":3414,"symbol":"ROYL","exchange":"NASDAQ","industry":"Independent Oil & Gas","sector":"Basic Materials","trending":false},{"displayName":"US Energy Corp.","stocktwits_id":3971,"symbol":"USEG","exchange":"NASDAQ","industry":"Independent Oil & Gas","sector":"Basic Materials","trending":false},{"displayName":"Groupon","stocktwits_id":8404,"symbol":"GRPN","exchange":"NASDAQ","industry":"Internet Information Providers","sector":"Technology","trending":true},{"displayName":"VelocityShares 3x Inverse Natural Gas ETN","stocktwits_id":11298,"symbol":"DGAZ","exchange":"NYSEArca","industry":"Exchange Traded Fund","sector":"Financial","trending":false},{"displayName":"TherapeuticsMD Inc.","stocktwits_id":11596,"symbol":"TXMD","exchange":"NYSEMkt","industry":null,"sector":null,"trending":false}],"chart":null,"sentiment":null,"video":null},"gnip":{"language":{"value":"en"}}}\r\n"""


class Teststocktwits(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        Stocktwits (Activity Streams) constructor takes five args - create one example of each for 
        use in all tests (loop over the self.objs list).
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular cases
        self.objs = { 
                    "base": StacsCSV(self.delim, None, False, False, False)
                    , "user": StacsCSV(self.delim, None, True, False, False) 
                    , "struct": StacsCSV(self.delim, None, False, True, False) 
                    , "influence": StacsCSV(self.delim, None, False, True, False) 
                    , "all": StacsCSV(self.delim, True, True, True, False) 
                    , "keypath": StacsCSV(self.delim, False, False, False, "source:title") 
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
                            + self.influence_length \
                            + self.struct_length 


    def tearDown(self):
        """
        """
        pass

    
    #
    # helpful to group test methods that are related into sections
    #
    
    def test_reader(self):
        """Test that our file_reader method is working as expected."""
        # grab the base instance 
        o = self.objs["base"]
        
        # without eg a for loop, we use the generator's next() method 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 


    def test_sample_data(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        stocktwits_native_sample.json example file without raising an Exception.
        """
        # get a temporary object
        tmp = self.objs["base"]

        # grab the correct data file 
        datafile = "./data/stocktwits_sample.json"

        # loop over all test stocktwits processing objects
        for o in self.objs.values():
            # loop over records in test file 
            for i, record in o.file_reader(datafile):
                # if there's a problem parsing, this method will raise an Exception
                record_string = o.procRecord(record)


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

    def test_influence_length(self):
        """
        Check the number of fields being output. (Update the expected results when new 
        features are added to the module.)
        """
        # grab the right instance 
        o = self.objs["influence"]
        
        # ensure our file_reader has worked correctly 
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
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
        g = o.file_reader( json_string=VALID_ACTIVITY )
        self.assertIsInstance( g.next(), tuple ) 

        # use sample record above 
        for i, record in o.file_reader( json_string=VALID_ACTIVITY ):
            loop = True
            record_string = o.procRecord(record)
            # should have many extra fields now 
            self.assertEqual( len( record_string.split( self.delim ) )
                                , self.all_length 
                            )  



if __name__ == "__main__":
    unittest.main()
