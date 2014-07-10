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

    def test_sample_set(self):
        ids = [
             ( 351835320003727360 , 73 )
            ,( 351835320121176064 , 1 )
            ,( 351835320125366272 , 2 )
            ,( 351835320184086528 , 16 )
            ,( 351835320217636864 , 24 )
            ,( 351835320226029568 , 26 )
            ,( 351835320284749824 , 40 )
            ,( 351835320284753920 , 40 )
            ,( 351835320297328640 , 43 )
            ,( 351835320301527040 , 44 )
            ,( 351835320339283968 , 53 )
            ,( 351835320368635905 , 60 )
            ,( 351835320385413124 , 64 )
            ,( 351835320418967552 , 72 )
            ,( 351835320435748864 , 76 )
            ,( 351835320590934016 , 13 )
            ,( 351835320607719424 , 17 )
            ,( 351835320645459968 , 26 )
            ,( 351835320695787522 , 38 )
            ,( 351835320737730561 , 48 )
            ,( 351835320788062208 , 60 )
            ,( 351835320792252417 , 61 )
            ,( 351835320817426433 , 67 )
            ,( 351835320859369475 , 77 )
            ,( 351835321006170112 , 12 )
            ,( 351835321056509952 , 24 )
            ,( 351835321081659392 , 30 )
            ,( 351835321220075524 , 63 )
            ,( 351835321425608704 , 12 )
            ,( 351835321442385921 , 16 )
            ,( 351835321471746048 , 23 )
            ,( 479311173150859264 , 50 )
            ,( 479311174387785728 , 45 )
            ,( 479311174836555777 , 52 )
            ,( 479311175247593473 , 50 )
            ,( 479311176489517058 , 46 )
            ,( 479311176925736961 , 50 )
            ,( 479311178183606272 , 50 )
            ,( 479311179006087168 , 46 )
            ,( 479311179009904640 , 47 )
            ,( 479311181094469632 , 44 )
                            ]
        for i,j in ids:
            self.assertEquals(Snowflake(i).sample_set, j)

    def test_repr(self):
        self.assertEquals("""###############\nid:      113733024721539072\nseq:     0\nworker:  1\nDS:      1\nSeconds: 1315951040.81\ntime:    2011-09-13T21:57:20\n""",str(self.obj))

if __name__ == "__main__":
    unittest.main()
