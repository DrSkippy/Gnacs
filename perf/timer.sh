#!/usr/bin/env bash
# start in Gnacs

echo $(date)
for n in 100 1000 10000 100000 1000000 2500000; do
    echo "################### $n ####################"
    cd ..
    unset PYTHONPATH
    echo "Original ($n) $(pwd) $(which gnaces.py)"
    for m in 1 2 3; do
        echo "   Trial ($m)"
        time $(head -qn${n} /mnt/shendrickson/big_twitter.json | gnacs.py -gilsturaoz twitter > /dev/null)
    done
    cd Gnacs
    export PYTHONPATH=./acscsv
    echo "New ($n) $(pwd) $(which gnaces.py)"
    for m in 1 2 3; do
        echo "   Trial ($m)"
        time $(head -qn${n} /mnt/shendrickson/big_twitter.json | ./gnacs.py -gilsturaoz twitter > /dev/null)
    done
done
echo $(date)
