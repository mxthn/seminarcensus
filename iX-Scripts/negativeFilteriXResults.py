#!/usr/bin/env python2.7

import threading,sys,re
import urllib
from collections import defaultdict

Usage = "./filteriXdata.py <Search String> <Input File> <Output File> <Badword List>"

#### Workaround for filtering Set-Cookie matches ####
#### Ascii 0D = Carriage Return - 0A = Line Feed ####
CookieFilter = re.compile("set-cookie: (.*)sap(.*)\r\n", re.I)

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

for BadWord in FilterExpressionFile:
	if len(BadWord) > 3:
		FilterStrings.append(BadWord.strip("\n"))

FilterExpressionFile.close()

#### Do real filtering ####
#.........................#
ResultFile = open(InputFile, "r")
FilteredResults = open(OutputFile, "w+")

print "Started Filtering"
for line in ResultFile:
	if SearchString.lower() in line.lower():

		if SearchString.lower() == "sap":
			Response = line.split("\t")[2]
			Response = urllib.unquote(Response.replace("=","%"))
			Match = CookieFilter.search(Response)
	
			##Filter Strings that contain the Set-Cookie hash containing SAP
			if Match and Response.lower().count(SearchString.lower()) < 2:
				##SAP String is only in Set Cookie
				#print "SAP RegEx workaround match."
				continue
						
		BadWordFound = False
		for BadWord in FilterStrings:
			if BadWord.lower() in line.lower():
#				print BadWord + " found"
				BadWordFound = True
				break

		if not BadWordFound:
			ip = line.split("\t")[0]
			if ip not in ResultDict:
				FilteredResults.write(line)
				ResultDict[ip] = line
			else:
				print "Filtered double IP"

ResultFile.close()
FilteredResults.close()

