#!/usr/bin/python2.7

# check if some trees are legal trees that can be parsed by nltk.Tree
# syntax: cat filename | ./isLegalTree.py

import sys
import nltk

def isLegalTree(line, i):
	try:
		t = nltk.Tree(line)
		pt = nltk.ParentedTree(line)
	except ValueError:
		print >> sys.stderr, "illegal tree!!! #" + str(i)
		print >> sys.stderr, line
		exit(1)

if __name__ == "__main__":
	i = 0
	for line in sys.stdin:
		isLegalTree(line, i)
		i += 1
		if i % 1000 == 0: print >> sys.stderr, '.',
