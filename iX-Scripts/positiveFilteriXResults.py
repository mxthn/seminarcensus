#!/usr/bin/env python2.7

import threading,sys,re
import urllib
from collections import defaultdict

Usage = "./filteriXdata.py <Search String> <Input File> <Output File> <White List>"

if len(sys.argv) != 5:
	print Usage
	sys.exit(-1)

ResultDict = defaultdict(tuple)
FilterList = sys.argv[4]
InputFile = sys.argv[2]
OutputFile = sys.argv[3]
SearchString = sys.argv[1]

#### Filter Results ####
#......................#
FilterStrings = []
FilterExpressionFile = open(FilterList, "r")

for word in FilterExpressionFile:
	if len(word) > 3:
		FilterStrings.append(word.strip("\n"))

FilterExpressionFile.close()

#### Do real filtering ####
#.........................#
ResultFile = open(InputFile, "r")
FilteredResults = open(OutputFile, "w+")

print "Started Filtering"
for line in ResultFile:
	if SearchString.lower() in line.lower():

		Response = line.split("\t")[2]
		Response = urllib.unquote(Response.replace("=","%"))
						
		IsInWhiteList = False
		for word in FilterStrings:
			if word.lower() in Response.lower():
				print "Whitelist match"
				IsInWhiteList = True
				break

		if IsInWhiteList:
			ip = line.split("\t")[0]
			if ip not in ResultDict:
				FilteredResults.write(line)
				ResultDict[ip] = line
			else:
				print "Filtered double IP"

ResultFile.close()
FilteredResults.close()

