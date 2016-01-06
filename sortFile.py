#!/usr/bin/python2.7

# sort all lines in a file

import codecs, sys

def sortLines(filename):
	lines = codecs.open(filename, 'r', 'utf-8').read().split('\n')[:-1]
	lines.sort()
	f = codecs.open(filename+'.sorted', 'w', 'utf-8')
	for line in lines:
		f.write(line+'\n')
	f.close()

if __name__ == "__main__":
	sortLines(sys.argv[1])
