#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from wordpress_acs import *


# valid activity from source (eg from data/) 
VALID_ACTIVITY = """{"id":"tag:gnip.wordpress.com:2012:blog/4885073/post/1089","verb":"post","target":{"summary":"(by jskr)","link":"http://300slow.wordpress.com/","feed":"http://300slow.wordpress.com/feed/","wpBlogId":4885073,"displayName":"300słow","objectType":"blog"},"postedTime":"2013-05-25T15:43:06.000Z","provider":{"link":"http://im.wordpress.com:8008/posts.json","displayName":"WordPress","objectType":"service"},"object":{"id":"article:wordpress.com:4885073:1089","content":"o już czasu jestem, pod dużym wrażeniem sposobów jakimi kościół próbuje mnie rozbawić.  Co najważniejsze, czyni to skutecznie i wręcz czoła chylę przed ich pomysłowością. Mistrzami są zaś w tak zwanym wykręcaniu kota ogonem. Oto jeden z ostatnich przykładow. Jef Kloch, rzecznik tzw. episkopatu odpowiedział wreszcie na pytania dziennikarzy (milczał jak skała przez niemal dwa miesiące) dotyczące pedofilii w polskim kościele. Co odpowiedział? Że kościół nie zbiera informacji na temat nadużyć księży. Oznacza to, że nie zna (przynajmniej oficjalnie) skali tego problemu. Ale wcale nie to jest najśmieszniejsze. Bo pytany dalej dlaczego to nie zbierają tych informacji, ksiądz Kloch z miną pokerzysty odpowiada, że danych tych nie zbierają ze względu na dobro osób pokrzywdzonych to dopiero jest naprawdę śmieszne, wręcz zwala z nóg. Byłbym bardzo ciekaw przeto, na czym zdaniem pana Klocha to dobro pokrzywdzonych polega. Bo niezmiennie od dłuższego już czasu mam graniczące z pewnością przekonanie, że mówiąc o pokrzywdzonych, pan Kloch ma na myśli wyłącznie biednych, napastowanych seksulanie księży, prawdziwe ofiary pedofilii w kościele.  I co? Ręce wprost same składają się do oklasków.","summary":"Od d&#322;u&#380;szego ju&#380; czasu jestem, pod du&#380;ym wra&#380;eniem sposob&#243;w jakimi ko&#347;ci&#243;&#322; pr&#243;buje mnie rozbawi&#263;. &#160;Co najwa&#380;niejsze, czyni to skutecznie i wr&#281;cz czo&#322;a chyl&#281; przed ich pomys&#322;owo&#347;ci&#261;. Mistrzami s&#261; za&#347; w tak zwanym wykr&#281;caniu kota ogonem. Oto jeden z&#160;ostatnich przyk&#322;adow. Ksi&#261;dz J&#243;zef Kloch, rzecznik tzw. episkopatu odpowiedzia&#322; wreszcie na pytania dziennikarzy (milcza&#322; jak ska&#322;a przez niemal [&#8230;]","link":"http://300slow.wordpress.com/2013/05/25/co-kosciol-wie-a-czego-na-wszelki-wypadek-nie-wie/","postedTime":"2013-05-25T15:42:58Z","wpBlogId":4885073,"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","objectType":"article","updatedTime":"2013-05-25T15:42:58Z","wpPostId":1089},"actor":{"id":"person:wordpress.com:45337318","link":"http://gravatar.com/jerzysikora","wpEmailMd5":"dea3b3f6a8265868871a6e12a01a8cf9","displayName":"jsikora","objectType":"person"},"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","gnip":{"language":{"value":"pl"},"urls":[{"url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg","expanded_url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg"}]}}"""

