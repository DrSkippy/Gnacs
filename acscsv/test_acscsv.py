#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"

import unittest
from acscsv import *  

class TestAcsCSV(unittest.TestCase):
    """Unit tests ofr common CSV utility functions"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCleanField(self):
        a = AcsCSV("|", False)
        self.assertEquals(a.cleanField("laksjflasjdfl;a"), "laksjflasjdfl;a")
        self.assertEquals(a.cleanField("\r\n \n\r \r\r \n\n"), "")
        self.assertEquals(a.cleanField("\r\na \n\r \r\r a\n\n"), "a       a")
        self.assertEquals(a.cleanField("asdf|asdf,,adsf|asdf"), "asdf asdf,,adsf asdf")
        b = AcsCSV(",", False)
        self.assertEquals(b.cleanField("asdf|asdf,,adsf|asdf"), "asdf|asdf  adsf|asdf")
        self.assertEquals(b.cleanField(245), "245")
        self.assertEquals(b.cleanField(a), INTERNAL_EMPTY_FIELD)


if __name__ == "__main__":
    unittest.main()
