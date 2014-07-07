#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Josh Montague"
__license__="MIT License"

import sys
import unittest
from StringIO import StringIO
from reflect_json import *


# valid activity from source (eg from data/) 
VALID_ACTIVITY ={}


class Testreflect(unittest.TestCase):
    """Unit tests of common CSV utility functions"""

    def setUp(self):
        """
        """ 

        self.delim = '|'

        # use a dict to make it easier to refer to the particular object cases
        self.objs = { 
                    "base": "foo" 
                    , "user": "baz" 
                    }

        # set any instance attributes here, avoid hard-coding in test methods 
        self.bar = None        

    def tearDown(self):
        """
        """
        pass

    
    #
    # helpful to group test methods that are related into sections
    #
    
    def test_method1(self):
        self.assertFalse(False)

        
    def test_method2(self):
        self.assertTrue(True)


 
if __name__ == "__main__":
    unittest.main()
