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
    parser.add_option("-j","--geojson", action="store_true", dest="geojson", 
            default=False, help="Output is geojson format (Foursquare and Twitter only) Caution: dataset must fit in memory.")
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
            default="twitter", help="Publisher (default is twitter), twitter, newsgator, disqus, wordpress, wpcomments, tumblr, foursquare, getglue, stocktwits, stocktwits-native")
    parser.add_option("-k","--keypath", dest="keypath", 
            default=None, help="returns a value from a path of the form 'key:value'")
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
    delim = "|"
    if options.csv:
        delim = ","
    elif options.geojson:
        options.geo = True 
        # NOTE: this is an in-memory structure
        #geo_d = {"type": "FeatureCollection", "features": []}
        sys.stdout.write('{"type": "FeatureCollection", "features": [')
    #ß
    if options.pub.lower().startswith("word") or options.pub.lower().startswith("wp"):
        processing_obj = wpacscsv.WPacsCSV(delim, options.keypath, options.user, options.rules, options.lang, options.struct)
    elif options.pub.lower().startswith("disq"):
        processing_obj = diacscsv.DiacsCSV(delim, options.keypath, options.user, options.rules, options.lang, options.struct, options.status)
    elif options.pub.lower().startswith("tumb"): 
        processing_obj = tblracscsv.TblracsCSV(delim, options.keypath, options.user, options.rules, options.lang, options.struct)
    elif options.pub.lower().startswith("four") or options.pub.lower().startswith("fsq"):
        processing_obj = fsqacscsv.FsqacsCSV(delim, options.keypath, options.geo, options.user, options.rules, options.lang, options.struct)
    elif options.pub.lower().startswith("get") or options.pub.lower().startswith("gg"):
        processing_obj = ggacscsv.GgacsCSV(delim, options.keypath, options.user, options.rules, options.urls, options.origin)
    elif options.pub.lower().startswith("st") and options.pub.lower().endswith("native"):
        processing_obj = stntvcsv.StntvCSV(delim, options.keypath, options.user, options.struct, options.influence)
    elif options.pub.lower().startswith("st"):
        processing_obj = stacscsv.StacsCSV(delim, options.user, options.struct, options.influence)
    elif options.pub.lower().startswith("news") or options.pub.lower().startswith("ng"):
        processing_obj = ngacscsv.NGacsCSV(delim, options.keypath, options.urls, options.user)
    else:
        processing_obj = twacscsv.TwacsCSV(delim, options.keypath, options.geo, options.user, options.rules, options.urls, options.lang, options.influence, options.struct)
    #
    cnt = 0
    first_geo = True 
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
                print json_formatter.dumps(record, indent=3, ensure_ascii=False)
            continue 
        for record in recs:
            if len(record) == 0:
                continue
            try:
                if options.explain:
                    record = reflect_json.reflect_json(record)
                    sys.stdout.write("%s\n"%processing_obj.procRecord(cnt, record))
                #
                elif options.geojson:
                    # geo-tag coords
                    geo_rec = processing_obj.asGeoJSON(cnt, record)
                    if geo_rec is not None:
                        if not first_geo: 
                            sys.stdout.write(",")
                        sys.stdout.write(json.dumps(geo_rec))
                        first_geo = False
                else:
                    sys.stdout.write("%s\n"%processing_obj.procRecord(cnt, record))
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
                sys.stderr.write("Bad unicode uncoding: record (%d): %s\n"%(cnt, e))

    if options.geojson:
        # sys.stdout.write(json.dumps(geo_d) + "\n")
        sys.stdout.write(']}\n')            
            
            
if __name__ == "__main__":
    main()
