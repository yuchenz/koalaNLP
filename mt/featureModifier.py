#!/usr/bin/python2.7

# replace mode:
# given two rule tables (used by hiero mt systems), most rules in the first table is also in the second one, some are not
# find all rules from the first rule table in the second table
# copy their probabilities and counts from the second rule table to replace their probabilities and counts in the first table
# for rules that are not in the second table, keep their original weights
#

# replace-remove mode:
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
	
def replace(toFile, fromFile, remove):
	bigDict = getBigDict(fromFile)

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

def augment(toFile, fromFile):
	bigDict = getBigDict(fromFile)

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

if __name__ == "__main__":
	mode = sys.argv[1]
	if mode == 'replace':
		replace(sys.argv[2], sys.argv[3], False)
	elif mode == 'replace-remove':
		replace(sys.argv[2], sys.argv[3], True)
	elif mode == "augment":
		augment(sys.argv[2], sys.argv[3])
	else:
		print("Error!")
		print("syntax: python featureModifier.py [replace | replace-remove | augment] toFile fromFile")
