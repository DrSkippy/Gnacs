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
## 17-241
VALID_ACTIVITY = """
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
### 17-241


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
                self.objs[name] = obj(valid_activity)
        # we need to preserve order so the tests match the answers
        self.objs = self.objs.items()
        # get some processing objects
        # delim
        #    , options.keypath
        #    , options.geo
        #    , options.user
        #    , options.rules
        #    , options.urls
        #    , options.lang
        #    , options.influence
        #    , options.struct
 
        args = ["|" 
                , None
                , False
                , False
                , False
                , False
                , False
                , False
                , False
            ]
        self.record_lengths = [
                3
                , 19
                , 22
                , 23
                , 26
                , 29
                , 34
                , 35        
            ]
        self.processing_objs = [TwacsCSV(*args)]
        for i in range(7):
            args[2+i] = True
            #print >>sys.stderr, args
            self.processing_objs.append(TwacsCSV(*args))

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
        twitter_sample.json example file without raising an Exception.
        """
        # grab the correct data file 
        # TODO: replace hard-coded path to file -- requires running test from acscsv/ dir
        datafile = "../data/twitter_sample.json"
        datafile = "./data/twitter_sample.json"

        # loop over all test twitter processing objects
        for j, o in enumerate(self.processing_objs):
            # loop over records in test file 
            for i, record in o.file_reader(datafile):
                # if there's a problem parsing, this method will raise an Exception
                record_string = o.procRecord(record)
                self.assertEquals(len(record_string.split("|")), self.record_lengths[j])
 
    def test_valid_objects(self):
        for n,x in self.objs:
            self.assertTrue(isinstance(x,acscsv._Field))
    
    def test_number_of_fields(self):
        self.assertEquals(len(self.objs), 70)

    def _test_field_values_(self):
        for n,x in self.objs:
            print "## path = ",x.path
            if len(x.path) == 0 :
                continue
            res = {x.path[-1]: None}
            for y in sorted(x.path, reverse=True)[1:]:
                res = {y:res}
            # test for values
            print "res.append(\"\"\"{}\"\"\")".format(x.value)
            # test for none
            #print "test_doc =",res
            #print "test_obj =",n,"(test_doc)"
            #print "self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')"

    def test_field_values(self):
        res = []
        ## 290-428
        ## path =  ['provider', 'displayName']
        res.append("""Twitter""")
        ## path =  ['actor', 'friendsCount']
        res.append(174)
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['gnip', 'matching_rules']
        res.append([{u'tag': None, u'value': u'(Chile) has:geo'}, {u'tag': None, u'value': u'(Brazil ) has:geo'}])
        ## path =  ['actor', 'listedCount']
        res.append(0)
        ## path =  ['generator', 'link']
        res.append("""http://twitter.com/download/iphone""")
        ## path =  ['favoritesCount']
        res.append(0)
        ## path =  ['location', 'twitter_country_code']
        res.append("""US""")
        ## path =  ['location', 'name']
        res.append("""Virginia""")
        ## path =  ['twitter_entities', 'media']
        res.append([{u'expanded_url': u'http://twitter.com/mokitwou_sigei/status/482946548071161857/photo/1', u'sizes': {u'small': {u'h': 453, u'w': 340, u'resize': u'fit'}, u'large': {u'h': 1024, u'w': 768, u'resize': u'fit'}, u'medium': {u'h': 800, u'w': 600, u'resize': u'fit'}, u'thumb': {u'h': 150, u'w': 150, u'resize': u'crop'}}, u'url': u'http://t.co/cT3lgNGwOi', u'media_url_https': u'https://pbs.twimg.com/media/BrPFU3ECcAAFpi6.jpg', u'id_str': u'482946547227717632', u'indices': [110, 132], u'media_url': u'http://pbs.twimg.com/media/BrPFU3ECcAAFpi6.jpg', u'type': u'photo', u'id': 482946547227717632, u'display_url': u'pic.twitter.com/cT3lgNGwOi'}])
        ## path =  ['actor', 'statusesCount']
        res.append(100)
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['twitter_lang']
        res.append("""en""")
        ## path =  ['actor', 'displayName']
        res.append("""Sam Sigei""")
        ## path =  ['body']
        res.append("""Brazil Vs chile #WorldCup and @GhettoRadio895 in the background. Can't miss #GNL  @djruffkenya @estherkagamba http://t.co/cT3lgNGwOi""")
        ## path =  ['actor', 'languages']
        res.append("""en""")
        ## path =  ['actor', 'id']
        res.append("""302411346""")
        ## path =  ['actor', 'utcOffset']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['location', 'displayName']
        res.append("""Virginia, USA""")
        ## path =  ['actor', 'link']
        res.append("""http://www.twitter.com/mokitwou_sigei""")
        ## path =  ['twitter_entities', 'urls']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['actor', 'postedTime']
        res.append("""2011-05-21T04:26:03.000Z""")
        ## path =  ['actor', 'preferredUsername']
        res.append("""mokitwou_sigei""")
        ## path =  ['twitter_entities', 'user_mentions']
        res.append([{u'indices': [30, 45], u'screen_name': u'GhettoRadio895', u'id': 36316250, u'name': u'Ghetto Radio', u'id_str': u'36316250'}, {u'indices': [82, 94], u'screen_name': u'djruffkenya', u'id': 339020526, u'name': u'DJ RUFF di CAPTAIN', u'id_str': u'339020526'}, {u'indices': [95, 109], u'screen_name': u'estherkagamba', u'id': 100987248, u'name': u'Esther Kagamba ', u'id_str': u'100987248'}])
        ## path =  ['provider', 'link']
        res.append("""http://www.twitter.com""")
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['location', 'link']
        res.append("""https://api.twitter.com/1.1/geo/id/5635c19c2b5078d1.json""")
        ## path =  ['geo', 'coordinates']
        res.append([37.36813165, -79.62764394])
        ## path =  []
        res.append("Tweet (482946548071161857)")
        ## path =  ['actor', 'objectType']
        res.append("""person""")
        ## path =  ['actor', 'favoritesCount']
        res.append(22)
        ## path =  ['objectType']
        res.append("""activity""")
        ## path =  ['id']
        res.append("""482946548071161857_2014-06-28T18:00:04_73""")
        ## path =  ['link']
        res.append("""http://twitter.com/mokitwou_sigei/statuses/482946548071161857""")
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['verb']
        res.append("""post""")
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['twitter_entities', 'symbols']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['object']
        res.append({u'link': u'http://twitter.com/mokitwou_sigei/statuses/482946548071161857', u'objectType': u'note', u'postedTime': u'2014-06-28T18:00:04.000Z', u'id': u'object:search.twitter.com,2005:482946548071161857', u'summary': u"Brazil Vs chile #WorldCup and @GhettoRadio895 in the background. Can't miss #GNL  @djruffkenya @estherkagamba http://t.co/cT3lgNGwOi"})
        ## path =  ['actor', 'summary']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['actor', 'followersCount']
        res.append(28)
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['twitter_entities', 'hashtags']
        res.append([{u'indices': [16, 25], u'text': u'WorldCup'}, {u'indices': [76, 80], u'text': u'GNL'}])
        ## path =  ['postedTime']
        res.append("""2014-06-28T18:00:04.000Z""")
        ## path =  ['twitter_filter_level']
        res.append("""medium""")
        ## path =  ['retweetCount']
        res.append(0)
        ## path =  ['generator', 'displayName']
        res.append("""Twitter for iPhone""")
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['actor', 'verified']
        res.append(False)
        ## path =  ['provider', 'objectType']
        res.append("""service""")
        ## path =  ['actor', 'links']
        res.append([{u'href': None, u'rel': u'me'}])
        ## path =  ['location', 'geo', 'coordinates']
        res.append([[-83.67529, 36.540739], [-83.67529, 39.466012], [-75.16644, 39.466012], [-75.16644, 36.540739]])
        ## path =  ['geo', 'type']
        res.append("""Point""")
        ## path =  ['location', 'geo', 'type']
        res.append("""Polygon""")
        ## path =  ['gnip', 'klout_profile', 'link']
        res.append("""http://klout.com/user/id/16607034464501326""")
        ## path =  ['actor', 'twitterTimeZone']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['gnip', 'klout_profile', 'klout_user_id']
        res.append("""16607034464501326""")
        ## path =  ['location', 'country_code']
        res.append("""United States""")
        ## path =  ['actor', 'image']
        res.append("""https://pbs.twimg.com/profile_images/432197756175003648/M_0WMna5_normal.jpeg""")
        ## path =  ['id']
        res.append("""482946548071161857""")
        ## path =  ['actor', 'location', 'objectType']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['gnip', 'klout_profile', 'topics']
        res.append([{u'displayName': u'Dwyane Wade', u'link': u'http://klout.com/topic/id/9219221220892054727', u'klout_topic_id': u'9219221220892054727'}, {u'displayName': u'Politics', u'link': u'http://klout.com/topic/id/8119426466902417284', u'klout_topic_id': u'8119426466902417284'}])
        ## path =  ['inReplyTo', 'link']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['gnip', 'language', 'value']
        res.append("""en""")
        ## path =  ['gnip', 'klout_score']
        res.append(13)
        ## path =  ['gnip', 'profileLocations']
        res.append("""GNIPEMPTYFIELD""")
        ## path =  ['gnip', 'urls']
        res.append([{u'url': u'http://t.co/cT3lgNGwOi', u'expanded_status': 200, u'expanded_url': u'http://twitter.com/mokitwou_sigei/status/482946548071161857/photo/1'}])
        ## path =  ['location', 'objectType']
        res.append("""place""")
        ## path =  ['actor', 'location', 'displayName']
        res.append("""GNIPEMPTYFIELD""")
        ## 289-428
        for x,t in zip(self.objs, res):
            #print t
            self.assertEquals(x[1].value, t)
 
    def test_none_value(self):
        ## 433-706 
        ## path =  ['provider', 'displayName']
        test_doc = {'displayName': {'displayName': None}}
        test_obj = Field_provider_displayname (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'friendsCount']
        test_doc = {'actor': {'friendsCount': None}}
        test_obj = Field_actor_friendscount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_displayname (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'matching_rules']
        test_doc = {'gnip': {'matching_rules': None}}
        test_obj = Field_gnip_rules (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'listedCount']
        test_doc = {'actor': {'listedCount': None}}
        test_obj = Field_actor_listedcount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['generator', 'link']
        test_doc = {'generator': {'link': None}}
        test_obj = Field_generator_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['favoritesCount']
        test_doc = {'favoritesCount': None}
        test_obj = Field_favoritescount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'twitter_country_code']
        test_doc = {'location': {'twitter_country_code': None}}
        test_obj = Field_location_twitter_country_code (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'name']
        test_doc = {'location': {'name': None}}
        test_obj = Field_location_name (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_entities', 'media']
        test_doc = {'media': {'media': None}}
        test_obj = Field_twitter_entities_media (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'statusesCount']
        test_doc = {'actor': {'statusesCount': None}}
        test_obj = Field_actor_statusesCount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_address_region (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_lang']
        test_doc = {'twitter_lang': None}
        test_obj = Field_twitter_lang (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'displayName']
        test_doc = {'actor': {'displayName': None}}
        test_obj = Field_actor_displayname (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['body']
        test_doc = {'body': None}
        test_obj = Field_body (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'languages']
        test_doc = {'actor': {'languages': None}}
        test_obj = Field_actor_language (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'id']
        test_doc = {'actor': {'id': None}}
        test_obj = Field_actor_id (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'utcOffset']
        test_doc = {'actor': {'utcOffset': None}}
        test_obj = Field_actor_utcoffset (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'displayName']
        test_doc = {'displayName': {'displayName': None}}
        test_obj = Field_location_displayname (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'link']
        test_doc = {'actor': {'link': None}}
        test_obj = Field_actor_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_entities', 'urls']
        test_doc = {'twitter_entities': {'urls': None}}
        test_obj = Field_twitter_entities_urls (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'postedTime']
        test_doc = {'actor': {'postedTime': None}}
        test_obj = Field_actor_postedtime (test_doc)
        self.assertEquals(test_obj.value, 'INVALID_DATE_FORMAT')
        ## path =  ['actor', 'preferredUsername']
        test_doc = {'actor': {'preferredUsername': None}}
        test_obj = Field_actor_preferredusername (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_entities', 'user_mentions']
        test_doc = {'twitter_entities': {'user_mentions': None}}
        test_obj = Field_twitter_entities_user_mentions (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['provider', 'link']
        test_doc = {'link': {'link': None}}
        test_obj = Field_provider_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_address_countrycode (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'link']
        test_doc = {'link': {'link': None}}
        test_obj = Field_location_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['geo', 'coordinates']
        test_doc = {'coordinates': {'coordinates': None}}
        test_obj = Field_geo_coordinates (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  []
        ## path =  ['actor', 'objectType']
        test_doc = {'actor': {'objectType': None}}
        test_obj = Field_actor_objecttype (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'favoritesCount']
        test_doc = {'actor': {'favoritesCount': None}}
        test_obj = Field_actor_favoritesCount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['objectType']
        test_doc = {'objectType': None}
        test_obj = Field_objecttype (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['link']
        test_doc = {'link': None}
        test_obj = Field_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_geo_coordinates (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['verb']
        test_doc = {'verb': None}
        test_obj = Field_verb (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_objecttype (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_entities', 'symbols']
        test_doc = {'symbols': {'symbols': None}}
        test_obj = Field_twitter_entities_symbols (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['object']
        test_doc = {'object': None}
        test_obj = Field_object (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'summary']
        test_doc = {'actor': {'summary': None}}
        test_obj = Field_actor_summary (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'followersCount']
        test_doc = {'actor': {'followersCount': None}}
        test_obj = Field_actor_followerscount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_address_subregion (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_entities', 'hashtags']
        test_doc = {'hashtags': {'hashtags': None}}
        test_obj = Field_twitter_entities_hashtags (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['postedTime']
        test_doc = {'postedTime': None}
        test_obj = Field_postedtime (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['twitter_filter_level']
        test_doc = {'twitter_filter_level': None}
        test_obj = Field_twitter_filter_level (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['retweetCount']
        test_doc = {'retweetCount': None}
        test_obj = Field_retweetcount (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['generator', 'displayName']
        test_doc = {'displayName': {'displayName': None}}
        test_obj = Field_generator_displayname (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_geo_type (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'verified']
        test_doc = {'actor': {'verified': None}}
        test_obj = Field_actor_verified (test_doc)
        self.assertEquals(test_obj.value, False)
        ## path =  ['provider', 'objectType']
        test_doc = {'objectType': {'objectType': None}}
        test_obj = Field_provider_objecttype (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'links']
        test_doc = {'actor': {'links': None}}
        test_obj = Field_actor_links (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'geo', 'coordinates']
        test_doc = {'coordinates': {'geo': {'coordinates': None}}}
        test_obj = Field_location_geo_coordinates (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['geo', 'type']
        test_doc = {'geo': {'type': None}}
        test_obj = Field_geo_type (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'geo', 'type']
        test_doc = {'geo': {'location': {'type': None}}}
        test_obj = Field_location_geo_type (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'klout_profile', 'link']
        test_doc = {'gnip': {'klout_profile': {'link': None}}}
        test_obj = Field_gnip_klout_profile_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'twitterTimeZone']
        test_doc = {'actor': {'twitterTimeZone': None}}
        test_obj = Field_actor_twittertimezone (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'klout_profile', 'klout_user_id']
        test_doc = {'gnip': {'klout_profile': {'klout_user_id': None}}}
        test_obj = Field_gnip_klout_profile_klout_user_id (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'country_code']
        test_doc = {'country_code': {'country_code': None}}
        test_obj = Field_location_country_code (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'image']
        test_doc = {'actor': {'image': None}}
        test_obj = Field_actor_image (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['id']
        test_doc = {'id': None}
        test_obj = Field_id (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'location', 'objectType']
        test_doc = {'actor': {'location': {'objectType': None}}}
        test_obj = Field_actor_location_objecttype (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'klout_profile', 'topics']
        test_doc = {'gnip': {'klout_profile': {'topics': None}}}
        test_obj = Field_gnip_klout_profile_topics (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['inReplyTo', 'link']
        test_doc = {'inReplyTo': {'link': None}}
        test_obj = Field_inreplyto_link (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_address_country (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'language', 'value']
        test_doc = {'gnip': {'language': {'value': None}}}
        test_obj = Field_gnip_language_value (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'klout_score']
        test_doc = {'gnip': {'klout_score': None}}
        test_obj = Field_gnip_klout_score (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'profileLocations']
        test_doc = {'gnip': {'profileLocations': None}}
        test_obj = Field_gnip_profilelocations_address_locality (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['gnip', 'urls']
        test_doc = {'gnip': {'urls': None}}
        test_obj = Field_gnip_urls (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['location', 'objectType']
        test_doc = {'location': {'objectType': None}}
        test_obj = Field_location_objecttype (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## path =  ['actor', 'location', 'displayName']
        test_doc = {'actor': {'displayName': {'displayName': None}}}
        test_obj = Field_actor_location_displayname (test_doc)
        self.assertEquals(test_obj.value, 'GNIPEMPTYFIELD')
        ## 433-706

if __name__ == "__main__":
    unittest.main()
