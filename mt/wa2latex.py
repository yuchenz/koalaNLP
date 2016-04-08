#!/usr/bin/python2.7

"""
Yuchen Zhang
03/19/2015
"""

from wa2latex_helper import *
import sys
import codecs
import operator

class Analyzer:
	def __init__(self, gold_wa_f, auto_wa_f, en_f, ch_f):
		self.gold_wa = [[(item.split('-')[0],item.split('-')[1]) for item in line.split()] for line in open(gold_wa_f).readlines()]
		self.auto_wa = [[(item.split('-')[0],item.split('-')[1]) for item in line.split()] for line in open(auto_wa_f).readlines()]
		self.en = [line.split() for line in codecs.open(en_f, 'r', 'utf-8').readlines()]
		self.ch = [line.split() for line in codecs.open(ch_f, 'r', 'utf-8').readlines()]

		assert(len(self.gold_wa) == len(self.auto_wa))
		assert(len(self.en) == len(self.ch))
		assert(len(self.en) == len(self.gold_wa))

	def visualize(self, outputFile):
		"""
		output a latex file
		"""
		outf = codecs.open(outputFile, 'w', 'utf-8')
		outf.write(latex_pre)

		k = 0
		max_clen = 0
		max_elen = 0
		for i in xrange(len(self.gold_wa)):
			gwa = set(self.gold_wa[i])
			awa = set(self.auto_wa[i])
			esent = self.en[i]
			csent = self.ch[i]

			outf.write("Sent \#%d: ch sent len: %d, en sent len: %d\n" % (k, len(csent), len(esent)))
			k += 1
			max_clen = max(max_clen, len(csent))
			max_elen = max(max_elen, len(esent))
			#print k, csent

			# set matrix scale
			scale = min(0.5, 17.0/len(esent))
			outf.write("\\renewcommand\myscale{%.5f}\n" % scale)
			# set english sent len
			outf.write("\\renewcommand\enwordnum{%d}\n" % len(esent))
			# set chinese sent len
			outf.write("\\renewcommand\chwordnum{%d}\n" % len(csent))
			# set chinese sent wordids and words
			tmp = ""
			for j, w in enumerate(csent):
				tmp += str(j)+"/{"+w+"}, "     
			outf.write("\\renewcommand\chidwords{"+tmp[:-2]+"}\n")
			# set english sent wordids and words
			tmp = ""
			for j, w in enumerate(esent):
				tmp += str(j)+"/{"+w+"}, "    
			outf.write("\\renewcommand\enidwords{"+tmp[:-2]+"}\n")

			# set correct, missed, and extra word alignments
			correctwa = gwa.intersection(awa)
			missedwa = gwa - correctwa
			extrawa = awa - correctwa
			tmp = ""
			for wa in correctwa:
				tmp += str(wa[0])+"/"+str(wa[1])+", "
			outf.write("\\renewcommand\correctwa{"+tmp[:-2]+"}\n")
			tmp = ""
			for wa in missedwa:
				tmp += str(wa[0])+"/"+str(wa[1])+", "
			outf.write("\\renewcommand\missedwa{"+tmp[:-2]+"}\n")
			tmp = ""
			for wa in extrawa:
				tmp += str(wa[0])+"/"+str(wa[1])+", "
			outf.write("\\renewcommand\extrawa{"+tmp[:-2]+"}\n")

			outf.write(latex_draw_matrix+"\n\n\clearpage\n\n")

		outf.write(latex_post)
		outf.close()

		print "max clen: ", max_clen, "max elen: ", max_elen

	def statistics(self):
		missedwa = {} 
		extrawa = {}
		correctwa = {}
		for i in xrange(len(self.gold_wa)):
			gwa = set(self.gold_wa[i])
			awa = set(self.auto_wa[i])
			esent = self.en[i]
			csent = self.ch[i]

			cwa = gwa.intersection(awa) 
			for wa in gwa - cwa:
				word_pair = (esent[int(wa[0])], csent[int(wa[1])])
				missedwa[word_pair] = missedwa.get(word_pair, 0) + 1
			for wa in awa - cwa:
				word_pair = (esent[int(wa[0])], csent[int(wa[1])])
				extrawa[word_pair] = extrawa.get(word_pair, 0) + 1
			for wa in cwa:
				word_pair = (esent[int(wa[0])], csent[int(wa[1])])
				correctwa[word_pair] = correctwa.get(word_pair, 0) + 1

		print "\nmissed word alignments:"
		for item in sorted(missedwa.items(), key=operator.itemgetter(1), reverse=True):
			if item[1] == 1:
				break
			print item[0][0], item[0][1], item[1] 
		print "\nextra word alignments:"
		for item in sorted(extrawa.items(), key=operator.itemgetter(1), reverse=True):
			if item[1] == 1:
				break
			print item[0][0], item[0][1], item[1]
		print "\ncorrect word alignments:"
		for item in sorted(correctwa.items(), key=operator.itemgetter(1), reverse=True):
			if item[1] == 1:
				break
			print item[0][0], item[0][1], item[1]



if __name__ == "__main__":
	gold_wa_f = sys.argv[1]    # gold word alignment file, format: 0-0 1-1 2-3 (i.e. word id in language 1 - word id in language 2)
	auto_wa_f = sys.argv[2]
	en_f = sys.argv[3]			# language 1 sentence file
	ch_f = sys.argv[4]			# language 2 sentence file
	outputTexFile = sys.argv[5]

	analyzer = Analyzer(gold_wa_f, auto_wa_f, en_f, ch_f)
	analyzer.visualize(outputTexFile)
	analyzer.statistics()


