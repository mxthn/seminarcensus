#!/usr/bin/env python2.7

import sys, pygeoip
from collections import defaultdict

Usage = "./xyz.py <vulnflag> <Inputfile.statistics> <Outputfile.vulnerable>"

if len(sys.argv) >= 4:
	try:
		keyword = sys.argv[1]
		keywordcount = 0

		f = open(sys.argv[2])

		for line in f:
			if sys.argv[1] in line.lower():
				keywordcount += int(line.split("\t")[1])
			
		f.close()

		#Write Result File
		fresult = open(sys.argv[3], "a+")
		fresult.write(keyword +"\t"+str(keywordcount)+"\r\n")
		fresult.close

	except IOError:
		print "Error!!!"

else:
	print Usage
