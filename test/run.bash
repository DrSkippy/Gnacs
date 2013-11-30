#!/usr/bin/env bash

publist="disqus foursquare getglue newsgator stocktwit tumblr twitter wp-com"
echo $(date)

tmpfile="$TMPDIR/gnacstest.tmp"
if [ -e $tmpfile ]; then
    rm $tmpfile
fi

echo "Calculating current test data size..."
# total record count (all files)
linecount=$(cat ../data/*.json | wc -l)
# total prettified linecount
plinecount=$(cat ../data/*.json | ../gnacs.py -p | wc -l)
# total num of files
filecount=$(find ../data/ -name '*.json' | wc -l)

opts='gilustorz'

for pub in $publist; do
    echo "Parsing $pub..."
    fn="../data/${pub}_sample.json"
    #
    echo " Records for $pub from $fn ...."
    #../gnacs.py -$opts $pub $fn >> $tmpfile
    cmd="../gnacs.py -$opts $pub $fn" 
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile 
    # one line per record per file
    # total = linecount 
    #
    echo " Explanation for $pub from $fn ...."
    #../gnacs.py -x$opts $pub $fn >> $tmpfile
    cmd="../gnacs.py -x$opts $pub $fn"
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile
    # one line per record per file
    # total = 2*linecount 
    #
    echo " Pretty $pub from $fn ...."
    #../gnacs.py -p $fn >> $tmpfile
    cmd="../gnacs.py -p $fn"
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile
    # arb lines per record
    # total = plinecount + 2*linecount
    #
    echo " GeoJSON $pub from $fn ...."
    #../gnacs.py -jz $pub $fn >> $tmpfile
    cmd="../gnacs.py -jz $pub $fn"
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile
    # one line per file
    # total = filecount + plinecount + 2*linecount
    #
    echo " tail-test $pub from $fn ...."
    #../gnacs.py -z $pub $fn | tail >> $tmpfile
    cmd="../gnacs.py -z $pub $fn | tail"
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile
    # 10 lines per file
    # total = (10+1)*filecount + plinecount + 2*linecount 
    #
    echo " custom keypath test $pub from $fn ...."
    #../gnacs.py -z $pub $fn -k'id' | tail >> $tmpfile
    cmd="../gnacs.py -z $pub $fn -k'id' | tail"
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile
    # flees are nowhere to be found, but still gives PATH_EMPTY
    #../gnacs.py -z $pub $fn -k'id:mydoghasflees' | tail >> $tmpfile
    cmd="../gnacs.py -z $pub $fn -k'id:mydoghasflees' | tail"
    echo $cmd
    echo "lines: $(eval $cmd | wc -l)"
    eval $cmd >> $tmpfile
    # 10 lines per file for 'id', 10 more for flees
    # total = (20+11)*filecount + plinecount + 2*linecount
    #
    # don't really need this many tests
    #../gnacs.py -z $pub $fn -k'object:id' | tail >> $tmpfile
    #../gnacs.py -z $pub $fn -k'object:id:mydoghasflees' | tail >> $tmpfile
    #../gnacs.py -z $pub $fn -k'object:id:1' | tail >> $tmpfile
done

echo "***********"
echo "linecount: $linecount"
echo "prettified linecount: $plinecount"
echo "filecount: $filecount"
echo "***********"
echo
# update 'should be' math as needed
echo "Output: $(cat $tmpfile | wc -l) should be $((31*$filecount + $plinecount + 2*$linecount))"
echo "GNIP lines: $(cat $tmpfile | grep GNIP | wc -l) should be 1"

if [ -e $tmpfile ]; then
    rm $tmpfile
    echo
    echo "(removed $tmpfile)"
fi

