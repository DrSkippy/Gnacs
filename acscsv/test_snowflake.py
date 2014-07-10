#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"

import unittest
import random
import string
from snowflake import *  

class TestSnowflake(unittest.TestCase):
    """Unit tests ofr common CSV utility functions"""
    def setUp(self):
        self.obj = Snowflake("113733024721539072")
        self.bin_obj = bin(self.obj.id)
        # 0b1 1001 0100 0000 1111 1001 0101 0101 1001 1100 0010 0001 0000 0000 0000

    def tearDown(self):
        pass

    def test_masked_id(self):
        self.assertEquals(self.obj.masked_id(8,0), 0)
        self.assertEquals(self.obj.masked_id(8,8), 16)
        self.assertEquals(self.obj.masked_id(8,16), 194 )
        self.assertEquals(self.obj.masked_id(8,24), 89)
        self.assertEquals(self.obj.masked_id(8,32), 149)
        self.assertEquals(self.obj.masked_id(8,40), 15)
        self.assertEquals(self.obj.masked_id(4,40), 15)
        
    def test_get_id_datetime(self):
        self.assertEquals(self.obj.get_id_datetime(), [113733024721539072, "2011-09-13T21:57:20"])

    def test_input_types(self):
        valid_inputs = [
                113733024721539072
                , 113733024721539072234534
                , "113733024721539072"
                , "113733024721539072234534"
                , "asdfasdfsa::113733024721539072"
                , "asdfasdfsa::11373302472153907223423"
                , "asdfasdfsa::113733024721539072qwerqwer"
                , "asdfasdfsa::11373302472152qwerqwer113733024721539072"
                ]
        ans = [
                self.obj.id
                , self.obj.sequence
                , self.obj.worker
                , self.obj.data_center
                , self.obj.hour
                , self.obj.min
                , self.obj.sec
                ]
        for i in valid_inputs:
            j = Snowflake(i)
            self.assertEquals([
                j.id
                , j.sequence
                , j.worker
                , j.data_center
                , j.hour
                , j.min
                , j.sec
                ], ans)

        invalid_inputs = [
                12341324132
                , "^&(*&^(*&^"
                , ""
                , None
                , ''.join(random.sample(string.digits, 2))
                , ''.join(random.sample(4*string.digits, 12))
                ]
        for i in invalid_inputs:
            j = Snowflake(i)
            
            self.assertEquals([
                j.id
                , j.sequence
                , j.worker
                , j.data_center
                , j.hour
                , j.min
                , j.sec
                ],[
                i
                , None
                , None
                , None
                , None
                , None
                , None
                ])

    def test_repr(self):
        self.assertEquals("""###############\nid:      113733024721539072\nseq:     0\nworker:  1\nDS:      1\nSeconds: 1315951040.81\ntime:    2011-09-13T21:57:20\n""",str(self.obj))

if __name__ == "__main__":
    unittest.main()
