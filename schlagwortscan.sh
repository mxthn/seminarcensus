#!/bin/bash

Usage="./schlagwortscan.sh <Liste von Schlagworten> <Liste von Ports>"

if [ -z $1 -o  -z $2 ] || [ ! -a $1 -o ! -a $2 ]; then
	echo $Usage;
	exit;
fi

for searchitem in $(cat $1);
	do (
		#./gatherdata.py Usage: ./analyse <Folder> <Server String> <Search Pattern> [[Result File] Number of parallel threads(default: 8)]
		for port in $(cat $2);
			do /usr/bin/time -o Times.info -a -f $searchitem-$port"\t%e real\t%U user\t%S sys" ./gatherdata.py /storage/TCP_GetRequest/$port-TCP_GetRequest $searchitem 'SAP ' $searchitem-VulnServicesOnPort-$port.schlagwort 1 > /dev/null;
			mv $searchitem-VulnServicesOnPort-$port.schlagwort VulnScanResults/
		done;
	);
done;
