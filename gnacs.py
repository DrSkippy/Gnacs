#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import pkg_resources
__version__ = pkg_resources.require("gnacs")[0].version
import sys
import codecs
import fileinput
from optparse import OptionParser
import diacscsv.diacscsv
import wpacscsv.wpacscsv
import twacscsv.twacscsv
import tblracscsv.tblracscsv
import fsqacscsv.fsqacscsv 
import reflect.reflect_json

# unicode
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def main():
    parser = OptionParser()
    parser.add_option("-a","--status", action="store_true", dest="status", 
            default=False, help="Version, status, etc.")
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
    parser.add_option("-v","--version", action="store_true", dest="ver", 
            default=False, help="Show version number")
    parser.add_option("-x","--explain", action="store_true", dest="explain", 
            default=False, help="Show field names in output for sample input records")
    parser.add_option("-z","--publisher", dest="pub", 
            default="twitter", help="Publisher (default is twitter), twitter, disqus, wordpress, wpcomments, tumblr, foursquare")
    (options, args) = parser.parse_args()
    #
    if options.ver:
        print "*"*70
        print "Gnacs Version: %s"%__version__
        print "Please see https://github.com/DrSkippy27/Gnacs for updates or"
        print "sudo pip install gnacs --upgrade to install the latest version."
        print "*"*70
        sys.exit()
    #
    if options.csv:
        delim = ","
    else:
        delim = "|"
    #
    if options.pub.startswith("word"):
        proc = wpacscsv.wpacscsv.WPacsCSV(delim, options.user, options.rules, options.lang, options.struct, options.pretty)
    elif options.pub.startswith("disq"):
        proc = diacscsv.diacscsv.DiacsCSV(delim, options.user, options.rules, options.lang, options.struct, options.status, options.pretty)
    elif options.pub.startswith("tumb"):
        proc = tblracscsv.tblracscsv.TblracsCSV(delim, options.user, options.rules, options.lang, options.struct, options.pretty)
    elif options.pub.startswith("four"):
        proc = fsqacscsv.fsqacscsv.FsqacsCSV(delim, options.geo, options.user, options.rules, options.lang, options.struct, options.pretty)
    else:
        proc = twacscsv.twacscsv.TwacsCSV(delim, options.geo, options.user, options.rules, options.urls, options.lang, options.influence, options.pretty)
    #
    #
    for r in fileinput.FileInput(args,openhook=fileinput.hook_compressed):
        # remove whitepace and trailing newlines
        # deal with missing new lines
        recs = r.strip().replace("}{", "}GNIP_SPLIT{").split("GNIP_SPLIT")
        if recs == []:
            continue
        for record in recs:
            if options.explain:
                record = reflect.reflect_json.reflect_json(record)
            sys.stdout.write("%s\n"%proc.procRecord(record))

if __name__ == "__main__":
    main()
