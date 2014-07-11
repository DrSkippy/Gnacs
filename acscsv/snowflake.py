#!/usr/bin/env python
import sys
import re
import time
import datetime
import calendar

"""
From twitter code on github
 workerIdBits = 5L
 datacenterIdBits = 5L
 sequenceBits = 12L
 
 maxWorkerId = -1L ^ (-1L << workerIdBits)
 maxDatacenterId = -1L ^ (-1L << datacenterIdBits)

 sequenceMask = -1L ^ (-1L << sequenceBits)
 
 workerIdShift = sequenceBits
 datacenterIdShift = sequenceBits + workerIdBits
 timestampLeftShift = sequenceBits + workerIdBits + datacenterIdBits

 ((timestamp - twepoch) << timestampLeftShift) |
          (datacenterId << datacenterIdShift) |
              (workerId << workerIdShift) | 
               sequence
"""

FMT = "%Y-%m-%dT%H:%M:%S"
TWEPOCH = 1288834974657.

SF_SEQ_BITS = 12
SF_WORK_BITS = 5
SF_DC_BITS = 5
SF_TIME_BITS = 41
SF_BITS = 64

nRE = re.compile("[0-9]{18}")

class Snowflake(object):
    """Snowflake id object provides access to multiple forms of of the bit fields
    present in a snowflake id. Ids can be of the form of a string with leading and
    trailing characters or symbols. The first 18 consecutive digits will be used
    as the id. It is also permitted to provide an int::

        tag:search.twitter.com,2005:113733024721539072
        113733024721539072
        113733024721539072|This is the tweet for which you are looking|en

    where the latter represents a pre-snowflake twitter id. In this case all 
    fields will be null.
    
    When the input does not match a valid snowflake id, the input field is available
    as the id and all other fields are set to None.

    Available fields::

        id 
        sequence 
        worker 
        data_center 
        ts 
        sample_set 
        timestamp 
        timeStruct 
        timeString 
        year 
        month 
        day 
        hour 
        min 
        sec 
        dow 
        doy 

    """

    def __init__(self, id):
        """Create a new snowflake object from string or number represenataion
        of id."""
        ns = nRE.findall(str(id))
        if len(ns) > 0:
            # only process first matching id in string
            self.id = int(ns[0])
            self.sequence = int(self.masked_id(SF_SEQ_BITS, 0))
            self.worker = int(self.masked_id(SF_WORK_BITS, SF_SEQ_BITS))
            self.data_center = int(self.masked_id(SF_DC_BITS, SF_WORK_BITS + SF_SEQ_BITS))
            self.ts = int(self.masked_id(SF_TIME_BITS, SF_DC_BITS + SF_WORK_BITS + SF_SEQ_BITS))
            self.sample_set = self.ts % 100
            # originally  ((self.id >> 22) + TWEPOCH)/1000.0 
            self.timestamp = (self.ts + TWEPOCH)/1000.
            self.timeStruct = time.gmtime(self.timestamp)
            self.timeString = time.strftime(FMT, self.timeStruct)
            self.year = self.timeStruct.tm_year
            self.month = self.timeStruct.tm_mon
            self.day = self.timeStruct.tm_mday
            self.hour = self.timeStruct.tm_hour
            self.min = self.timeStruct.tm_min
            self.sec = self.timeStruct.tm_sec
            self.dow = self.timeStruct.tm_wday
            self.doy = self.timeStruct.tm_yday
            #self.trials = [self.ndigits(self.id, 2)
            #        , self.ndigits(self.ts, 2)
            #        , self.ndigits(self.timestamp, 2)]
        if len(ns) == 0 or self.year < 2010 or self.year > datetime.datetime.now().year + 1:
            # no valid snowflake id found
            self.id = id  # pass through input
            self.sequence = self.worker = self.data_center = self.ts = self.timestamp = None
            self.timeStruct = self.timeString = self.year = self.month = self.day = None
            self.hour = self.min = self.sec = self.dow = self.doy = None

    #def ndigits(self, x, n):
        #return int(x - (10**n) * int(x/(10**n)))

    def masked_id(self, bits, pos):
        # returns an int
        mask = int('1'*bits, 2) << pos
        res = (mask & self.id) >> pos
        #print '%s' % bin(self.id).rjust(65)
        #print '%s' % bin(mask).rjust(65)
        #print '%s' % bin(res).rjust(65)
        return res
    
    def get_id_datetime(self):
        return [self.id, self.timeString]

    def __repr__(self):
        res = "#"*15 + "\n"
        res += "id:      %s\n"%self.id
        res += "seq:     %s\n"%self.sequence
        res += "worker:  %s\n"%self.worker
        res += "DS:      %s\n"%self.data_center
        res += "Seconds: %s\n"%self.timestamp
        res += "time:    %s\n"%self.timeString
        return res

if __name__ == "__main__":
    import csv
    wrtr = csv.writer(sys.stdout)
    for r in sys.stdin:
        ns = nRE.findall(r)
        try:
            for x in ns:
                sf = Snowflake(x)
                wrtr.writerow([sf.id
                    , sf.sequence
                    , sf.worker
                    , sf.data_center
                    , sf.timeString
                    , sf.hour
                    , sf.min
                    , sf.sec])
        except IndexError:
            sys.stderr.write( "ERROR %s"%ns)

