#!/bin/sh

for port in $(cat ../Lists/portlist);
	do
		echo nmap -T4 -Pn -p T:$port --script StillAlive.nse -oN result-$port.nmap -iL ../Results/$port-SAP.result-iplist.totest -d;
		nmap -T4 -Pn -p T:$port --script StillAlive.nse -oN result-$port.nmap -iL ../Results/$port-SAP.result-iplist.totest -d;

		echo mv script.log $port-TCP_GetRequest.checked;
		mv script.log $port-TCP_GetRequest.checked;
done;
