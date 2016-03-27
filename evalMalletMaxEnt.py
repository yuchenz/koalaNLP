'''
Created on Nov 26, 2013

@author: yuchenz
'''

import codecs, sys
from Evaluator import Evaluator

def chooseMax(lis):
	tags = [lis[i] for i in range(0, len(lis)-1, 2)]
	values = [float(lis[i+1]) for i in range(0, len(lis)-1, 2)]
	maxv = max(values)
	return tags[values.index(maxv)]

def evaluate(goldfile, autofile, joint, model):
    print "goldfile -- ", goldfile
    print "autofile -- ", autofile
    f = codecs.open(goldfile, "r", "utf-8")
    gold = f.readlines()
    f.close()
    f = codecs.open(autofile, "r", "utf-8")
    auto = f.readlines()
    f.close()

    if model == "maxent":
        goldTags = [item.split()[1] for item in gold if item.split() != []]
        autoTags = [chooseMax(item.split()[1:]) for item in auto if item.split() != []]
        idTags = [item.split()[0] for item in auto if item.split() != []]
        print "koala !!! len of gold tags --", len(goldTags), "len of auto tags --", len(autoTags)
    elif model == "crfpp":
        pass
    elif model == "crfsuite":
        pass
    
    if joint == "joint":
        print "\nfirst tag in joint tags --"
        evaluator = Evaluator([tag.split("_")[0] for tag in goldTags], [tag.split("_")[0] for tag in autoTags], gold)
        correct, total = evaluator.evaluate()
        print "\nsecond tag in joint tags --"
        evaluator = Evaluator([tag.split("_")[1] for tag in goldTags], [tag.split("_")[1] for tag in autoTags], gold)
        correct, total = evaluator.evaluate()
    else:
        evaluator = Evaluator(goldTags, autoTags, gold)
        correct, total = evaluator.evaluate()
    return correct, total, zip(idTags, autoTags)
   

if __name__ == "__main__":
	if len(sys.argv) > 3:
		evaluate(sys.argv[1], sys.argv[2], sys.argv[3], "maxent")
	else:
		evaluate(sys.argv[1], sys.argv[2], "no", "maxent")
