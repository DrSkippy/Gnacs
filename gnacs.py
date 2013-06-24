#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import pkg_resources
try:
    __version__ = pkg_resources.require("gnacs")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "N/A"
import sys
import codecs
import fileinput
from optparse import OptionParser
from acscsv import *
# ujson is 20% faster
import json as json_formatter
try:
    import ujson as json
except ImportError:
    try:
        import json
    except ImportError:
        import simplejson as json

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
    parser.add_option("-o","--origin", action="store_true", dest="origin", 
            default=False, help="Include source/origin fields")
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
            default="twitter", help="Publisher (default is twitter), twitter, disqus, wordpress, wpcomments, tumblr, foursquare, getglue, stocktwits")
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
    if options.pub.startswith("word") or options.pub.startswith("wp-com") or options.pub.startswith("wp-org"):
        proc = wpacscsv.WPacsCSV(delim, options.user, options.rules, options.lang, options.struct)
    elif options.pub.startswith("disq") or options.pub.startswith("disqus"):
        proc = diacscsv.DiacsCSV(delim, options.user, options.rules, options.lang, options.struct, options.status)
    elif options.pub.startswith("tumb") or options.pub.startswith("tumblr"):
        proc = tblracscsv.TblracsCSV(delim, options.user, options.rules, options.lang, options.struct)
    elif options.pub.startswith("four") or options.pub.startswith("foursquare"):
        proc = fsqacscsv.FsqacsCSV(delim, options.geo, options.user, options.rules, options.lang, options.struct)
    elif options.pub.startswith("get") or options.pub.startswith("gg") or options.pub.startswith("getglue"):
        proc = ggacscsv.GgacsCSV(delim, options.user, options.rules, options.urls, options.origin)
    elif options.pub.startswith("stock") or options.pub.startswith("stocktwits") or options.pub.startswith("st"):
        proc = stntvcsv.StntvCSV(delim, options.user, options.struct, options.influence)
    else:
        proc = twacscsv.TwacsCSV(delim, options.geo, options.user, options.rules, options.urls, options.lang, options.influence)
    #
    cnt = 0
    #
    for r in fileinput.FileInput(args,openhook=fileinput.hook_compressed):
        cnt += 1
        try:
            recs = [json.loads(r.strip())]
        except ValueError:
            try:
                # maybe a missing line feed?
                recs = [json.loads(x) for x in r.strip().replace("}{", "}GNIP_SPLIT{").split("GNIP_SPLIT")]
            except ValueError:
                sys.stderr.write("Invalid JSON record (%d) %s, skipping\n"%(cnt, r.strip()))
                continue
        if options.pretty:
            for record in recs:
                print json_formatter.dumps(record, indent=3)
            continue 
        for record in recs:
            if len(record) == 0:
                continue
            if options.explain:
                record = reflect_json.reflect_json(record)
            sys.stdout.write("%s\n"%proc.procRecord(cnt, record))

if __name__ == "__main__":
    main()
