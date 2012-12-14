'''
Class to generate n-gram models from tokens and calculate n-gram probs

Created on Dec 13, 2012

@author: lulu
'''

from collections import defaultdict

class NGram:
    
    def __init__(self):
        self.unicount = defaultdict(float) # unigram counts
        self.total_unicount = 0 # total unigram counts
        self.bicount = defaultdict(float) # bigram counts
        
    #######################################################
    #     Train(update) unigram model with an input       #
    #     tokenized sentence(a list)                      #
    #######################################################
    def train_unigram(self, sent):
        sent.insert(0, '*start*')
        sent.append('*end*')
        for token in sent:
            self.unicount[token.__str__()] += 1
            self.total_unicount += 1
    
    #######################################################
    #     Train(update) bigram model with an input        #
    #     tokenized sentence(a list)                      #
    #######################################################
    def train_bigram(self, sent):
        sent.insert(0,'*start*')
        sent.append('*end*')
        total_token = len(sent)
        for i in range(total_token - 1):
            cur_bigram = sent[i].__str__() + ' ' + sent[i+1].__str__()
            self.bicount[cur_bigram] += 1
            
    
    #######################################################
    #     Calculate unigram probability of a sentence     #
    #     using the current unigram model                 #
    #######################################################
    def prob_unigram(self, sent):
        sent.insert(0,'*start*')
        sent.append('*end*')
        prob = 1.0
        for token in sent:
            token = token.__str__()
            # add-one smoothing
            if token in self.unicount:
                count = self.unicount[token]
            else:
                count = 0
            cur_unicount = (count + 1) * self.total_unicount / (self.total_unicount + len(self.unicount))
            prob *= (cur_unicount / self.total_unicount)
        return prob
    
    #######################################################
    #     Calculate bigram probability of a sentence      #
    #     using the current bigram model                  #
    #######################################################
    def prob_bigram(self, sent):
        sent.insert(0,'*start*')
        sent.append('*end*')
        prob = 1.0
        total_token = len(sent)
        for i in range(total_token - 1):
            # Laplace smoothing
            if sent[i].__str__() in self.unicount:
                count = self.unicount[sent[i]]
            else:
                count = 0
            cur_unicount = count + len(self.unicount)
            cur_bigram = sent[i].__str__()+' '+sent[i+1].__str__()
            cur_bicount = self.bicount[cur_bigram] + 1
            prob *= (cur_bicount / cur_unicount)
        return prob