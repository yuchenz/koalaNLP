#!/usr/bin/python2.7

import os
import codecs
import sys


def build_vocab_index(filename):
	lines = codecs.open(filename, 'r', 'utf-8').readlines()

	vocab = {}
	vocab_count = {}
	max_len = 0
	index = 0
	for line in lines:
		line = line.split()
		max_len = max(max_len, len(line))

		for word in line:
			if word not in vocab:
				vocab[word] = index
				vocab_count[word] = 1
				index += 1
			else:
				vocab_count[word] += 1

	print('max_len:', max_len)
	print('vocab size:', index)

	f = codecs.open(filename + '.vocab', 'w', 'utf-8')
	for word in sorted(vocab, key=lambda x: vocab[x]):
		f.write('{:d}\t{}\t{:d}\n'.format(
			vocab[word],  word, vocab_count[word]))
	f.close()

	f = codecs.open(filename + '.index', 'w', 'utf-8')
	for line in lines:
		line = line.split()
		for word in line:
			f.write(str(vocab[word]) + ' ')
		f.write('\n')
	f.close()


if __name__ == '__main__':
	build_vocab_index(sys.argv[1])
