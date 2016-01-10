#!/usr/bin/python2.7

import codecs
import sys
import pdb

def main(wholeFile, partFile, wholeParaFile, partParaFile):
	wF = codecs.open(wholeFile, 'r', 'utf-8').read().split('\n')[:-1]
	pF = codecs.open(partFile, 'r', 'utf-8').read().split('\n')[:-1]
	wPF = codecs.open(wholeParaFile, 'r', 'utf-8').read().split('\n')[:-1]

	print len(wF), len(pF), len(wPF)

	assert len(wF) == len(wPF), "wholeFile and wholeParallelFile don't have same number of sentences!!!"

	pPF = codecs.open(partParaFile, 'w', 'utf-8')
	i, j = 0, 0
	while i < len(pF):
		if pF[i] == wF[j]:
			pPF.write(wPF[j] + '\n')
			i += 1
		j += 1
	pPF.close()

if __name__ == '__main__':
	wholeFile = sys.argv[1]
	partFile = sys.argv[2]
	wholeParaFile = sys.argv[3]
	partParaFile = sys.argv[4]

	main(wholeFile, partFile, wholeParaFile, partParaFile)
