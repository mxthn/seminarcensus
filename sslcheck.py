#!/usr/bin/env python2.7

import sys, threading, os, signal
from collections import defaultdict

Usage = "./sslcheck.py <SSLServiceprobeDirectory> <ServiceFilePraefix>  <Inputfile.iplist> <Outputfile.sslcheckresult> \n\
\n\
EXAMPLE:\n\
./sslcheck.py /storage/TCP_SSLProbes/443-TCP_SSLv23SessionReq 443-TCP_SSLv23SessionReq- 443-SAP-SSLCheck.iplist output\n"

############################################
############   Analysis Class   ############
############################################
class AnalysisThread(threading.Thread):
	outfilelock = threading.Lock()
	
	def __init__(self, lock, netpraefix, iprange, inputpath, filepraefix, outputfilename):
		threading.Thread.__init__(self)		
		self.lock = lock
		self.iprange = iprange
		self.sortIpRange()
		self.inputfile = open(inputpath+"/"+filepraefix+netpraefix, "r")
		self.outputfile = open(outputfilename, "a+")
		self.resultdict = defaultdict(str)

	def run(self):
		currentlistkey = 0
		currentip = self.iprange[currentlistkey]

		for line in self.inputfile:
			if  currentip.lower() in line.lower():
				status = line.split("\t")[2] 	#3 value is port state
				self.resultdict[currentip] = status

				##We have found our IP go to the next one
				currentlistkey = currentlistkey + 1
				if currentlistkey < len(self.iprange):
					currentip = self.iprange[currentlistkey]

		if currentlistkey + 1 != len(self.iprange):
			print "You should have looked better for me: "+currentip
			print "Current Key: "+str(currentlistkey)+"Max. Key "+str(len(self.iprange)) 
		self.writeResult()
		self.inputfile.close()
		self.outputfile.close()
		self.lock.release()

	def sortIpRange(self):
		for i in range(len(self.iprange)):
			self.iprange[i] = "%3s.%3s.%3s.%3s" % tuple(self.iprange[i].split("."))
		self.iprange.sort()

		for i in range(len(self.iprange)):
			self.iprange[i] = self.iprange[i].replace(" ", "")
	
	def writeResult(self):
		AnalysisThread.outfilelock.acquire()
		
		for ip in self.resultdict:
			self.outputfile.write(ip+"\t"+self.resultdict[ip]+"\r\n")

		AnalysisThread.outfilelock.release()
	

############################################
###########    Signal Handler   ############
############################################
def signalhandler(signum, frame):
	print "Caught Signal Handler" + str(signum)
	os.exit(0)

############################################
############	Main Function	############
############################################
IpRangeDict = defaultdict(list)

if len(sys.argv) != 5:
	print Usage
	sys.exit()

#Setup Signalhandling
signal.signal(signal.SIGINT, signalhandler)

##Setup Information provided through args
serviceprobepath = sys.argv[1]
praefix = sys.argv[2]
ipfilepath = sys.argv[3]
outputpath = sys.argv[4]

ipfile = open(ipfilepath, "r")

##Arrange IP's in Dictionary
for ip in ipfile:
	classanet = ip.split(".")[0]	##Get first 3 digits of IP
	classaiplist = IpRangeDict[classanet]
	ip = ip.replace("\r\n", "")
	classaiplist.append(ip)

threadsema = threading.Semaphore(4)
for anet in IpRangeDict:
	threadsema.acquire()
	SSLCheckThread = AnalysisThread(threadsema, str(anet), IpRangeDict[anet], serviceprobepath, praefix, outputpath)
	SSLCheckThread.start()
