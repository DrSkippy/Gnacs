#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague, Fiona Pigott"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from newsgator_acs import *


# valid activity from source (eg from data/) 
VALID_ACTIVITY = '''{"id":"tag:gnip.newsgator.com:2012:feed/9073659/post/24254991653","postedTime":"2013-10-31T19:55:16+00:00","link":"http://tampa.craigslist.org/hil/syd/4163563239.html","verb":"post","actor":{},"object":{"displayName":"Samsung Series 7 Slate 11.6 64GB Cool New (Hillsborough County) $330","content":"The application works fantastic and you will perform lot of things using it. Look for rates, company trade device with great discount. Purchase Samsung Series 7 Slate 11.6 64GB.The screen is really great has true colors and excellent viewing angles.  [...]"},"ngState":"new","ngFeedScore":1,"ngFeedXmlUrl":"http://tampa.craigslist.org/search/sya?query=ipad&amp;srchType=A&amp;format=rss","ngModifiedDate":"Fri, 01 Nov 2013 15:37:35 GMT","ngFeedId":9073659,"ngPostId":24254991653,"ngScore":0,"original_item":{"ng:feedScore":1,"guid":"http://tampa.craigslist.org/hil/syd/4163563239.html","pubDate":"Thu, 31 Oct 2013 19:55:16 GMT","title":"Samsung Series 7 Slate 11.6 64GB Cool New (Hillsborough County) $330","ng:feedXmlUrl":"http://tampa.craigslist.org/search/sya?query=ipad&amp;srchType=A&amp;format=rss","attributes":{"ng:state":"new"},"ng:modifiedDate":"Fri, 01 Nov 2013 15:37:35 GMT","ng:feedId":9073659,"ng:text":{},"ng:postId":24254991653,"description":"The application works fantastic and you will perform lot of things using it. Look for rates, company trade device with great discount. Purchase Samsung Series 7 Slate 11.6 64GB.The screen is really great has true colors and excellent viewing angles.  [...]","link":"http://tampa.craigslist.org/hil/syd/4163563239.html","ng:score":0},"gnip":{}}'''

