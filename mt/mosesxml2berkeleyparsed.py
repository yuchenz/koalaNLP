#!/usr/bin/python2.7

# convert moses' second xml format trees into berkeley format trees
# used on moses' relax-parse output binarized trees

# syntax: ./mosesxml2berkeleyparsed.py < in-parse > out-parse

import sys
import pdb
import codecs
from xml.etree import ElementTree as ET

def convert(line):
	#print line
	xml = ET.fromstring("<boundary> " + line + " </boundary>")
	#for node in xml.iter(): print node.tag, node.attrib
	wordList = xml.text.strip().split()
	#print wordList
	nodeList = [(node.attrib.get('span'), node.attrib.get('label')) for node in xml.iter()][1:]
	#print nodeList
	nodeList = [(int(node[0].split('-')[0]), int(node[0].split('-')[1]), node[1]) for node in nodeList]
	#print nodeList
	nodeList.sort(key = lambda x: x[1], reverse = True)
	#print nodeList
	nodeList.sort(key = lambda x: x[0])
	#print nodeList

	stack = []
	berkeleyFormatTree = ""
	for node in nodeList:
		if node[0] != node[1]:
			stack.append(node)
			berkeleyFormatTree += "(" + node[2] + " "
		else:
			berkeleyFormatTree += "(" + node[2] + " " + wordList[node[0]] + ") "
			while stack != [] and node[1] == stack[-1][1]:
				if berkeleyFormatTree[-1] == " ":
					berkeleyFormatTree = berkeleyFormatTree[:-1] + ") "
				else: 
					berkeleyFormatTree += ") "
				stack.pop()
	
	if stack == []:
		return berkeleyFormatTree + '\n'
	else:
		return "ERROR: illegal xml format tree!!!"

if __name__ == "__main__":
	#sys.stdin = codecs.getreader('utf-8')(sys.stdin)
	#sys.stdout = codecs.getreader('utf-8')(sys.stdout)
	sys.stdout.write('\n')
	for line in sys.stdin:
		sys.stdout.write(convert(line + '\n'))
	sys.stdout.write('\n')

