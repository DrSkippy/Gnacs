#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import inspect
import unittest
import json
from StringIO import StringIO
from twitter_acs import *
import  acscsv 


# valid activity from source (eg from data/) 
VALID_ACTIVITY ="""
{
   "body": "Brazil Vs chile #WorldCup and @GhettoRadio895 in the background. Can't miss #GNL  @djruffkenya @estherkagamba http://t.co/cT3lgNGwOi", 
   "retweetCount": 0, 
   "generator": {
      "link": "http://twitter.com/download/iphone", 
      "displayName": "Twitter for iPhone"
   }, 
   "twitter_filter_level": "medium", 
   "geo": {
      "type": "Point", 
      "coordinates": [
         37.36813165, 
         -79.62764394
      ]
   }, 
   "favoritesCount": 0, 
   "object": {
      "postedTime": "2014-06-28T18:00:04.000Z", 
      "summary": "Brazil Vs chile #WorldCup and @GhettoRadio895 in the background. Can't miss #GNL  @djruffkenya @estherkagamba http://t.co/cT3lgNGwOi", 
      "link": "http://twitter.com/mokitwou_sigei/statuses/482946548071161857", 
      "id": "object:search.twitter.com,2005:482946548071161857", 
      "objectType": "note"
   }, 
   "actor": {
      "preferredUsername": "mokitwou_sigei", 
      "displayName": "Sam Sigei", 
      "links": [
         {
            "href": null, 
            "rel": "me"
         }
      ], 
      "twitterTimeZone": null, 
      "image": "https://pbs.twimg.com/profile_images/432197756175003648/M_0WMna5_normal.jpeg", 
      "verified": false, 
      "statusesCount": 100, 
      "summary": null, 
      "languages": [
         "en"
      ], 
      "utcOffset": null, 
      "link": "http://www.twitter.com/mokitwou_sigei", 
      "followersCount": 28, 
      "favoritesCount": 22, 
      "friendsCount": 174, 
      "listedCount": 0, 
      "postedTime": "2011-05-21T04:26:03.000Z", 
      "id": "id:twitter.com:302411346", 
      "objectType": "person"
   }, 
   "twitter_lang": "en", 
   "twitter_entities": {
      "symbols": [], 
      "user_mentions": [
         {
            "id": 36316250, 
            "indices": [
               30, 
               45
            ], 
            "id_str": "36316250", 
            "screen_name": "GhettoRadio895", 
            "name": "Ghetto Radio"
         }, 
         {
            "id": 339020526, 
            "indices": [
               82, 
               94
            ], 
            "id_str": "339020526", 
            "screen_name": "djruffkenya", 
            "name": "DJ RUFF di CAPTAIN"
         }, 
         {
            "id": 100987248, 
            "indices": [
               95, 
               109
            ], 
            "id_str": "100987248", 
            "screen_name": "estherkagamba", 
            "name": "Esther Kagamba "
         }
      ], 
      "hashtags": [
         {
            "indices": [
               16, 
               25
            ], 
            "text": "WorldCup"
         }, 
         {
            "indices": [
               76, 
               80
            ], 
            "text": "GNL"
         }
      ], 
      "urls": [], 
      "media": [
         {
            "expanded_url": "http://twitter.com/mokitwou_sigei/status/482946548071161857/photo/1", 
            "display_url": "pic.twitter.com/cT3lgNGwOi", 
            "url": "http://t.co/cT3lgNGwOi", 
            "media_url_https": "https://pbs.twimg.com/media/BrPFU3ECcAAFpi6.jpg", 
            "id_str": "482946547227717632", 
            "sizes": {
               "small": {
                  "h": 453, 
                  "resize": "fit", 
                  "w": 340
               }, 
               "large": {
                  "h": 1024, 
                  "resize": "fit", 
                  "w": 768
               }, 
               "medium": {
                  "h": 800, 
                  "resize": "fit", 
                  "w": 600
               }, 
               "thumb": {
                  "h": 150, 
                  "resize": "crop", 
                  "w": 150
               }
            }, 
            "indices": [
               110, 
               132
            ], 
            "type": "photo", 
            "id": 482946547227717632, 
            "media_url": "http://pbs.twimg.com/media/BrPFU3ECcAAFpi6.jpg"
         }
      ]
   }, 
   "verb": "post", 
   "link": "http://twitter.com/mokitwou_sigei/statuses/482946548071161857", 
   "location": {
      "displayName": "Virginia, USA", 
      "name": "Virginia", 
      "link": "https://api.twitter.com/1.1/geo/id/5635c19c2b5078d1.json", 
      "twitter_country_code": "US", 
      "country_code": "United States", 
      "geo": {
         "type": "Polygon", 
         "coordinates": [
            [
               [
                  -83.67529, 
                  36.540739
               ], 
               [
                  -83.67529, 
                  39.466012
               ], 
               [
                  -75.16644, 
                  39.466012
               ], 
               [
                  -75.16644, 
                  36.540739
               ]
            ]
         ]
      }, 
      "objectType": "place"
   }, 
   "provider": {
      "link": "http://www.twitter.com", 
      "displayName": "Twitter", 
      "objectType": "service"
   }, 
   "postedTime": "2014-06-28T18:00:04.000Z", 
   "id": "tag:search.twitter.com,2005:482946548071161857", 
   "gnip": {
      "klout_profile": {
         "link": "http://klout.com/user/id/16607034464501326", 
         "topics": [
            {
               "link": "http://klout.com/topic/id/9219221220892054727", 
               "displayName": "Dwyane Wade", 
               "klout_topic_id": "9219221220892054727"
            }, 
            {
               "link": "http://klout.com/topic/id/8119426466902417284", 
               "displayName": "Politics", 
               "klout_topic_id": "8119426466902417284"
            }
         ], 
         "klout_user_id": "16607034464501326"
      }, 
      "klout_score": 13, 
      "matching_rules": [
         {
            "tag": null, 
            "value": "(Chile) has:geo"
         }, 
         {
            "tag": null, 
            "value": "(Brazil ) has:geo"
         }
      ], 
      "language": {
         "value": "en"
      }, 
      "urls": [
         {
            "url": "http://t.co/cT3lgNGwOi", 
            "expanded_status": 200, 
            "expanded_url": "http://twitter.com/mokitwou_sigei/status/482946548071161857/photo/1"
         }
      ]
   }, 
   "objectType": "activity"
}
"""


