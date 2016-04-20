#!/usr/bin/python2.7

import sys
import codecs

def extract(chF, enF, waF):
	chSentL = [line.split() for line in codecs.open(chF, 'r', 'utf-8').readlines()]
	enSentL = [line.split() for line in codecs.open(enF, 'r', 'utf-8').readlines()]
	waSentL = [line.split() for line in codecs.open(waF, 'r', 'utf-8').readlines()]

	assert len(chSentL) == len(enSentL) == len(waSentL), "len of ch, en, wa == %d, %d, %d" % (len(chSentL), len(enSentL), len(waSentL))

	D = {}
	for k, waSent in enumerate(waSentL):
		for wa in waSent:
			i = int(wa.split('-')[0])
			j = int(wa.split('-')[1])
			D[(chSentL[k][i], enSentL[k][j])] = D.get((chSentL[k][i], enSentL[k][j]), 0) + 1
	
	return D

if __name__ == "__main__":
	chF = sys.argv[1]
	enF = sys.argv[2]
	waF = sys.argv[3]
	
	D = extract(chF, enF, waF)

	for key in sorted(D, key=lambda x: D[x], reverse=True):
		print key[0].encode('utf-8') + '\t' + key[1].encode('utf-8') + '\t' + str(D[key])
