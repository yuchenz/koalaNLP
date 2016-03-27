'''
Created on Feb 13, 2014

@author: yuchenz
'''
import nltk

class Evaluator(object):
    '''
    classdocs
    '''

    def __init__(self, gold, auto, feats):
        '''
        gold, auto -- lists of tags
        '''
        if len(gold) != len(auto):
            print "numbers of instances don't match!!!"
            exit(1)
            
        self.gold = gold
        self.auto = auto
        self.feats = feats
        
    def evaluate(self):
        # compute accuracy
        correct = 0
        total = 0
        
        for i, tag in enumerate(self.gold):
            if tag == self.auto[i]:
                correct +=1
            else:
                #print self.feats[i], "auto ==", self.auto[i]
                #print
				pass
            total +=1
        
        print "instances --"
        print "total: ", total
        print "correct: ", correct
        accuracy = float(correct) / total
        print "accuracy: ", accuracy
        
        # compute precision, recall, and f-score for each category
        categories = set(self.gold + self.auto)
        for cat in categories:
            print "category ", cat
            p = self.precision(cat, zip(self.gold, self.auto))
            r = self.recall(cat, zip(self.gold, self.auto))
            if p + r == 0.0:
                f = 0.0
            else:
                f = 2.0 * p * r / (p + r)
            
            print "p == ", p, "r == ", r, "f == ", f
        
        # generate confusion matrix
        print nltk.ConfusionMatrix(self.gold, self.auto)
        return correct, total
            
    def precision(self, cat, tags):
        assigned = 0
        hit = 0
        for t in tags:
            if t[1] == cat:
                assigned += 1
                if t[0] == cat:
                    hit += 1
        if assigned == 0:
            return 0.0
        return 1.0 * hit / assigned
            
    def recall(self, cat, tags):
        gold = 0
        hit = 0
        for t in tags:
            if t[0] == cat:
                gold += 1
                if t[1] == cat:
                    hit += 1   
        if gold == 0:
            return 0.0  
        return 1.0 * hit / gold

