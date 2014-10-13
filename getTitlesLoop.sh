#!/bin/bash

outFile="animeTitles.csv"
curYear=`date +%Y`
startYear=1960
lastYear=$curYear

if [ -e $outFile ] ; then
	rm $outFile
fi

for ((year=$startYear; year<=$lastYear; year++))
do
	python getTitles.py $year >> $outFile
	sleep 15s
done