class TestNewsgatorAcs(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular object cases
        self.objs = { 
                    "base": NGacsCSV(self.delim, None, False, False) 
                    , "urls": NGacsCSV(self.delim, None, True, False)
                    , "user": NGacsCSV(self.delim, None, False, True)
                    , "all": NGacsCSV(self.delim, None, True, True)
                    , "keypath": NGacsCSV(self.delim,"original_item,attributes,ng:state",False,False)
            }        
        # set any instance attributes here, avoid hard-coding in test methods 
        self.lengths = { "base": 3, "urls": 5, "user": 4, "all": 6, "keypath": 4}

    def tearDown(self):
        """
        """
        pass

    
    #
    # helpful to group test methods that are related into sections
    #
    
    def test_sample_data(self):
        """
        Check that we can use each test object's procRecord method on each record in the 
        newsgator_sample.json example file without raising an exception."""
        # get a temporary object
        tmp = self.objs["base"]

        # grab the correct data file
        datafile = "./data/newsgator_sample.json"
        
        # loop over all of the test newsgator processing objects
        for o in self.objs.values():
            # loop over records in a test file
            for i, record in o.file_reader(datafile):
                # if there's a problem parsing, this should raise an Exception
                record_string = o.procRecord(record)
                #print record_string

    def test_reader(self):
        """Test that our file_reader method is working as expected"""
        # grab the base instance
        o = self.objs["base"]

        # without eg for a loop, use .next()
        g = o.file_reader(json_string = VALID_ACTIVITY)
        self.assertIsInstance(g.next(), tuple)

    def test_lengths(self):
        """ Check the number of fields being output """
        for key in self.objs.keys():
            o = self.objs[key]
            for i, record in o.file_reader(json_string = VALID_ACTIVITY):
                failure_msg = "failed while testing the length of the {} case output".format(key)
                # procRecord returns a delimited string
                record_string = o.procRecord(record)
                self.assertEqual(len(record_string.split(self.delim)), self.lengths[key], failure_msg)
        
    def test_user_fields(self):
        """ Test for non-None values in a good record when using the 'user' option,
        and None values in an intentionally damaged record"""
        GOOD_USER_STRING = """{"id":"tag:gnip.newsgator.com:2012:feed/9072310/post/24254991675","postedTime":"2013-10-31T18:46:09+00:00","link":"magnet:?xt=urn:btih:3CC1E15CD7DDF8480F47391273C60D6E63E6AAD2&dn=NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","verb":"post","actor":{"displayName":"DVD-Uploader"},"object":{"displayName":"NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","content":"","tags":[{"displayName":"Video / Movies DVDR"}],"comments":{"link":"http://thepiratebay.sx/torrent/9127508"}},"ngState":"new","ngFeedScore":10,"ngFeedXmlUrl":"http://rss.thepiratebay.se/202","ngModifiedDate":"Fri, 01 Nov 2013 15:37:37 GMT","ngFeedId":9072310,"ngPostId":24254991675,"ngScore":0,"original_item":{"category":"Video / Movies DVDR","ng:feedScore":10,"author":"DVD-Uploader","comments":"http://thepiratebay.sx/torrent/9127508","guid":"http://thepiratebay.sx/torrent/9127508/","pubDate":"Thu, 31 Oct 2013 18:46:09 GMT","title":"NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","ng:feedXmlUrl":"http://rss.thepiratebay.se/202","attributes":{"ng:state":"new"},"ng:modifiedDate":"Fri, 01 Nov 2013 15:37:37 GMT","ng:feedId":9072310,"ng:text":{},"ng:postId":24254991675,"description":"","link":"magnet:?xt=urn:btih:3CC1E15CD7DDF8480F47391273C60D6E63E6AAD2&dn=NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","ng:score":0},"gnip":{}}""" 
        
        USER_STRING_W_NULL = """{"id":"tag:gnip.newsgator.com:2012:feed/9072310/post/24254991675","postedTime":"2013-10-31T18:46:09+00:00","link":"magnet:?xt=urn:btih:3CC1E15CD7DDF8480F47391273C60D6E63E6AAD2&dn=NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","verb":"post","actor":{"displayName":null},"object":{"displayName":"NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","content":"","tags":[{"displayName":"Video / Movies DVDR"}],"comments":{"link":"http://thepiratebay.sx/torrent/9127508"}},"ngState":"new","ngFeedScore":10,"ngFeedXmlUrl":"http://rss.thepiratebay.se/202","ngModifiedDate":"Fri, 01 Nov 2013 15:37:37 GMT","ngFeedId":9072310,"ngPostId":24254991675,"ngScore":0,"original_item":{"category":"Video / Movies DVDR","ng:feedScore":10,"author":"DVD-Uploader","comments":"http://thepiratebay.sx/torrent/9127508","guid":"http://thepiratebay.sx/torrent/9127508/","pubDate":"Thu, 31 Oct 2013 18:46:09 GMT","title":"NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","ng:feedXmlUrl":"http://rss.thepiratebay.se/202","attributes":{"ng:state":"new"},"ng:modifiedDate":"Fri, 01 Nov 2013 15:37:37 GMT","ng:feedId":9072310,"ng:text":{},"ng:postId":24254991675,"description":"","link":"magnet:?xt=urn:btih:3CC1E15CD7DDF8480F47391273C60D6E63E6AAD2&dn=NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","ng:score":0},"gnip":{}}"""
        
        USER_STRING_WO_FIELD =  """{"id":"tag:gnip.newsgator.com:2012:feed/9072310/post/24254991675","postedTime":"2013-10-31T18:46:09+00:00","link":"magnet:?xt=urn:btih:3CC1E15CD7DDF8480F47391273C60D6E63E6AAD2&dn=NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","verb":"post","actor":{"BAD_displayName": "DVD-Uploader"},"object":{"displayName":"NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","content":"","tags":[{"displayName":"Video / Movies DVDR"}],"comments":{"link":"http://thepiratebay.sx/torrent/9127508"}},"ngState":"new","ngFeedScore":10,"ngFeedXmlUrl":"http://rss.thepiratebay.se/202","ngModifiedDate":"Fri, 01 Nov 2013 15:37:37 GMT","ngFeedId":9072310,"ngPostId":24254991675,"ngScore":0,"original_item":{"category":"Video / Movies DVDR","ng:feedScore":10,"author":"DVD-Uploader","comments":"http://thepiratebay.sx/torrent/9127508","guid":"http://thepiratebay.sx/torrent/9127508/","pubDate":"Thu, 31 Oct 2013 18:46:09 GMT","title":"NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","ng:feedXmlUrl":"http://rss.thepiratebay.se/202","attributes":{"ng:state":"new"},"ng:modifiedDate":"Fri, 01 Nov 2013 15:37:37 GMT","ng:feedId":9072310,"ng:text":{},"ng:postId":24254991675,"description":"","link":"magnet:?xt=urn:btih:3CC1E15CD7DDF8480F47391273C60D6E63E6AAD2&dn=NCIS.S10.MULTiSUBS.PAL.DVDR-Winters","ng:score":0},"gnip":{}}"""
        
        o = self.objs["user"]

        # this should have data
        failure_msg = "There should have been data in this field, but there wasn't (or the data that was there was wrong)"
        for i, record in o.file_reader(json_string = GOOD_USER_STRING):
            record_string = o.procRecord(record)
            self.assertNotEqual("None", record_string.split(self.delim)[-1], failure_msg)
            self.assertEqual("DVD-Uploader" , record_string.split(self.delim)[-1], failure_msg)

        # this should not have data (the field is null)
        failure_msg = "Seems like a JSON 'null' value is not being converted to a Python 'None' value"
        for i, record in o.file_reader(json_string = USER_STRING_W_NULL):
            record_string = o.procRecord(record)
            # payload JSON null => python None => check
            self.assertEqual("None", record_string.split(self.delim)[-1], failure_msg)
            
        # this shouldn't have data either (the field is missing)
        failure_msg = "Seems like missing fields are not being returned as 'None'"
        for i, record in o.file_reader(json_string = USER_STRING_WO_FIELD):
            record_string = o.procRecord(record)
            # payload has a 'None' where the missing string was
            self.assertEqual("None", record_string.split(self.delim)[-1], failure_msg)

    def test_keypath(self):
        """ Test for correct values in the specified keypath"""
        o = self.objs['keypath']

        KEYPATH_WO_PATH = '''{"id":"tag:gnip.newsgator.com:2012:feed/9073659/post/24254991653","postedTime":"2013-10-31T19:55:16+00:00","link":"http://tampa.craigslist.org/hil/syd/4163563239.html","verb":"post","actor":{},"object":{"displayName":"Samsung Series 7 Slate 11.6 64GB Cool New (Hillsborough County) $330","content":"The application works fantastic and you will perform lot of things using it. Look for rates, company trade device with great discount. Purchase Samsung Series 7 Slate 11.6 64GB.The screen is really great has true colors and excellent viewing angles.  [...]"},"ngState":"new","ngFeedScore":1,"ngFeedXmlUrl":"http://tampa.craigslist.org/search/sya?query=ipad&amp;srchType=A&amp;format=rss","ngModifiedDate":"Fri, 01 Nov 2013 15:37:35 GMT","ngFeedId":9073659,"ngPostId":24254991653,"ngScore":0,"original_item":{"ng:feedScore":1,"guid":"http://tampa.craigslist.org/hil/syd/4163563239.html","pubDate":"Thu, 31 Oct 2013 19:55:16GMT","title":"Samsung Series 7 Slate 11.6 64GB Cool New (Hillsborough County) $330","ng:feedXmlUrl":"http://tampa.craigslist.org/search/sya?query=ipad&amp;srchType=A&amp;format=rss","ng:modifiedDate":"Fri, 01 Nov 2013 15:37:35 GMT","ng:feedId":9073659,"ng:text":{},"ng:postId":24254991653,"description":"The application works fantastic and you will perform lot of things using it. Look for rates, company trade device with great discount. Purchase Samsung Series 7 Slate 11.6 64GB.The screen is really great has true colors and excellent viewing angles.  [...]","link":"http://tampa.craigslist.org/hil/syd/4163563239.html","ng:score":0},"gnip":{}}'''

        KEYPATH_WO_FIELD = '''{"id":"tag:gnip.newsgator.com:2012:feed/9073659/post/24254991653","postedTime":"2013-10-31T19:55:16+00:00","link":"http://tampa.craigslist.org/hil/syd/4163563239.html","verb":"post","actor":{},"object":{"displayName":"Samsung Series 7 Slate 11.6 64GB Cool New (Hillsborough County) $330","content":"The application works fantastic and you will perform lot of things using it. Look for rates, company trade device with great discount. Purchase Samsung Series 7 Slate 11.6 64GB.The screen is really great has true colors and excellent viewing angles.  [...]"},"ngState":"new","ngFeedScore":1,"ngFeedXmlUrl":"http://tampa.craigslist.org/search/sya?query=ipad&amp;srchType=A&amp;format=rss","ngModifiedDate":"Fri, 01 Nov 2013 15:37:35 GMT","ngFeedId":9073659,"ngPostId":24254991653,"ngScore":0,"original_item":{"ng:feedScore":1,"guid":"http://tampa.craigslist.org/hil/syd/4163563239.html","pubDate":"Thu, 31 Oct 2013 19:55:16GMT","title":"Samsung Series 7 Slate 11.6 64GB Cool New (Hillsborough County) $330","ng:feedXmlUrl":"http://tampa.craigslist.org/search/sya?query=ipad&amp;srchType=A&amp;format=rss","attributes":{},"ng:modifiedDate":"Fri, 01 Nov 2013 15:37:35 GMT","ng:feedId":9073659,"ng:text":{},"ng:postId":24254991653,"description":"The application works fantastic and you will perform lot of things using it. Look for rates, company trade device with great discount. Purchase Samsung Series 7 Slate 11.6 64GB.The screen is really great has true colors and excellent viewing angles.  [...]","link":"http://tampa.craigslist.org/hil/syd/4163563239.html","ng:score":0},"gnip":{}}'''

        # this should have data
        failure_msg = "Looks like the parser never found the specified kaypath"
        for i, record in o.file_reader(json_string = VALID_ACTIVITY):
            record_string = o.procRecord(record)
            self.assertEqual("new", record_string.split(self.delim)[-1], failure_msg)

        # this should not have data
        failure_msg = "A missing path is evaluating to something other than 'PATH_EMPTY'"
        for i, record in o.file_reader(json_string = KEYPATH_WO_FIELD):
            record_string = o.procRecord(record)
            self.assertEqual("PATH_EMPTY", record_string.split(self.delim)[-1], failure_msg)

        # this should not have data
        failure_msg = "A missing field is evaluating to something other than 'PATH_EMPTY'"
        for i, record in o.file_reader(json_string = KEYPATH_WO_FIELD):
            record_string = o.procRecord(record)
            self.assertEqual("PATH_EMPTY", record_string.split(self.delim)[-1], failure_msg)

if __name__ == "__main__":
    unittest.main()
