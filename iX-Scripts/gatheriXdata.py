#!/usr/bin/env python2.7

import threading,sys,os
from time import sleep
from collections import defaultdict

Usage = "./gatheriXdata.py <Search String> <Port> <Input Folder> <Output File> [<Filter Files>]"

class CGatheringThread(threading.Thread):
	
	WriteLock = threading.Lock()
	SearchString = ""
	OutputFile = ""
	Port = ""
	
	def __init__(self, InputFile):
		threading.Thread.__init__(self)
		self.InputFile = open(InputFile, "r")
		self.ResultList = []
		print InputFile + " is being parsed."

	def run(self):
		for line in self.InputFile:
			if CGatheringThread.SearchString.lower() in line.lower():
				line = line.strip("\n")
				LineArray = line.split("\t")
				self.ResultList.append([LineArray[0], CGatheringThread.Port, LineArray[3]])				
			
		self.InputFile.close()
		self.output()
		Semaphore.release()

	def output(self):
		self.WriteLock.acquire()

		f = open(CGatheringThread.OutputFile, "a+")
		for ListEntry in self.ResultList:
			f.write(ListEntry[0]+"\t"+ListEntry[1]+"\t"+ListEntry[2]+"\n")
		f.close()

		self.WriteLock.release()

####################################################

if len(sys.argv) < 5 or len(sys.argv) > 6:
	print Usage
	sys.exit()
elif len(sys.argv) == 6:
	FilterList = sys.argv[5]	

Semaphore = threading.Semaphore(4)
CGatheringThread.SearchString = sys.argv[1]
CGatheringThread.Port = sys.argv[2]
CGatheringThread.OutputFile = sys.argv[4]

if not os.path.isdir(sys.argv[3]):
	print sys.argv[3]+" is not a directory."
else:
	InputFolder = sys.argv[3]

for InputFile in os.listdir(InputFolder):
	Semaphore.acquire()
	thread = CGatheringThread(InputFolder+"/"+InputFile)
	thread.start()

#### Filter Results ####
#......................#
if len(sys.argv) == 6:
	FilterStrings = []
	FilterExpressionFile = open(FilterList, "r")
	for BadWord in FilterExpressionFile:
		if len(BadWord) > 3:
			FilterStrings.append(BadWord.strip("\n"))
	FilterExpressionFile.close()

	while threading.activeCount() > 1:
		print str(threading.activeCount())+" active Threads...\nSleeping 500ms"
		sleep(0.5)

	ResultFile = open(CGatheringThread.OutputFile, "r")
	FilteredResults = open(CGatheringThread.Port+"-"+CGatheringThread.SearchString+".filteredResults", "w+")

	print "Started Filtering"
	for line in ResultFile:
		BadWordFound = False
		for BadWord in FilterStrings:
			if BadWord.lower() in line.lower():
				print BadWord + " found"
				BadWordFound = True
				break
	
		if not BadWordFound:
			FilteredResults.write(line)

	ResultFile.close()
	FilteredResults.close()