class TestTwitter_acs(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        """ 

        self.delim = '|'
        valid_activity = json.loads(VALID_ACTIVITY)
        self.objs = {}
        # use a dict to make it easier to refer to the particular object cases
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if name.startswith("Field_"):
                self.objs[name.lower()+"_"] = obj(valid_activity)

    def tearDown(self):
        """
        """
        pass
    
    #
    # helpful to group test methods that are related into sections
    #
    
    def test_valid_objects(self):
        for x in self.objs.values():
            self.assertTrue(isinstance(x,acscsv._Field))
    
    def test_number_of_fields(self):
        self.assertEquals(len(self.objs), 69)

    def test_field_values_(self):
        for x in self.objs.values():
            print "res.append(\"\"\"{}\"\"\")".format(x.value)
            print x.path

    def test_field_values(self):
        res = []
        res.append("""https://api.twitter.com/1.1/geo/id/5635c19c2b5078d1.json""")
        res.append("""Polygon""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""http://www.twitter.com""")
        res.append("""en""")
        res.append([{u'href': None, u'rel': u'me'}])
        res.append("""2011-05-21T04:26:03.000Z""")
        res.append(13)
        res.append("""https://pbs.twimg.com/profile_images/432197756175003648/M_0WMna5_normal.jpeg""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""16607034464501326""")
        res.append([{u'expanded_url': u'http://twitter.com/mokitwou_sigei/status/482946548071161857/photo/1', u'sizes': {u'small': {u'h': 453, u'w': 340, u'resize': u'fit'}, u'large': {u'h': 1024, u'w': 768, u'resize': u'fit'}, u'medium': {u'h': 800, u'w': 600, u'resize': u'fit'}, u'thumb': {u'h': 150, u'w': 150, u'resize': u'crop'}}, u'url': u'http://t.co/cT3lgNGwOi', u'media_url_https': u'https://pbs.twimg.com/media/BrPFU3ECcAAFpi6.jpg', u'id_str': u'482946547227717632', u'indices': [110, 132], u'media_url': u'http://pbs.twimg.com/media/BrPFU3ECcAAFpi6.jpg', u'type': u'photo', u'id': 482946547227717632, u'display_url': u'pic.twitter.com/cT3lgNGwOi'}])
        res.append("""Tweet (482946548071161857)""")
        res.append([{u'tag': None, u'value': u'(Chile) has:geo'}, {u'tag': None, u'value': u'(Brazil ) has:geo'}])
        res.append("""482946548071161857""")
        res.append(22)
        res.append([{u'indices': [30, 45], u'screen_name': u'GhettoRadio895', u'id': 36316250, u'name': u'Ghetto Radio', u'id_str': u'36316250'}, {u'indices': [82, 94], u'screen_name': u'djruffkenya', u'id': 339020526, u'name': u'DJ RUFF di CAPTAIN', u'id_str': u'339020526'}, {u'indices': [95, 109], u'screen_name': u'estherkagamba', u'id': 100987248, u'name': u'Esther Kagamba ', u'id_str': u'100987248'}])
        res.append(100)
        res.append(0)
        res.append([[-83.67529, 36.540739], [-83.67529, 39.466012], [-75.16644, 39.466012], [-75.16644, 36.540739]])
        res.append("""http://klout.com/user/id/16607034464501326""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""Sam Sigei""")
        res.append("""Virginia, USA""")
        res.append(0)
        res.append(174)
        res.append("""GNIPEMPTYFIELD""")
        res.append("""en""")
        res.append("""GNIPEMPTYFIELD""")
        res.append([{u'displayName': u'Dwyane Wade', u'link': u'http://klout.com/topic/id/9219221220892054727', u'klout_topic_id': u'9219221220892054727'}, {u'displayName': u'Politics', u'link': u'http://klout.com/topic/id/8119426466902417284', u'klout_topic_id': u'8119426466902417284'}])
        res.append("""GNIPEMPTYFIELD""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""medium""")
        res.append("""http://twitter.com/download/iphone""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""person""")
        res.append("""Point""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""302411346""")
        res.append("""activity""")
        res.append("""mokitwou_sigei""")
        res.append("""GNIPEMPTYFIELD""")
        res.append([])
        res.append(False)
        res.append("""Brazil Vs chile #WorldCup and @GhettoRadio895 in the background. Can't miss #GNL  @djruffkenya @estherkagamba http://t.co/cT3lgNGwOi""")
        res.append("""http://www.twitter.com/mokitwou_sigei""")
        res.append([])
        res.append([37.36813165, -79.62764394])
        res.append("""US""")
        res.append("""en""")
        res.append("""GNIPEMPTYFIELD""")
        res.append([{u'indices': [16, 25], u'text': u'WorldCup'}, {u'indices': [76, 80], u'text': u'GNL'}])
        res.append("""GNIPEMPTYFIELD""")
        res.append("""place""")
        res.append({u'link': u'http://twitter.com/mokitwou_sigei/statuses/482946548071161857', u'objectType': u'note', u'postedTime': u'2014-06-28T18:00:04.000Z', u'id': u'object:search.twitter.com,2005:482946548071161857', u'summary': u"Brazil Vs chile #WorldCup and @GhettoRadio895 in the background. Can't miss #GNL  @djruffkenya @estherkagamba http://t.co/cT3lgNGwOi"})
        res.append("""service""")
        res.append("""http://twitter.com/mokitwou_sigei/statuses/482946548071161857""")
        res.append("""GNIPEMPTYFIELD""")
        res.append("""post""")
        res.append([{u'url': u'http://t.co/cT3lgNGwOi', u'expanded_status': 200, u'expanded_url': u'http://twitter.com/mokitwou_sigei/status/482946548071161857/photo/1'}])
        res.append("""2014-06-28T18:00:04.000Z""")
        res.append(0)
        res.append(28)
        res.append("""Twitter for iPhone""")
        res.append("""Twitter""")
        res.append("""United States""")
        res.append("""Virginia""")
        for x,t in zip(self.objs.values(), res):
            self.assertEquals(x.value, t)

 
if __name__ == "__main__":
    unittest.main()
