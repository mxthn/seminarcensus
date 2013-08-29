#!/usr/bin/env python2.7

import sys, pygeoip
from collections import defaultdict

Usage = "./locate.py <Inputfile> <Outputfile>"

ServerFlagDict = defaultdict(list)

if len(sys.argv) >= 3:
	try:
		f = open(sys.argv[1])

		for line in f:
			iplist = line.split("\t")

			serverflag = iplist[0]
				
			for ip in iplist[1:len(iplist)-1]:
				ServerFlagDict[serverflag].append(ip)
				
		f.close()

		#Write Result File
		fresult = open(sys.argv[2], "a+")
		
		for key in ServerFlagDict:
			fresult.write(key+"\t"+str(len(ServerFlagDict[key])))
			fresult.write("\r\n") 	

		fresult.close

	except IOError:
		print "Error!!!"

else:
	print Usage
