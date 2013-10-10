#!/usr/bin/env bash

publist="disqus foursquare tumblr twitter wp-com stocktwit"
echo $(date)

tmpfile="$TMPDIR/gnacstest.tmp"
if [ -e $tmpfile ]; then
    rm $tmpfile
fi

for pub in $publist; do
    echo "Parsing $pub..."
    fn="../data/${pub}_sample.json"
    echo " Records for $pub from $fn..."
    ../gnacs.py -gilustorz $pub $fn >> $tmpfile
    echo " Explanation for $pub from $fn..."
    ../gnacs.py -xgilustorz $pub $fn >> $tmpfile
    echo " Pretty $pub from $fn..."
    ../gnacs.py -p $fn >> $tmpfile
    echo " GeoJSON $pub from $fn..."
    ../gnacs.py -jgz $pub $fn >> $tmpfile
    echo " tail-test $pub from $fn..."
    ../gnacs.py -z $pub $fn | tail >> $tmpfile
done

echo "Output: $(cat $tmpfile | wc -l) should be 34807"
echo "GNIP lines: $(cat $tmpfile | grep GNIP | wc -l) should be 1"

if [ -e $tmpfile ]; then
    rm $tmpfile
fi

