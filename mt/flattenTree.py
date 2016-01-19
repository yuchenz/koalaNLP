#!/usr/bin/python2.7

# flatten a parse tree to relax syntax restriction for mt rule extraction
# syntax: cat filename | ./flattenTree.py level

import sys
import nltk

def flatten2one(tr):
	newLine = '(' + tr.node + ' '
	for subt in tr.subtrees():
		if subt.height() == 2:
			if isinstance(subt.node, str) and isinstance(subt[0], str):
				newLine += '(' + subt.node + ' ' + subt[0] + ') '
			else:
				print subt
				exit(1)
	newLine += ')'
	newTr = nltk.ParentedTree(newLine)
	#print 'newTr is: ', newTr
	return newTr

def flatten(line, level):
	tr = nltk.ParentedTree(line.strip())
	#if the tree's height is smaller or equal to 3, no changes are needed
	if tr.height() <= 3:
		return ' '.join(tr.pprint().split())

	# if level is greater than tree's height, set it to tree's height, which means the most flattening
	if level > tr.height():
		level = tr.height()

	#print 'tr is: ', tr
	for subt in tr.subtrees():
		#print 'subt is: ', subt, 'height is: ', subt.height(),
		if subt.height() == level:
			#print 'yes!'
			if subt.parent():
				subt.parent()[subt.parent_index()] = flatten2one(subt)
			else:
				tr = flatten2one(subt)
				break
		else:
			#print 'no!'
			continue
	return ' '.join(tr.pprint().split())

if __name__ == "__main__":
	level = int(sys.argv[1])
	assert level > 3, "level has to be at least 4, level smaller than 4 doesn't flatten the tree"

	#print 'level is: ', level
	for line in sys.stdin:
		#print 'line is: ', line
		line = flatten(line, level)
		sys.stdout.write(line + '\n')
