#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson, Josh Montague"
__license__="Simplified BSD"

import pkg_resources
try:
    __version__ = pkg_resources.require("gnacs")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "N/A"
import sys
import codecs
import fileinput
import re
import os
import argparse
from acscsv import *
# needed only for the pretty-printing
import json as json_printer
# use fastest option available for parsing
try:
    import ujson as json
except ImportError:
    try:
        import json
    except ImportError:
        import simplejson as json

# unicode input
reload(sys)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def gnacs_args():
    """Parse comand line arguemnts for defining input and output of command line utility."""
    parser = argparse.ArgumentParser(
            description="Parse seqeunce of JSON formated activities.")
    parser.add_argument("file_name", metavar= "file_name", nargs="?"
            , default=[] 
            , help="Input file name (optional).")
    parser.add_argument("-a","--status", action="store_true", dest="status"
            , default=False
            , help="Version, status, etc.")
    parser.add_argument("-g","--geo", action="store_true", dest="geo"
            , default=False
			, help="Include geo fields")
    parser.add_argument("-i", "--influence", action="store_true", dest="influence"
            , default=False
			, help="Show user's influence metrics (Twitter only)")
    parser.add_argument("-c","--csv", action="store_true", dest="csv"
            , default=False
			, help="Comma-delimited output (, default is | without quotes)")
    parser.add_argument("-l","--lang", action="store_true", dest="lang"
            , default=False
			, help="Include language fields")
    parser.add_argument("-j","--geojson", action="store_true", dest="geojson"
            , default=False
			, help="Output is geojson format (Foursquare and Twitter only) \
                    Caution: dataset must fit in memory.")
    parser.add_argument("-o","--origin", action="store_true", dest="origin"
            , default=False
			, help="Include source/origin fields")
    parser.add_argument("-p","--pretty", action="store_true", dest="pretty"
            , default=False
			, help="Pretty JSON output of full records")
    parser.add_argument("-s", "--urls", action="store_true", dest="urls"
            , default=False
			, help="Include urls fields")
    parser.add_argument("-t","--structure", action="store_true", dest="struct"
            , default=False
			, help="Include thread linking fields")
    parser.add_argument("-r","--rules", action="store_true", dest="rules"
            , default=False
			, help="Include rules fields")
    parser.add_argument("-u","--user", action="store_true", dest="user"
            , default=False
			, help="Include user fields")
    parser.add_argument("-v","--version", action="store_true", dest="ver"
            , default=False
			, help="Show version number")
    parser.add_argument("-x","--explain", action="store_true", dest="explain", 
            default=False
			, help="Show field names in output for sample input records")
    parser.add_argument("-z","--publisher", dest="pub"
            , default="twitter"
			, help="Publisher (default is twitter), twitter, newsgator, disqus, \
                    wordpress, wpcomments, tumblr, foursquare, getglue, stocktwits, stocktwits-native")
    parser.add_argument("-k","--keypath", dest="keypath"
            , default=None
			, help="returns a value from a path of the form 'key:value'")
    return parser

if __name__ == "__main__":
    """Use gnacs delimited-field parsing libraries as a command line tool to parse a series of JSON
    formatted actvities from file, compressed file or standard input (stdin)."""
    
    options = gnacs_args().parse_args()
    if options.ver:
        print "*"*70
        print "Gnacs Version: %s"%__version__
        print "Please see https://github.com/DrSkippy27/Gnacs for updates or"
        print "sudo pip install gnacs --upgrade to install the latest version."
        print "*"*70
        sys.exit()
    #
    delim = "|"     # default delimiter
    if options.csv:
        delim = "," # csv delimiter
    elif options.geojson:
        options.geo = True 
        # note: geojson option creates an in-memory structure
        sys.stdout.write('{"type": "FeatureCollection", "features": [')
    #
    if options.pub.lower().startswith("word") or options.pub.lower().startswith("wp"):
        processing_obj = wordpress_acs.WPacsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.lang
			, options.struct
            )
    elif options.pub.lower().startswith("disq"):
        processing_obj = disqus_acs.DiacsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.lang
			, options.struct
			, options.status
            )
    elif options.pub.lower().startswith("tumb"): 
        processing_obj = tumblr_acs.TblracsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.lang
			, options.struct
            )
    elif options.pub.lower().startswith("four") or options.pub.lower().startswith("fsq"):
        processing_obj = foursquare_acs.FsqacsCSV(delim
			, options.keypath
			, options.geo
			, options.user
			, options.rules
            )
    elif options.pub.lower().startswith("get") or options.pub.lower().startswith("gg"):
        processing_obj = getglue_acs.GgacsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.urls
			, options.origin
            )
    elif options.pub.lower().startswith("st") and options.pub.lower().endswith("native"):
        processing_obj = stocktwits_native.StocktwitsNative(delim
			, options.keypath
			, options.user
			, options.struct
			, options.influence
            )
    elif options.pub.lower().startswith("st"):
        processing_obj = stocktwits_acs.StacsCSV(delim
			, options.keypath
			, options.user
			, options.struct
			, options.influence
            )
    elif options.pub.lower().startswith("news") or options.pub.lower().startswith("ng"):
        processing_obj = newsgator_acs.NGacsCSV(delim
			, options.keypath
			, options.urls
			, options.user
            )
    else:
        processing_obj = twitter_acs.TwacsCSV(delim
			, options.keypath
			, options.geo
			, options.user
			, options.rules
			, options.urls
			, options.lang
			, options.influence
			, options.struct
            )
    #
    first_geo = True 
    for line_number, record in processing_obj.file_reader(options.file_name): 
        if options.pretty:
            print json_printer.dumps(record, indent=3, ensure_ascii=False)
            continue 
        try:
            if options.explain:
                #### TODO: fix -x option for new extractors ####
                print >>sys.stderr, "\n****\n\n'explain' functionality currently unavailable\n\n****\n"
                sys.exit()
                ################################################
                record = reflect_json.reflect_json(record)
                sys.stdout.write("%s\n"%processing_obj.procRecord(record))
            elif options.geojson:
                # geo-tag coords
                geo_rec = processing_obj.asGeoJSON(record)
                if geo_rec is not None:
                    if not first_geo: 
                        sys.stdout.write(",")
                    sys.stdout.write(json.dumps(geo_rec))
                    first_geo = False
            else:
                # ensure formatter is working on a unicode object 
                sys.stdout.write(u"{}\n".format(processing_obj.procRecord(record, emptyField="None")))
        # handle I/O exceptions associated with writing to stdout (e.g. when output is piped to 'head')
        # TODO: handle this via contextmanager (within AcsCSV)? 
        except IOError, e:
            try:
                sys.stdout.close()
            except IOError:
                pass
            try:
                sys.stderr.close()
            except IOError:
                pass
            break
    # close the geojson data structure
    if options.geojson:
        sys.stdout.write(']}\n')            

