#!/usr/bin/python2.7

import nltk
import sys

def tree2pos(line):
	tree = nltk.Tree(line)
	print ' '.join([word + '_' + pos for word, pos in tree.pos()])

if __name__ == '__main__':
	for line in sys.stdin:
		tree2pos(line)
