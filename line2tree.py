#!/bin/python
# -*- coding: utf-8 -*-

# convert a file of syntactic trees of sentences in the format of lines into format of tree structures
# python line2tree.py [file] [INPUT FILE] > [OUTPUT FILE]

# OR convert a line of tree into tree structure
# python line2tree.py [sent] [INPUT LINE TREE]

# e.g. in input file:
#		( (IP (NP (NP (NR 深圳)) (CP (IP (VP (VV 嫁) (NP (NR 港))))) (NP (NN 姑娘))) (VP (ADVP (AD 逐年)) (VP (VV 减少)))) )
#	in output file:
#		

import sys
from nltk.tree import *

op = sys.argv[1]

lines = []
if op == "file":
	inf = open(sys.argv[2])
	lines = inf.readlines()
	inf.close()
elif op == "sent":
	lines.append(sys.argv[2])

print
for line in lines:
	if line == "\n":
		continue
	sentT = Tree(line)
	print sentT.pprint()
	print

