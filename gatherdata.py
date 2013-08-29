#!/usr/bin/env python2.7

import sys, os, threading, re, urllib, signal
from collections import defaultdict

Usage = "Usage: ./analyse <Folder> <Server String> <Search Pattern> [[Result File] Number of parallel threads(default: 8)]\n\
	 Folder: The Folder you want to analyse recursively\n\
	 Server String: The String represents a Server Class you want to find e.g. Apache, nginx, IIS, SAP\n\
	 Search Pattern: A Python-style regular Expression to Match Server Versions e.g. Apache.*1.3.* to\n\
	 find Apache versions containing 1.3 in their version number\n\
	 Result File: File to write result to.\n\
	 \n\
	 EXAMPLE:\n\
	 ./analyse.py /path/to/files apache \".*1.3.*(Unix)\" 2\n\
	 ./analyse.py /path/to/files SAP SAP 8"


#Regular Expressions to parse HTTP Response
regex = {
	"Server" : "Server: (.+?)\r\n",
	#"Status" : "(.+?)\r\n" #First Line is Status Line
	}

##########################################################
##########		Classes			##########
##########################################################
#Class that provides Analysis Algorithm
class AnalysisThread(threading.Thread):
	def __init__(self, path, file, searchstring, searchpattern, countingsem, resultfile, filewritelock):
		threading.Thread.__init__(self)
		self.path = path
		self.file = file
		self.searchstring = searchstring
		self.searchpattern = searchpattern
		self.countingsem = countingsem
		self.resultfile = resultfile
		self.filewritelock = filewritelock	
		#Dictionary to Save IP Lists indexed with Serverversion
		self.evalDictionary = defaultdict(list)	

	def run(self):
		scandata = open(self.path+"/"+self.file, "r")

		for line in scandata:
			if self.searchstring.lower() in line.lower():
			#if self.searchpattern.search(line):			
				lineSplit = line.split("\t")
				#Safe IP
				ip = lineSplit[0]
				timestamp = lineSplit[1]
				scanstatus = lineSplit[2]
				
				#Parse Http Response Header
				response = urllib.unquote(lineSplit[3].replace("=","%"))
				for key in regex:
					m = re.search(regex[key], response, re.I)
					
					if m and len(m.group()) >= 1:
						#print key + m.group(1)
						serverflag = m.group(1)
						
						#Check if sap is found in Serverflag
						#if self.searchpattern.lower() in serverflag.lower():	
						if self.searchpattern.search(serverflag):					
							#defaultdict(list) adds key if it doesn't exist						
							
							iplist =  self.evalDictionary[serverflag]
							
							if not ip in iplist:
								iplist.append(ip)
								print "Added Ip "+ip+"  to Dictionary with Key: " + serverflag
								
		self.writeResults()

		#Release Semaphore to allow the main Thread to create another worker thread
		self.countingsem.release()
	def writeResults(self):
		#Write results but do it synchronized
		self.filewritelock.acquire()
		print "Writing results for "+self.file
		f = open(self.resultfile, "a+")	#append to file
		if f:
			for key in self.evalDictionary:
				iplist = self.evalDictionary[key]
				f.write(key)
				for ip in iplist:		
					f.write("\t"+ip)
				f.write("\t\r\n")
		f.flush()
		f.close()
		self.filewritelock.release()

##########################################################
##########		Functions		##########
##########################################################
#Function to List Directory Contents Recursively
def listDirContent(filepath, general, pattern, result):
	if os.path.isdir(filepath) == True:
		for filename in os.listdir(filepath):
			if os.path.isdir(filepath+"/"+filename) == True:
				print "Stepping down into folder "+filename
				listDirContent(filepath+"/"+filename) 
			else:
				#Reduce Threads that my be created by 1 if 0 acquire() blocks
				semThreadCounter.acquire()
				print "Started new Job. File "+filepath+"/"+filename+" is being parsed"
				thread = AnalysisThread(filepath, filename, general, pattern, semThreadCounter, result, fileLock)
				thread.start()
	else:
		print filepath+" is not a directory\n"+Usage

#Signal Handler to explicityly close the Python Interpreter
def handler(signum, frame):
	print 'Signal handler called with signal', signum
	sys.exit(0)	


##########################################################
##########		Main Function		##########
##########################################################
#Test if there are enough parameters set		
if len(sys.argv) < 5:
	print Usage
else:
	#Parse Optional Thread Count Input
	if len(sys.argv) >= 6:
		if sys.argv[5].isdigit():
			nThreadCount = int(sys.argv[5])
		else:
			print Usage
	else:
		nThreadCount = 8

	#Resultfile
	filename = "empty"
	if len(sys.argv) >= 5:
		filename = sys.argv[4]
	else:
		print Usage

	#Directorystring
	directory = sys.argv[1]	

	#General Search String for faster Seperation
	generalString = sys.argv[2]

	#Try to compile regex pattern
	try:
		compiledPattern = re.compile(sys.argv[3], re.I)
	except SynthaxError:
		print Usage + "\n" + sys.argv[3] + " is not a valid regex\n"
		sys.exit()
		
	#Setup Signal Handler to close Script properly
	signal.signal(signal.SIGINT, handler)

	#Setup Threadcounter Semaphore
	semThreadCounter = threading.Semaphore(nThreadCount)
	
	#Setup Filelock
	fileLock = threading.Lock()	
	
	#Start Analysis
	print "Analysis started on %d threads with Searchpattern %s" % (nThreadCount,sys.argv[2])
	listDirContent(directory, generalString, compiledPattern, filename)

	
