#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import codecs
import diacscsv.diacscsv

# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

tcsv = diacscsv.diacscsv.DiacsCSV(None, False, False, False, False, False, True) 
for x in sys.stdin:
    record = x.strip()
    if record == "":
        continue
    sys.stdout.write("%s\n"%tcsv.procRecord(record))
