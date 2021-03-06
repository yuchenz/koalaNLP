#!/usr/bin/python2.7

# replace mode:
# given two rule tables (used by hiero mt systems), most rules in the first table is also in the second one, some are not
# find all rules from the first rule table in the second table
# copy their probabilities and counts from the second rule table to replace their probabilities and counts in the first table
# for rules that are not in the second table, keep their original weights
#

# replaceRemove mode:
# basically the same with the replace mode, except that 
# for rules that are not in the second table, remove them from the first table too
#

# augment mode:
# given two rule tables (used by hiero mt systems), most rules in the first table is also in the second one, some are not
#
# for all rules in the first table that are also in the second table, augment their features as follows:
#		source phrase ||| target phrase ||| new_feat new_feat new_feat new_feat 1 old_feat old_feat old_feat old_feat 1 ||| alignment ||| ...
#
# for all rules in the first table that are not in the second table, agument their features as follows:
#		source phrase ||| target phrase ||| 0 0 0 0 0 old_feat old_feat old_feat old_feat 1 ||| alignment ||| ...
# 
# where, new_feat means a feature from the second table, old_feat means a feature from the first table
# the 5th feature means if this rule is in the second table, the last feature means if this rule is in the first table
#


import sys, codecs

def getBigDict(fromFile):
	bigDict = {}
	print "reading in the big rule table ..."
	for line in codecs.open(fromFile, 'r', 'utf-8'):
		line = line.split("|||")
		key = tuple((line[0], line[1], line[3]))
		value = tuple((line[2], "|||".join(line[4:])))
		bigDict[key] = value

	return bigDict
	
def replace(bigDict, toFile, fromFile, remove):
	print "writing out the replaced small rule table ..."
	if remove:
		outF = codecs.open(toFile+'.replaceRemoved', 'w', 'utf-8')
	else:
		outF = codecs.open(toFile+'.replaced', 'w', 'utf-8')

	for line in codecs.open(toFile, 'r', 'utf-8'):
		line = line.split("|||")
		key = tuple((line[0], line[1], line[3]))
		if key not in bigDict:
			if remove: 
				continue
			else:
				outF.write(key[0] + '|||' + key[1] + '|||')
				outF.write(line[2] + "|||" + key[2] + "|||" + "|||".join(line[4:]))
		else:
			outF.write(key[0] + '|||' + key[1] + '|||')
			value = bigDict[key]
			outF.write(value[0] + "|||" + key[2] + "|||" + value[1])
	
	outF.close()

def augment(bigDict, toFile, fromFile):
	print("writing out the augmented small rule table ...")
	outF = codecs.open(toFile+'.augmented', 'w', 'utf-8')
	for line in codecs.open(toFile, 'r', 'utf-8'):
		line = line.split("|||")
		key = tuple((line[0], line[1], line[3]))
		outF.write(key[0] + "|||" + key[1] + "|||")
		if key not in bigDict:
			outF.write(" 0 0 0 0 0" + line[2] + "1 |||" + key[2] + "|||" + "|||".join(line[4:]))
		else:
			value = bigDict[key]
			outF.write(value[0] + "1" + line[2] + "1 |||" + key[2] + "|||" + value[1])
	
	outF.close()

def stat(bigDict, toFile, fromFile):
	print("stat ...")
	notInBigD, inBigD, nontermRule1, termRule1, nontermRule2, termRule2 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
	for line in codecs.open(toFile, 'r', 'utf-8'):
		line = line.split('|||')
		key = tuple((line[0], line[1], line[3]))
		if key not in bigDict:
			notInBigD += 1
			if '[X][X]' in line[0]:
				nontermRule1 += 1
			else:
				termRule1 += 1
		else:
			inBigD += 1
			if '[X][X]' in line[0]:
				nontermRule2 += 1
			else:
				termRule2 += 1
	
	total = notInBigD + inBigD
	print("total rules in %s: %d\n" % (toFile, int(total)))

	print("%.2f %% phrase pair rules" % ((termRule1 + termRule2) * 100.0 / total))
	print("%.2f %% rules with nonterminals\n" % ((nontermRule1 + nontermRule2) * 100.0 / total))

	print("%.2f %% not in %s" % (notInBigD * 100.0 / total, fromFile))
	print("\tamong which %.2f %% is phrase pair rules" % (termRule1 * 100.0 / notInBigD))
	print("\tamong which %.2f %% is rules with nonterminals\n" % (nontermRule1 * 100.0 / notInBigD))
	print("%.2f %% in %s" % (inBigD * 100.0 / total, fromFile))
	print("\tamong which %.2f %% is phrase pair rules" % (termRule2 * 100.0 / inBigD))
	print("\tamong which %.2f %% is rules with nonterminals\n" % (nontermRule2 * 100.0 / inBigD))

if __name__ == "__main__":
	mode = sys.argv[1].split('-')
	print("mode is: ", ' '.join(mode))
	if 'replace' not in mode and 'replaceRemove' not in mode and 'augment' not in mode and 'stat' not in mode:
		print("Error!")
		print("syntax: python featureModifier.py [stat-replace-replaceRemove-augment] toFile fromFile")
	else:
		bigDict = getBigDict(sys.argv[3])
		if 'stat' in mode:
			stat(bigDict, sys.argv[2], sys.argv[3])
		if 'replace' in mode:
			replace(bigDict, sys.argv[2], sys.argv[3], False)
		if 'replaceRemove' in mode:
			replace(bigDict, sys.argv[2], sys.argv[3], True)
		if "augment" in mode:
			augment(bigDict, sys.argv[2], sys.argv[3])
