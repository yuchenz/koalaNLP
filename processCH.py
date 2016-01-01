#!/usr/bin/python2.7

import codecs
import argparse
import pdb

def inBasicSet(char):
	'''
	Return True if char is:
		- in basic CJK set (unicode 4E00-9FFF(base 16))
	
	:type char: int 
	:param char: the decimal unicode of a Chinese character
	'''
	return True if char >= int('4e00', 16) and char <= int('9fff', 16) else False

def inPuncSet(char): # Return True if char in is CJK punctuation Set
	return True if char >= int('3000', 16) and char <= int('303f', 16) or \
			char >= int('2000', 16) and char <= int('206f', 16) else False 

def inASet(char): # Return True if char is in extended CJK set A
	return True if char >= int('3400', 16) and char <= int('4dff', 16) else False

def inBSet(char): # Return True if char is in extended CJK set B
	return True if char >= int('20000', 16) and char <= int('2a6df', 16) else False

def inSymbolSet(char): # Return True if char is in some symbol set
	return True if char >= int('ff00', 16) and char <= int('ffef', 16) or \
			char >= int('2500', 16) and char <= int('257f', 16) or \
			char in [int('30fb', 16), int('25cb', 16), int('2236', 16)] else False

def inOtherSet(char): # Return True
	return True

'''
Please note that extended CJK set C, D, E, and F are not specified here.
'''

def stat(filename, text):
	basicSetD, aSetD, bSetD, puncSetD, symSetD, otherSetD = {}, {}, {}, {}, {}, {}
	numChar = len(text)
	for i, char in enumerate(text):
		if i % 1000000 == 0:
			print "%d / %d chars, \t %.2f %%" % (i, numChar, i * 100.0 / numChar)

		unicodeStr = char.encode("raw_unicode_escape")[2:]
		if unicodeStr == '':		# for characters that don't have unicode strings
			if len(char) > 1 or ord(char) >=  256:		# if it's not an ascii byte, add it to otherSetD
				otherSetD[char] = otherSetD.get(char, 0) + 1
			continue		# if it's an ascii byte, ignore it and continue
		
		funcDicPair = zip([inBasicSet, inASet, inBSet, inPuncSet, inSymbolSet, inOtherSet], \
				[basicSetD, aSetD, bSetD, puncSetD, symSetD, otherSetD])
		for func, dic in funcDicPair:
			if func(int(unicodeStr, 16)):
				break

		dic[char] = dic.get(char, 0) + 1
	
	print
	f = codecs.open(filename + ".stat", 'w', 'utf-8')
	for func, dic in funcDicPair:
		print func.func_name, ': ', sum(dic.values()), ' characters'
		f.write(func.func_name + ': ' + str(sum(dic.values())) + ' characters\n')
	f.write('\n')

	for func, dic in funcDicPair:
		f.write(func.func_name + ': ' + str(sum(dic.values())) + ' characters\n')
		for char in sorted(dic):
			unicodeStr = char.encode("raw_unicode_escape")[2:]
			f.write(unicodeStr + "\t")
			freq = dic[char]
			f.write(char + "\t")
			f.write(str(freq) + "\n")
	f.close()

def cleanSent(filename, text):
	lines = text.split('\n')[:-1]
	result = []
	#pdb.set_trace()
	for i, sent in enumerate(lines):
		if i % 100000 == 0:
			print "%d / %d sents, \t %.2f %%" % (i, len(lines), i * 100.0 / len(lines))

		for char in sent:
			unicodeStr = char.encode("raw_unicode_escape")[2:]
			if unicodeStr == '':
				if len(char) > 1 or ord(char) >= 256:
					break
				else:
					continue

			if any([func(int(unicodeStr, 16)) for func in [inBasicSet, inPuncSet, inSymbolSet]]):
				continue
			else:
				break
		else:
			result.append(sent)
	print '# sentences orignally: ', len(lines)
	print '# sentences after cleaning: ', len(result)

	f = codecs.open(filename + '.clean', 'w', 'utf-8')
	for sent in result:
		f.write(sent + '\n')
	f.close()

def main():
	argParser = argparse.ArgumentParser(description = "Chinese data statistics and cleaning processor")

	argParser.add_argument('-f', '--filename', help="Chinese data file to be processed")
	argParser.add_argument('-m', '--mode', help="processing mode: stat, cleanSent", default="stat")

	args = argParser.parse_args()

	filename = args.filename
	mode = args.mode

	text = codecs.open(filename, 'r', 'utf-8').read()

	if mode == "stat":
		stat(filename, text)
	elif mode == "cleanSent":
		cleanSent(filename, text)

if __name__ == '__main__':
	main()

