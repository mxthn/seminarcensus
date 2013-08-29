#!/usr/bin/env python2.7

import sys, os
#from collections import defaultdict

Usage = "./visualize <Inputfile> <Outputfile>"	 

try:
	if len(sys.argv) >= 3:
		infilename = sys.argv[1]
		outfilename = sys.argv[2]	

		infile = open(infilename, "r")
		outfile = open(infilename.split(".")[0]+".pins", "w+")

		for line in infile:
			linesplit = line.split("\t")

			if len(linesplit) > 1:
				outfile.write("["+linesplit[0]+"]\n")
				outfile.write("latitude: "+linesplit[4]+"\n")
				outfile.write("longitude: "+linesplit[5]+"\n\n")

		outfile.close()
		infile.close()

		#Execute World Map Generation
		#nugsl-worldmap -o 443-HTTPS-SAP-Worldmap.svg --pin-file=443-HTTPS-Worldmap.pins
		os.system("nugsl-worldmap -o "+outfilename+" --pin-file="+infilename.split(".")[0]+".pins")
		os.remove(os.getcwd()+"/"+infilename.split(".")[0]+".pins")
		os.remove(os.getcwd()+"/"+outfilename.split(".")[0]+".pickle")
	else:
		print Usage
except IOError:
	print "IOError"