class TestWordpress(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular object cases
        self.objs = { 
                    "base": WPacsCSV(self.delim, None, False, False, False, False)
                    , "user": WPacsCSV(self.delim, None, True, False, False, False)
                    , "rules": WPacsCSV(self.delim, None, False, True, False, False)
                    , "lang": WPacsCSV(self.delim, None, False, False, True, False)
                    , "struct": WPacsCSV(self.delim, None, False, False, False, True)
                    , "keypath": WPacsCSV(self.delim, "target:displayName", False, False, False, False)
                    , "all": WPacsCSV(self.delim, None, False, False, False, True)
                    }

        # set any instance attributes here, avoid hard-coding in test methods 
        self.lengths = {"base": 4, "user": 5, "rules": 5, "lang": 5, "struct": 8, "keypath":5, "all":8}

    def tearDown(self):
        """
        """
        pass

    
    #
    # helpful to group test methods that are related into sections
    #
    
    def test_sample_data(self):
        """ Check that we can use each test object's procRecord method on each record
        in the newsgator_sample.json example file without raising an exception"""
        # get a temporary obj
        tmp = self.objs["base"]
        # grab the correct data file
        datafile = "./data/wp-com_sample.json"

        # loop over all of the test wordpress processing objects
        for o in self.objs.values():
            # loop over records
            for i, record in o.file_reader(datafile):
                record_string = o.procRecord(record)

    def test_reader(self):
        """Test that our file_reader method is working as expected"""
        # base instance
        o = self.objs["base"]
        # without eg for a loop, use .next()
        g = o.file_reader(json_string = VALID_ACTIVITY)
        self.assertIsInstance(g.next(), tuple)

    def test_lengths(self):
        """Check the number of fields being output."""
        for key in self.objs.keys():
            o = self.objs[key]
            for i, record in o.file_reader(json_string = VALID_ACTIVITY):
                failure_msg = "failed while testing the length of the {} case output".format(key)
                record_string = o.procRecord(record)
                self.assertEqual(len(record_string.split(self.delim)),self.lengths[key],failure_msg)

    def test_user_fields(self):
        """ Test for non-None values in a good record when using the 'user' option,
        and None values in an intentionally damaged record"""

        GOOD_USER_STRING = VALID_ACTIVITY

        USER_STRING_W_NULL = """{"id":"tag:gnip.wordpress.com:2012:blog/4885073/post/1089","verb":"post","target":{"summary":"(by jskr)","link":"http://300slow.wordpress.com/","feed":"http://300slow.wordpress.com/feed/","wpBlogId":4885073,"displayName":"300słow","objectType":"blog"},"postedTime":"2013-05-25T15:43:06.000Z","provider":{"link":"http://im.wordpress.com:8008/posts.json","displayName":"WordPress","objectType":"service"},"object":{"id":"article:wordpress.com:4885073:1089","content":"o już czasu jestem, pod dużym wrażeniem sposobów jakimi kościół próbuje mnie rozbawić.  Co najważniejsze, czyni to skutecznie i wręcz czoła chylę przed ich pomysłowością. Mistrzami są zaś w tak zwanym wykręcaniu kota ogonem. Oto jeden z ostatnich przykładow. Jef Kloch, rzecznik tzw. episkopatu odpowiedział wreszcie na pytania dziennikarzy (milczał jak skała przez niemal dwa miesiące) dotyczące pedofilii w polskim kościele. Co odpowiedział? Że kościół nie zbiera informacji na temat nadużyć księży. Oznacza to, że nie zna (przynajmniej oficjalnie) skali tego problemu. Ale wcale nie to jest najśmieszniejsze. Bo pytany dalej dlaczego to nie zbierają tych informacji, ksiądz Kloch z miną pokerzysty odpowiada, że danych tych nie zbierają ze względu na dobro osób pokrzy wdzonych to dopiero jest naprawdę śmieszne, wręcz zwala z nóg. Byłbym bardzo ciekaw przeto, na czym zdaniem pana Klocha to dobro pokrzywdzonych polega. Bo niezmiennie od dłuższego już czasu mam graniczące z pewnością przekonanie, że mówiąc o pokrzywdzonych, pan Kloch ma na myśli wyłącznie biednych, napastowanychseksulanie księży, prawdziwe ofiary pedofilii w kościele.  I co? Ręce wprost same składają się do oklasków.","summary":"Od d&#322;u&#380;szego ju&#380; czasu jestem, pod du&#380;ym wra&#380;eniem sposob&#243;w jakimi ko&#347;ci&#243;&#322; pr&#243;buje mnie rozbawi&#263;. &#160;Co najwa&#380;niejsze, czyni to skutecznie i wr&#281;cz czo&#322;a chyl&#281; przed ich pomys&#322;owo&#347;ci&#261;. Mistrzami s&#261; za&#347; w tak zwanym wykr&#281;caniu kota ogonem. Oto jeden z&#160;ostatnich przyk&#322;adow. Ksi&#261;dz J&#243;zef Kloch, rzecznik tzw. episkopatu odpowiedzia&#322; wreszcie na pytania dziennikarzy (milcza&#322; jak ska&#322;a przez niemal [&#8230;]","link":"http://300slow.wordpress.com/2013/05/25/co-kosciol-wie-a-czego-na-wszelki-wypadek-nie-wie/","postedTime":"2013-05-25T15:42:58Z","wpBlogId":4885073,"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","objectType":"article","updatedTime":"2013-05-25T15:42:58Z","wpPostId":1089},"actor":{"id":null,"link":"http://gravatar.com/jerzysikora","wpEmailMd5":"dea3b3f6a8265868871a6e12a01a8cf9","displayName":"jsikora","objectType":"person"},"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","gnip":{"language":{"value":"pl"},"urls":[{"url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg","expanded_url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg"}]}}""" 

        USER_STRING_WO_FIELD = """{"id":"tag:gnip.wordpress.com:2012:blog/4885073/post/1089","verb":"post","target":{"summary":"(by jskr)","link":"http://300slow.wordpress.com/","feed":"http://300slow.wordpress.com/feed/","wpBlogId":4885073,"displayName":"300słow","objectType":"blog"},"postedTime":"2013-05-25T15:43:06.000Z","provider":{"link":"http://im.wordpress.com:8008/posts.json","displayName":"WordPress","objectType":"service"},"object":{"id":"article:wordpress.com:4885073:1089","content":"o już czasu jestem, pod dużym wrażeniem sposobów jakimi kościół próbuje mnie rozbawić.  Co najważniejsze, czyni to skutecznie i wręcz czoła chylę przed ich pomysłowością. Mistrzami są zaś w tak zwanym wykręcaniu kota ogonem. Oto jeden z ostatnich przykładow. Jef Kloch, rzecznik tzw. episkopatu odpowiedział wreszcie na pytania dziennikarzy (milczał jak skała przez niemal dwa miesiące) dotyczące pedofilii w polskim kościele. Co odpowiedział? Że kościół nie zbiera informacji na temat nadużyć księży. Oznacza to, że nie zna (przynajmniej oficjalnie) skali tego problemu. Ale wcale nie to jest najśmieszniejsze. Bo pytany dalej dlaczego to nie zbierają tych informacji, ksiądz Kloch z miną pokerzysty odpowiada, że danych tych nie zbierają ze względu na dobro osób pokrzy wdzonych to dopiero jest naprawdę śmieszne, wręcz zwala z nóg. Byłbym bardzo ciekaw przeto, na czym zdaniem pana Klocha to dobro pokrzywdzonych polega. Bo niezmiennie od dłuższego już czasu mam graniczące z pewnością przekonanie, że mówiąc o pokrzywdzonych, pan Kloch ma na myśli wyłącznie biednych, napastowanychseksulanie księży, prawdziwe ofiary pedofilii w kościele.  I co? Ręce wprost same składają się do oklasków.","summary":"Od d&#322;u&#380;szego ju&#380; czasu jestem, pod du&#380;ym wra&#380;eniem sposob&#243;w jakimi ko&#347;ci&#243;&#322; pr&#243;buje mnie rozbawi&#263;. &#160;Co najwa&#380;niejsze, czyni to skutecznie i wr&#281;cz czo&#322;a chyl&#281; przed ich pomys&#322;owo&#347;ci&#261;. Mistrzami s&#261; za&#347; w tak zwanym wykr&#281;caniu kota ogonem. Oto jeden z&#160;ostatnich przyk&#322;adow. Ksi&#261;dz J&#243;zef Kloch, rzecznik tzw. episkopatu odpowiedzia&#322; wreszcie na pytania dziennikarzy (milcza&#322; jak ska&#322;a przez niemal [&#8230;]","link":"http://300slow.wordpress.com/2013/05/25/co-kosciol-wie-a-czego-na-wszelki-wypadek-nie-wie/","postedTime":"2013-05-25T15:42:58Z","wpBlogId":4885073,"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","objectType":"article","updatedTime":"2013-05-25T15:42:58Z","wpPostId":1089},"actor":{"id_DAMAGED":"person:wordpress.com:45337318","link":"http://gravatar.com/jerzysikora","wpEmailMd5":"dea3b3f6a8265868871a6e12a01a8cf9","displayName":"jsikora","objectType":"person"},"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","gnip":{"language":{"value":"pl"},"urls":[{"url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg","expanded_url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg"}]}}"""

        o = self.objs['user']

        # this should have data
        failure_msg = "There should have been data in this field, but there wasn't (or the data that was there was wrong)"
        for i, record in o.file_reader(json_string = GOOD_USER_STRING):
            record_string = o.procRecord(record)
            self.assertNotEqual("None", record_string.split(self.delim)[-1], failure_msg)
            self.assertEqual("person:wordpress.com:45337318" , record_string.split(self.delim)[-1], failure_msg)

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
         
        KEYPATH_WO_PATH = """{"id":"tag:gnip.wordpress.com:2012:blog/4885073/post/1089","verb":"post","target":{"summary":"(by jskr)","link":"http://300slow.wordpress.com/","feed":"http://300slow.wordpress.com/feed/","wpBlogId":4885073,"BAD_displayName":"300słow","objectType":"blog"},"postedTime":"2013-05-25T15:43:06.000Z","provider":{"link":"http://im.wordpress.com:8008/posts.json","displayName":"WordPress","objectType":"service"},"object":{"id":"article:wordpress.com:4885073:1089","content":"o już czasu jestem, pod dużym wrażeniem sposobów jakimi kościół próbuje mnie rozbawić.  Co najważniejsze, czyni to skutecznie i wręcz czoła chylę przed ich pomysłowością. Mistrzami są zaś w tak zwanym wykręcaniu kota ogonem. Oto jeden z ostatnich przykładow. Jef Kloch, rzecznik tzw. episkopatu odpowiedział wreszcie na pytania dziennikarzy (milczał jak skała przez niemal dwa miesiące) dotyczące pedofilii w polskim kościele. Co odpowiedział? Że kościół nie zbiera informacji na temat nadużyć księży. Oznacza to, że nie zna (przynajmniej oficjalnie) skali tego problemu. Ale wcale nie to jest najśmieszniejsze. Bo pytany dalej dlaczego to nie zbierają tych informacji, ksiądz Kloch z miną pokerzysty odpowiada, że danych tych nie zbierają ze względu na dobro osób pokrzywdzonych to dopiero jest naprawdę śmieszne, wręcz zwala z nóg. Byłbym bardzo ciekaw przeto, na czym zdaniem pana Klocha to dobro pokrzywdzonych polega. Bo niezmiennie od dłuższego już czasu mam graniczące z pewnością przekonanie, że mówiąc o pokrzywdzonych, pan Kloch ma na myśli wyłącznie biednych, napastowanych seksulanie księży, prawdziwe ofiary pedofilii w kościele.  I co? Ręce wprost same składają się do oklasków.","summary":"Od d&#322;u&#380;szego ju&#380; czasu jestem, pod du&#380;ym wra&#380;eniem sposob&#243;w jakimi ko&#347;ci&#243;&#322; pr&#243;buje mnie rozbawi&#263;. &#160;Co najwa&#380;niejsze, czyni to skutecznie i wr&#281;cz czo&#322;a chyl&#281; przed ich pomys&#322;owo&#347;ci&#261;. Mistrzami s&#261; za&#347; w tak zwanym wykr&#281;caniu kota ogonem. Oto jeden z&#160;ostatnich przyk&#322;adow. Ksi&#261;dz J&#243;zef Kloch, rzecznik tzw. episkopatu odpowiedzia&#322; wreszcie na pytania dziennikarzy (milcza&#322; jak ska&#322;a przez niemal [&#8230;]","link":"http://300slow.wordpress.com/2013/05/25/co-kosciol-wie-a-czego-na-wszelki-wypadek-nie-wie/","postedTime":"2013-05-25T15:42:58Z","wpBlogId":4885073,"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","objectType":"article","updatedTime":"2013-05-25T15:42:58Z","wpPostId":1089},"actor":{"id":"person:wordpress.com:45337318","link":"http://gravatar.com/jerzysikora","wpEmailMd5":"dea3b3f6a8265868871a6e12a01a8cf9","displayName":"jsikora","objectType":"person"},"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","gnip":{"language":{"value":"pl"},"urls":[{"url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg","expanded_url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg"}]}}"""

        KEYPATH_WO_FIELD = """{"id":"tag:gnip.wordpress.com:2012:blog/4885073/post/1089","verb":"post","BAD_target":{"summary":"(by jskr)","link":"http://300slow.wordpress.com/","feed":"http://300slow.wordpress.com/feed/","wpBlogId":4885073,"displayName": "stuff","objectType":"blog"},"postedTime":"2013-05-25T15:43:06.000Z","provider":{"link":"http://im.wordpress.com:8008/posts.json","displayName":"WordPress","objectType":"service"},"object":{"id":"article:wordpress.com:4885073:1089","content":"o już czasu jestem, pod dużym wrażeniem sposobów jakimi kościół próbuje mnie rozbawić.  Co najważniejsze, czyni to skutecznie i wręcz czoła chylę przed ich pomysłowością. Mistrzami są zaś w tak zwanym wykręcaniu kota ogonem. Oto jeden z ostatnich przykładow. Jef Kloch, rzecznik tzw. episkopatu odpowiedział wreszcie na pytania dziennikarzy (milczał jak skała przez niemal dwa miesiące) dotyczące pedofilii w polskim kościele. Co odpowiedział? Że kościół nie zbiera informacji na temat nadużyć księży. Oznacza to, że nie zna (przynajmniej oficjalnie) skali tego problemu. Ale wcale nie to jest najśmieszniejsze. Bo pytany dalej dlaczego to nie zbierają tych informacji, ksiądz Kloch z miną pokerzysty odpowiada, że danych tych nie zbierają ze względu na dobro osób pokrzywdzonych to dopiero jest naprawdę śmieszne, wręcz zwala z nóg. Byłbym bardzo ciekaw przeto, na czym zdaniem pana Klocha to dobro pokrzywdzonych polega. Bo niezmiennie od dłuższego już czasu mam graniczące z pewnością przekonanie, że mówiąc o pokrzywdzonych, pan Kloch ma na myśli wyłącznie biednych, napastowanych seksulanie księży, prawdziwe ofiary pedofilii w kościele.  I co? Ręce wprost same składają się do oklasków.","summary":"Od d&#322;u&#380;szego ju&#380; czasu jestem, pod du&#380;ym wra&#380;eniem sposob&#243;w jakimi ko&#347;ci&#243;&#322; pr&#243;buje mnie rozbawi&#263;. &#160;Co najwa&#380;niejsze, czyni to skutecznie i wr&#281;cz czo&#322;a chyl&#281; przed ich pomys&#322;owo&#347;ci&#261;. Mistrzami s&#261; za&#347; w tak zwanym wykr&#281;caniu kota ogonem. Oto jeden z&#160;ostatnich przyk&#322;adow. Ksi&#261;dz J&#243;zef Kloch, rzecznik tzw. episkopatu odpowiedzia&#322; wreszcie na pytania dziennikarzy (milcza&#322; jak ska&#322;a przez niemal [&#8230;]","link":"http://300slow.wordpress.com/2013/05/25/co-kosciol-wie-a-czego-na-wszelki-wypadek-nie-wie/","postedTime":"2013-05-25T15:42:58Z","wpBlogId":4885073,"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","objectType":"article","updatedTime":"2013-05-25T15:42:58Z","wpPostId":1089},"actor":{"id":"person:wordpress.com:45337318","link":"http://gravatar.com/jerzysikora","wpEmailMd5":"dea3b3f6a8265868871a6e12a01a8cf9","displayName":"jsikora","objectType":"person"},"displayName":"Co kościół wie, a czego na wszelki wypadek nie wie","gnip":{"language":{"value":"pl"},"urls":[{"url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg","expanded_url":"http://300slow.files.wordpress.com/2013/05/avatar_new.jpeg"}]}}"""

        # this should have data
        failure_msg = "Looks like the parser never found the specified kaypath"
        for i, record in o.file_reader(json_string = VALID_ACTIVITY):
            record_string = o.procRecord(record)
            self.assertEqual(u'300słow', record_string.split(self.delim)[-1], failure_msg)

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
