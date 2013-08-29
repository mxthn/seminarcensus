#!/bin/bash

Usage="./master <directory> <scanname> <server> <pattern>"

if [ -z $1 ] || [ ! -d $1 ] || [ -z $2 ] || [ -z $3 ] || [ -z "$4" ]; then
	echo $Usage;
	exit;
fi

./gatherdata.py $1 $3 "$4" $2.result 1;
./locate.py $2.result $2.located;
./visualize.py $2.located $2.svg;
./statistics.py $2.result $2.statistics

#mv $2.result Results/;
#mv $2.located Results/;
#mv $2.svg Results/;
#mv $2.statistics Results/;
