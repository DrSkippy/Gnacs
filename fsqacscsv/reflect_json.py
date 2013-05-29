#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"
import sys
import json as json_formatter
try:
    import ujson as json
except ImportError:
    try:
        import json
    except ImportError:
        import simplejson as json

LIST_ITEMS = "list-items"

def reflect_json(json_string):
    try:
        d = json.loads(json_string.strip())
    except ValueError:
        sys.stderr.write("Invalid JSON record %s, skipping\n"%(json_string.strip()))
        return None 
    #
    return walk_label(d)

def walk_label(x, label=None):
    if type(x) == type({}):
        for field in x:
            if label is None:
                new_field = field
            else:
                new_field = "%s:%s"%(label, field)
            x[field] = walk_label(x[field], label=new_field)
    elif type(x) == type([]):
        if len(x) > 0:
            a = x[0]
            x = [ walk_label(a, label="%s_%s"%(label, LIST_ITEMS))  ]
        else:
            x = [ "%s_%s"%(label, LIST_ITEMS) ]
    else:
        return label
    if label is None:
        return json.dumps(x)
    else:
        return x
