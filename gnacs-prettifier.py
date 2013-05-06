#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import codecs
import fileinput
import diacscsv.diacscsv

# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

tcsv = diacscsv.diacscsv.DiacsCSV(None,  False, False, False, False, False, True) 
for record in fileinput.FileInput(openhook=fileinput.hook_compressed):
    if record == "":
        continue
    sys.stdout.write("%s\n"%tcsv.procRecord(record))
