#!/usr/bin/env python2.7

import sys, pygeoip
from collections import defaultdict

Usage = "./locate.py <Inputfile> <Outputfile>"

geoLocatedIpDict = defaultdict(list)

if len(sys.argv) >= 3:
	#try:
		f = open(sys.argv[1])

		CityGeoDB = pygeoip.GeoIP("geoip-db/GeoIPCity.dat", pygeoip.MEMORY_CACHE)		

		for line in f:
			iplist = line.split("\t")

			serverflag = iplist[0]
				
#			print "##### Evaluating GeoIp-Data for IP\'s running " + serverflag

			for ip in iplist[1:len(iplist)-1]:
				#print ip
				try:
					entry = CityGeoDB.record_by_addr(ip)		
				except Exception as ipexception:
					print type(ipexception)
					print ip
			
				if entry:
					resulttuple = (ip, entry["country_code3"], entry["country_name"],  entry["city"], entry["latitude"], entry["longitude"])
					geoLocatedIpDict[serverflag].append(resulttuple)
					#print str(resulttuple)
				else:
					print "Coult not locate IP: " + ip + "\n"
				
		f.close()

		#Write Result File
		fresult = open(sys.argv[2], "a+")
		
		for key in geoLocatedIpDict:
			fresult.write(key+"\n")
			for iplist in geoLocatedIpDict[key]:
				for iplistentry in iplist:
					fresult.write(str(iplistentry)+"\t")
					#print str(iplistentry)
				fresult.write("\t\r\n") 
	
		fresult.close
	#except IOError:
	#	print "Error!!!"

else:
	print Usage
