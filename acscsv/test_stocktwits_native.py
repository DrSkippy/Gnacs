#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague, Fiona Pigott"
__license__="Simplified BSD"

import sys
from stocktwits_native import *
import unittest
from StringIO import StringIO


nice_string = """{"id":12802603,"body":"&quot;Hard knocks have a place and value, but hard thinking goes farther in less time.&quot; - Henry Ford","created_at":"2013-04-01T00:32:06Z","user":{"id":76647,"username":"TradingPlays","name":"Paul Elliott","avatar_url":"http://avatars.stocktwits.net/production/76647/thumb-1348961241.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/76647/thumb-1348961241.png","identity":"User","classification":[],"join_date":"2011-05-07","followers":273,"following":52,"ideas":3002,"following_stocks":0,"location":"USA","bio":"Proprietary stock trader, specializing in active intraday trading strategies.","website_url":"http://www.tradingplays.com","trading_strategy":{"assets_frequently_traded":["Equities"],"approach":"Momentum","holding_period":"Day Trader","experience":"Professional"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"entities":{"sentiment":null}}"""


class TestStocktwitsNative(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        # create one of each 
        delim = '|'
        self.objs = [ 
                        StocktwitsNative(delim, None, True, False, False)
                        , StocktwitsNative(delim, None, False, True, False)
                        , StocktwitsNative(delim, None, False, False, True) 
                        , StocktwitsNative(delim, None, True, True, True) 
                    ]

    def tearDown(self):
        pass


    def test_data(self):
        """
        Parse all the files in data/ without raising any Exception. 

        This test method should be included in all pub-specific test modules. 
        """
        obj = self.objs[-1]

        filename = "../data/{}_sample.json".format(obj.__module__)  

        # use the last St... object
        for i, record in obj.file_reader(filename):
            a = obj.procRecord(record)






    def test_body(self):
        
        evil_string = """{"id":12802603,"EVIL_body":"&quot;Hard knocks have a place and value, but hard thinking goes farther in less time.&quot; - Henry Ford","created_at":"2013-04-01T00:32:06Z","user":{"id":76647,"username":"TradingPlays","name":"Paul Elliott","avatar_url":"http://avatars.stocktwits.net/production/76647/thumb-1348961241.png","avatar_url_ssl":"https://s3.amazonaws.com/st-avatars/production/76647/thumb-1348961241.png","identity":"User","classification":[],"join_date":"2011-05-07","followers":273,"following":52,"ideas":3002,"following_stocks":0,"location":"USA","bio":"Proprietary stock trader, specializing in active intraday trading strategies.","website_url":"http://www.tradingplays.com","trading_strategy":{"assets_frequently_traded":["Equities"],"approach":"Momentum","holding_period":"Day Trader","experience":"Professional"}},"source":{"id":1,"title":"StockTwits","url":"http://stocktwits.com"},"entities":{"sentiment":null}}"""

        for obj in self.objs:
            for i, record in obj.file_reader(StringIO(evil_string)):
                self.assertEqual(12802603, record["id"]) 
                self.assertEqual("None", record["body"]) 
        
        
        



if __name__ == "__main__":
    unittest.main()
