#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import codecs
import fileinput
from optparse import OptionParser
import diacscsv.diacscsv
import wpacscsv.wpacscsv
import twacscsv.twacscsv
import reflect.reflect_json

# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

parser = OptionParser()
parser.add_option("-g","--geo", action="store_true", dest="geo", 
        default=False, help="Include geo fields")
parser.add_option("-i", "--influence", action="store_true", dest="influence", 
        default=False, help="Show user's influence metrics")
parser.add_option("-c","--csv", action="store_true", dest="csv", 
        default=False, help="Comma-delimited output (default is | without quotes)")
parser.add_option("-l","--lang", action="store_true", dest="lang", 
        default=False, help="Include language fields")
parser.add_option("-p","--pretty", action="store_true", dest="pretty", 
        default=False, help="Pretty JSON output of full records")
parser.add_option("-s", "--urls", action="store_true", dest="urls", 
        default=False, help="Include urls fields")
parser.add_option("-t","--structure", action="store_true", dest="struct", 
        default=False, help="Include thread linking fields")
parser.add_option("-r","--rules", action="store_true", dest="rules", 
        default=False, help="Include rules fields")
parser.add_option("-u","--user", action="store_true", dest="user", 
        default=False, help="Include user fields")
parser.add_option("-x","--explain", action="store_true", dest="explain", 
        default=False, help="Show field names in output for for sample input records")
parser.add_option("-z","--publisher", dest="pub", 
        default="twitter", help="Publisher(default is twitter)\n twitter\n disqus\n wordpress\n wpcomments")
(options, args) = parser.parse_args()

if options.csv:
    delim = ","
else:
    delim = "|"

#
#
if options.pub.startswith("word"):
    proc = wpacscsv.wpacscsv.WPacsCSV(delim, options.user, options.rules, options.lang, options.struct, options.pretty)
elif options.pub.startswith("disq"):
    proc = diacscsv.diacscsv.DiacsCSV(delim, options.user, options.rules, options.lang, options.struct, options.pretty)
else:
    proc = twacscsv.twacscsv.TwacsCSV(delim, options.geo, options.user, options.rules, options.urls, options.lang, options.influence, options.pretty)

#
#
for record in fileinput.FileInput(args,openhook=fileinput.hook_compressed):
    if record == "":
        continue
    if options.explain:
        record = reflect.reflect_json.reflect_json(record)
    sys.stdout.write("%s\n"%proc.procRecord(record))
