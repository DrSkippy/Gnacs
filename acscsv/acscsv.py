#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__="Scott Hendrickson"
__license__="Simplified BSD"

import sys
import datetime
import fileinput
from StringIO import StringIO
# Experimental: Use numba to speed up some fo the basic function
# that are run many times per record
# from numba import jit
# use fastest option available
try:
    import ujson as json
except ImportError:
    try:
        import json
    except ImportError:
        import simplejson as json

gnipError = "GNIPERROR"
gnipRemove = "GNIPREMOVE"
gnipDateTime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
INTERNAL_EMPTY_FIELD = "GNIPEMPTYFIELD"

class _Field(object):
    """
    Base class for extracting the desired value at the end of a series of keys in a JSON Activity 
    Streams payload. Set the application-wide default value (for e.g. missing values) here, 
    but also use child classes to override when necessary. Subclasses also need to define the 
    key-path (path) to the desired location by overwriting the path attr.
    """

    # set some default values; these can be overwritten in custom classes 
    # twitter format
    default_t_fmt = "%Y-%m-%dT%H:%M:%S.000Z" 
    default_value = INTERNAL_EMPTY_FIELD
    path = []                       # dict key-path to follow for desired value

    label = 'DummyKeyPathLabel'         # this must match if-statement in constructor

    def __init__(self, json_record):
        if self.label == 'DummyKeyPathLabel':
            self.label = ':'.join(self.path)
        self.value = None                    # str representation of the field, often = str( self.value_list ) 
        if json_record is not None:
            self.value = self.walk_path(json_record)
        else:
            self.value = self.default_value

    def __repr__(self):
        return unicode(self.value)

    def walk_path(self, json_record, path=None):
        res = json_record
        if path is None:
            path = self.path
        for k in path:
            if res is None:
                break
            if k not in res or ( type(res[k]) is list and len(res[k]) == 0 ):
                # parenthetical clause for values with empty lists e.g. twitter_entities
                return self.default_value
            res = res[k]
        # handle the special case where the walk_path found null (JSON) which converts to 
        # a Python None. Only use "None" (str version) if it's assigned to self.default_value 
        res = res if res is not None else self.default_value
        return res
    
    def walk_path_slower(self, json_record, path=None):
        """Slower version fo walk path. Depricated."""
        if path is None:
            path = self.path
        try:
            execstr = "res=json_record" + '["{}"]'*len(path)
            exec(execstr.format(*path))
        except (KeyError, TypeError):
            res = None
        if res is None:
            res = self.default_value
        return res

    def fix_length(self, iterable, limit=None):
        """
        Take an iterable (typically a list) and an optional maximum length (limit). 
        If limit is not given, and the input iterable is not equal to self.default_value
        (typically "None"), the input iterable is returned. If limit is given, the return
        value is a list that is either truncated to the first limit items, or padded 
        with self.default_value until it is of size limit. Note: strings are iterables, 
        so if you pass this function a string, it will (optionally) truncate the 
        number of characters in the string according to limit. 
        """
        res = [] 

        if limit is None:
            # no limits on the length of the result, so just return the original iterable
            res = iterable
        else:
            #if len(iterable) == 0:
            if iterable == self.default_value or len(iterable) == 0:
                # if walk_path() finds the final key, but the value is an empty list 
                #   (common for e.g. the contents of twitter_entities) 
                #   overwrite self.value with a list of self.default_value and of length limit
                res = [ self.default_value ]*limit
            else:
                # found something useful in the iterable, either pad the list or truncate 
                #   to end up with something of the proper length                                                                                                                                   
                current_length = len( iterable ) 
                if current_length < limit:
                    res = iterable + [ self.default_value 
                                        for _ in range(limit - current_length) ]
                else:  
                    res = iterable[:limit]
        return res


class _LimitedField(_Field):
    """  
    Takes JSON record (in python dict form) and optionally a maximum length (limit, 
    with default length=5). Uses parent class _Field() to assign the appropriate value 
    to self.value. When self.value is a list of dictionaries, 
    inheriting from _LimitedField() class allows for the extraction and combination of 
    an arbitrary number of fields within self.value into self.value_list.

    Ex: if your class would lead to having 
    self.value = [ {'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6} ], and what you'd like 
    is a list that looks like [ 1, 2, 4, 5 ], inheriting from _LimitedField() allows you 
    to overwrite the fields list ( fields=["a", "b"] ) to obtain this result. 
    Finally, self.value is set to a string representation of the final self.value_list.
    """
    #TODO: is there a better way that this class and the fix_length() method in _Field class
    #       could be combined?
    #TODO: set limit=None by default and just return as many as there are, otherwise (by specifying 
    #    limit), return a maximum of limit.
    # TODO:
    # - consolidate _LimitedField() & fix_length() if possible 

    def __init__(self, json_record, limit=1):
        self.fields = None
        super(
            _LimitedField 
            , self).__init__(json_record)
        # self.value is possibly a list of dicts for each activity media object 
        if self.fields:
            # start with default list full of the default_values
            self.value_list = [ self.default_value ]*( len(self.fields)*limit )
            if self.value != self.default_value: 
                for i,x in enumerate(self.value):   # iterate over the dicts in the list
                    if i < limit:                   # ... up until you reach limit 
                        for j,y in enumerate(self.fields):      # iterate over the dict keys 
                            self.value_list[ len( self.fields )*i + j ] = x[ self.fields[j] ] 
            # finally, str-ify the list
            self.value = str( self.value_list )
    
