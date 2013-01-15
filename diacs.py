#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import codecs
from optparse import OptionParser
import diacscsv.diacscsv

# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

parser = OptionParser()
parser.add_option("-u", "--user", action="store_true", dest="user", default=False, help="Include user fields")
parser.add_option("-s", "--structure", action="store_true", dest="struct", default=False, help="Include thread linking fields")
parser.add_option("-r", "--rules", action="store_true", dest="rules", default=False, help="Include rules fields")
parser.add_option("-l", "--lang", action="store_true", dest="lang", default=False, help="Include language fields")
parser.add_option("-p", "--pretty", action="store_true", dest="pretty", default=False, help="Pretty JSON output of full records")
parser.add_option("-c", "--csv", action="store_true", dest="csv", default=False, help="Comma-delimited output (default is | without quotes)")
(options, args) = parser.parse_args()

if options.csv:
    delim = ","
else:
    delim = "|"
dcsv = diacscsv.diacscsv.DiacsCSV(delim, options.user, options.rules, options.lang, options.struct, options.pretty)
for x in sys.stdin:
    record = x.strip()
    if record == "":
        continue
    sys.stdout.write("%s\n"%dcsv.procRecord(record))
