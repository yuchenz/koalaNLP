#!/usr/bin/python2.7

def simplifyTree(tr):
	'''
	if a subtree in this tree has only one child, combine the subtree's node label and the child's node label,
	and reduce a level of the subtree (keep POS tags for words)

	e.g.

	input: "(TOP (S (NP (NN (XX I))) (VP (XX (VV love) (NP (XX (NN python)))))))"
	output: "(TOP+S (NP+NN (XX I)) (VP+XX (VV love) (NP+XX (NN python))))" 
	
	'''
	stack = [tr]
	while stack:
		pointer = stack.pop() 
		if pointer.height() <= 2:
			continue
		while len(list(pointer)) == 1:
			if pointer.height() <= 3:
				break
			child = pointer[0]
			pointer.node += '+' + child.node 
			pointer.pop()
			for ch in child:
				pointer.append(ch)
		else:
			for child in pointer:
				stack.append(child)

	return tr

if __name__ == '__main__':
	import sys
	import nltk
	for tree in sys.stdin:
		tr = nltk.Tree(tree)
		simTr = simplifyTree(tr)
		print simTr.pprint().encode('utf-8')

