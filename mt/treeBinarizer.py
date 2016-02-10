#!/usr/bin/python2.7

import sys
import nltk
import pdb

vvTags = "VV VBD VBZ VBG VB VBP VBN VC VA VRD VE VCD VPT VNV VSB VP".split()

def output(tr):
	print >> sys.stderr, tr.node, "==>",
	for child in tr:
		print >> sys.stderr, child.node,
	print >> sys.stderr

def rightBinarize(tr):
	children = []
	for child in tr:
		children.append(child)
	
	tmpNode = children[-1] 
	i = len(children) - 2
	while i > 0:
		tmpNode2 = nltk.Tree("(X)")
		tmpNode2.append(children[i])
		tmpNode2.append(tmpNode)
		tmpNode = tmpNode2
		i -= 1
	
	while len(tr) > 1:
		tr.pop()

	tr.append(tmpNode)
	
def leftBinarize(tr):
	children = []
	for child in tr:
		children.append(child)
	
	tmpNode = children[0] 
	i = 1
	while i < len(children) - 1:
		tmpNode2 = nltk.Tree("(X)")
		tmpNode2.append(tmpNode)
		tmpNode2.append(children[i])
		tmpNode = tmpNode2
		i += 1
	
	while len(tr) > 1:
		tr.pop(0)

	tr.insert(0, tmpNode)

def vvBinarize(tr):
	children = []
	vvIndex = None
	for i, child in enumerate(tr):
		children.append(child)
		if child.node in vvTags: 
			vvIndex = i
	
	if vvIndex == None:
		print >> sys.stderr, "no vv in the children!!!",
		output(tr)
		return
	
	tmpNode = nltk.Tree("(X)")
	for i in xrange(vvIndex, len(tr)):
		tmpNode.append(children[i])
	leftBinarize(tmpNode)

	while len(tr) > vvIndex:
		tr.pop()
	tr.append(tmpNode)
	rightBinarize(tr)

def binarize(line, lan = "en"):
	assert lan in ['en', 'ch'], "illegal language (en or ch): %s" % lan

	root = nltk.Tree(line)
	stack = [root]
	while stack:
		curNode = stack.pop()
		if len(curNode) > 2:
			if curNode.node == 'NP':
				rightBinarize(curNode)
			elif curNode.node == 'VP':
				if lan == 'en':
					vvBinarize(curNode)
				elif lan == 'ch':
					if curNode[0].node in vvTags: 
						leftBinarize(curNode)
					elif curNode[-1].node in vvTags: 
						rightBinarize(curNode)
					else:
						vvBinarize(curNode)

		for child in curNode:
			#print >> sys.stderr, child
			if child.height() > 2:
				stack.append(child)
		continue

	return ' '.join(root.pprint().split()) + '\n'

if __name__ == "__main__":
	'''
	# test
	tr = nltk.Tree("(S (NN 1) (NN 2) (NN 3) (NN 4) (NP (NN 5) (NN 6) (NN 7)))")
	print >> sys.stderr, tr
	rightBinarize(tr)
	print >> sys.stderr, "right binarize:"
	print >> sys.stderr, tr
	print >> sys.stderr, 

	tr = nltk.Tree("(S (NN 1) (NN 2) (NN 3) (NN 4) (NP (NN 5) (NN 6) (NN 7)))")
	print >> sys.stderr, tr
	leftBinarize(tr)
	print >> sys.stderr, "left binarize:"
	print >> sys.stderr, tr
	print

	tr = nltk.Tree("(S (NN 1) (NN 2) (VV 3) (NN 4) (NP (NN 5) (NN 6) (NN 7)))")
	print >> sys.stderr, tr
	vvBinarize(tr)
	print >> sys.stderr, "vv binarize:"
	print >> sys.stderr, tr
	print
	'''

	lan = sys.argv[1]
	for line in sys.stdin:
		line = binarize(line.strip(), lan)
		sys.stdout.write(line)
