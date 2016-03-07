#!/usr/bin/python2.7

# preprocess data before feeding into berkeley parser
#
# get rid of begining spaces, continuous spaces
# change '@' to '-at-', '(' to '-lrb-', ')' to '-rrb-'
#

def preprocess(sent):
	sent = sent.strip()
	sent = ' '.join(sent.split())
	sent = re.sub('@', '-AT-', sent)
	sent = re.sub('\(', '-lrb-', sent)
	sent = re.sub('\)', '-rrb-', sent)

	return sent + '\n'

if __name__ == '__main__':
	import sys
	import re
	for sent in sys.stdin:
		sys.stdout.write(preprocess(sent))
