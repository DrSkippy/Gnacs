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
# ujson is 20% faster
import json as json_formatter
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
			, help="Show user's influence metrics")
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
    parser.add_argument("-D","--database", action="store_true", dest="db"
            , default=False
			, help="directs stdout to file objects for uploading to mysql db tables")
    return parser

if "__main__" == __name__:
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
        # NOTE: When using geojson, we have an in-memory structure
        # example record is geo_d = {"type": "FeatureCollection", "features": []}
        # so we do this in two parts. See below for completion of structure.
        sys.stdout.write('{"type": "FeatureCollection", "features": [')
    #
    if options.pub.lower().startswith("word") or options.pub.lower().startswith("wp"):
        processing_obj = wpacscsv.WPacsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.lang
			, options.struct)
    elif options.pub.lower().startswith("disq"):
        processing_obj = diacscsv.DiacsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.lang
			, options.struct
			, options.status)
    elif options.pub.lower().startswith("tumb"): 
        processing_obj = tblracscsv.TblracsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.lang
			, options.struct)
    elif options.pub.lower().startswith("four") or options.pub.lower().startswith("fsq"):
        processing_obj = fsqacscsv.FsqacsCSV(delim
			, options.keypath
			, options.geo
			, options.user
			, options.rules
			, options.lang
			, options.struct)
    elif options.pub.lower().startswith("get") or options.pub.lower().startswith("gg"):
        processing_obj = ggacscsv.GgacsCSV(delim
			, options.keypath
			, options.user
			, options.rules
			, options.urls
			, options.origin)
    elif options.pub.lower().startswith("st") and options.pub.lower().endswith("native"):
        processing_obj = stntvcsv.StntvCSV(delim
			, options.keypath
			, options.user
			, options.struct
			, options.influence)
    elif options.pub.lower().startswith("st"):
        processing_obj = stacscsv.StacsCSV(delim
			, options.user
			, options.struct
			, options.influence)
    elif options.pub.lower().startswith("news") or options.pub.lower().startswith("ng"):
        processing_obj = ngacscsv.NGacsCSV(delim
			, options.keypath
			, options.urls
			, options.user)
    else:
        processing_obj = twacscsv.TwacsCSV(delim
			, options.keypath
			, options.geo
			, options.user
			, options.rules
			, options.urls
			, options.lang
			, options.influence
			, options.struct)
    if options.db:
        # different twacs module!
        processing_obj = twacsDB.Twacs(delim
			, options.keypath
			, options.geo
			, options.user
			, options.rules
			, options.urls
			, options.lang
			, options.influence
			, options.struct
			, options.db)
        #
        # create a new data directory (change as needed)
        data_dir = os.environ['HOME'] + "/gnacs_db"
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        # open file objects for writing below 
        acs_f = codecs.open( data_dir + '/table_activities.csv', 'wb', 'utf8') 
        ustatic_f = codecs.open( data_dir + '/table_users_static.csv', 'wb', 'utf8') 
        udyn_f = codecs.open( data_dir + '/table_users_dynamic.csv', 'wb', 'utf8') 
        hash_f = codecs.open( data_dir + '/table_hashtags.csv', 'wb', 'utf8') 
    #
    cnt = 0
    first_geo = True 
    #
    for r in fileinput.FileInput(options.file_name,openhook=fileinput.hook_compressed):
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
                print json_formatter.dumps(record, indent=3, ensure_ascii=False)
            continue 
        for record in recs:
            if len(record) == 0:
                # ignore blank lines
                continue
            try:
                if options.explain:
                    record = reflect_json.reflect_json(record)
                    sys.stdout.write("%s\n"%processing_obj.procRecord(cnt, record))
                elif options.geojson:
                    # geo-tag coords
                    geo_rec = processing_obj.asGeoJSON(cnt, record)
                    if geo_rec is not None:
                        if not first_geo: 
                            sys.stdout.write(",")
                        sys.stdout.write(json.dumps(geo_rec))
                        first_geo = False
                elif options.db:
                    compRE = re.compile(r"GNIPREMOVE") 
                    tmp_combined_rec = processing_obj.procRecord(cnt, record, emptyField="\\N")
                    if compRE.search(tmp_combined_rec): 
                        sys.stderr.write("Skipping compliance activity: ({}) {}\n"
                                .format(cnt, tmp_combined_rec) ) 
                        continue
                    # otherwise, write to appropriate file objects (from above)
                    flag = "GNIPSPLIT"      # also hardcoded in twacsDB.py
                    acs_str, ustatic_str, udyn_str, hash_str = tmp_combined_rec.split(flag) 
                    # clean up any leading/trailing pipes 
                    acs_str = acs_str.strip("|")
                    ustatic_str = ustatic_str.strip("|")
                    udyn_str = udyn_str.strip("|")
                    hash_str = hash_str.strip("|")                    # id|tag1|id|tag2|...
                    hash_list = re.findall("[^|]+\|[^|]+", hash_str)  # [ 'id|tag1', 'id|tag2', ... ] 
                    #
                    acs_f.write(acs_str + "\n")
                    ustatic_f.write(ustatic_str + "\n")
                    udyn_f.write(udyn_str + "\n")
                    [ hash_f.write(x + "\n") for x in hash_list ] 
                else:
                    sys.stdout.write("%s\n"%processing_obj.procRecord(cnt, record, emptyField="None"))
            # catch I/O exceptions associated with writing to stdout (e.g. when output is piped to 'head')
            except IOError:
                try:
                    sys.stdout.close()
                except IOError:
                    pass
                try:
                    sys.stderr.close()
                except IOError:
                    pass
                break
            except UnicodeEncodeError, e:
                sys.stderr.write("UnicodeEncodeError: error={} ({})\n".format(e, cnt))
                # use this if you want to see the full troublesome records  
                #sys.stderr.write("Bad unicode encoding: error={} ({}), record={}\n".format(e, cnt, record))

    if options.geojson:
        # sys.stdout.write(json.dumps(geo_d) + "\n")
        sys.stdout.write(']}\n')            
