#!/usr/bin/python2.7

# given two rule tables (used by hiero mt systems), the first rule talbe is a subset of the second one
# find all rules from the first rule table in the second table
# copy their probabilities and counts from the second rule table to replace their probabilities and counts in the first table

import sys, codecs

def replace(toFile, fromFile):
	bigDict = {}
	print "reading in the big rule table ..."
	for line in codecs.open(fromFile, 'r', 'utf-8'):
		line = line.split("|||")
		key = "|||".join(line[:2])
		value = "|||".join(line[2:])
		bigDict[key] = value
	
	print "writing out the replaced small rule table ..."
	outF = codecs.open(toFile+'.replaced', 'w', 'utf-8')
	for line in codecs.open(toFile, 'r', 'utf-8'):
		line = line.split("|||")
		key = "|||".join(line[:2])
		outF.write(key + '|||')
		if key not in bigDict:
			outF.write("|||".join(line[2:]))
		else:
			outF.write(bigDict[key])
	
	outF.close()

if __name__ == "__main__":
	replace(sys.argv[1], sys.argv[2])