class AcsCSV(object):
    """Base class for all delimited list objects. Basic delimited list utility functions"""

    def __init__(self, delim, options_keypath):
        self.delim = delim
        if delim == "":
            print >>sys.stderr, "Warning - Output has Null delimiter"
        self.rmchars = "\n\r {}".format(self.delim)
        self.options_keypath = options_keypath
        
    def string_hook(self, record_string, mode_dummy):
        """
        Returns a file-like StringIO object built from the activity record in record_string.
        This is ultimately passed down to the FileInput.readline() method. The mode_dummy 
        parameter is only included so the signature matches other hooks. 
        """
        return StringIO( record_string ) 

    def file_reader(self, options_filename=None, json_string=None):
        """
        Read arbitrary input file(s) or standard Python str. When passing file_reader() a 
        JSON string, assign it to the json_string arg. Yields a tuple of (line number, record).
        """
        line_number = 0
        if json_string is not None: 
            hook = self.string_hook 
            options_filename = json_string 
        else:
            hook = fileinput.hook_compressed
        for r in fileinput.FileInput(options_filename, openhook=hook):  
            line_number += 1
            try:
                recs = [json.loads(r.strip())]
            except ValueError:
                try:
                    # maybe a missing line feed?
                    recs = [json.loads(x) for x in r.strip().replace("}{", "}GNIP_SPLIT{")
                        .split("GNIP_SPLIT")]
                except ValueError:
                    sys.stderr.write("Invalid JSON record (%d) %s, skipping\n"
                        %(line_number, r.strip()))
                    continue
            for record in recs:
                if len(record) == 0:
                    continue
                # hack: let the old source modules still have a self.cnt for error msgs
                self.cnt = line_number
                yield line_number, record

    def cleanField(self,f):
        """Clean fields of new lines and delmiter."""
        res = INTERNAL_EMPTY_FIELD
        try:
            res = f.strip(
                ).replace("\n"," "
                ).replace("\r"," "
                ).replace(self.delim, " "
                )
        except AttributeError:
            try:
                # odd edge case that f is a number
                # then can't call string functions
                float(f)
                res = str(f)
            except TypeError:
                pass
        return res

    def buildListString(self,l):
        """Generic list builder returns a string representation of list"""
        # unicode output of list (without u's)
        res = '['
        for r in l:
            # handle the various types of lists we might see
            if isinstance(r, list):
                res += "'" + self.buildListString(r) + "',"
            #elif isinstance(r, str):
            elif isinstance(r, str) or isinstance(r, unicode):
                res += "'" + r + "',"
            else:
                res += "'" + str(r) + "',"
        if res.endswith(','):
            res = res[:-1]
        res += ']'
        return res

    def splitId(self, x, index=1):
        """Generic functions for splitting id parts"""
        tmp = x.split("/")
        if len(tmp) > index:
            return tmp[index]
        else:
            return x

    def asString(self, l, emptyField):
        """Returns a delimited list object as a properly delimited string."""
        if l is None:
            return None
        for i, x in enumerate(l):
            if x == INTERNAL_EMPTY_FIELD:
                l[i] = emptyField
        return self.delim.join(l)

    def get_source_list(self, x):
        """Wrapper for the core activity parsing function."""
        source_list = self.procRecordToList(x)
        if self.options_keypath:
            source_list.append(self.keyPath(x))
        # ensure no pipes, newlines, etc
        return [ self.cleanField(x) for x in source_list ]

    def procRecord(self, x, emptyField="None"):
        return self.asString(self.get_source_list(x), emptyField)

    def asGeoJSON(self, x):
        """Get results as GeoJSON representation."""
        record_list = self.procRecordToList(x)
        if self.__class__.__name__ == "TwacsCSV" and self.options_geo:
            if self.geoCoordsList is None:
                return
            lon_lat = self.geoCoordsList[::-1]
        elif self.__class__.__name__ == "FsqacsCSV" and self.options_geo:
            lon_lat = self.geo_coords_list
        else:
            return {"Error":"This publisher doesn't have geo"}
        return { 
                "type": "Feature"
                , "geometry": { "type": "Point", "coordinates": lon_lat }
                , "properties": { "id": record_list[0] } 
                }
    
    def keyPath(self,d):
        """Get a generic key path specified at run time. Consider using jq instead?"""
        #key_list = self.options_keypath.split(":")
        delim = ":"
        #print >> sys.stderr, "self.__class__ " + str(self.__class__)
        if self.__class__.__name__ == "NGacsCSV":
            delim = ","
        key_stack = self.options_keypath.split(delim)
        #print >> sys.stderr, "key_stack " + str(key_stack)
        x = d
        while len(key_stack) > 0:
            try:
                k = key_stack.pop(0)
                try:
                    idx = int(k)
                except ValueError:
                    # keys are ascii strings
                    idx = str(k)
                x = x[idx]
            except (IndexError, TypeError, KeyError) as e:
                #sys.stderr.write("Keypath error at %s\n"%k)
                return "PATH_EMPTY"
        return unicode(x)

