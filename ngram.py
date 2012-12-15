'''
Class to generate n-gram models from tokens and calculate n-gram probs

Created on Dec 13, 2012

@author: lulu
'''

from collections import defaultdict
import math
import random

class NGram:
    
    def __init__(self):
        self.unicount = defaultdict(float) # unigram counts
        self.total_unicount = 0 # total unigram counts
        self.bicount = defaultdict(float) # bigram counts
        self.ids = {}
    #######################################################
    #     Train(update) unigram model with an input       #
    #     tokenized sentence(a list)                      #
    #######################################################
    def train_unigram(self, sent, id = None):
        if id != None:
            ids[id] = True
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
        return math.log(prob)
    
    #######################################################
    #     Calculate bigram probability of a sentence      #
    #     using the current bigram model                  #
    #######################################################
    def prob_bigram(self, sent, id = None):
        if id != None and ids[id]:
            return None
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
        return math.log(prob)

    #######################################################
    #     Genrate random sentence using                   #
    #     the current unigram model                       #
    #######################################################
    def gen_unigram(self):
        sent = []
        while True:
            pos = random.random() * self.total_unicount
            cur_pos = 0
            for word in self.unicount:
                cur_pos += self.unicount[word]
                if cur_pos > pos: # find the word
                    if word == '*end*':
                        return sent
                    elif word != '*start*':
                        sent.append(word)
                    break
                    
    #######################################################
    #     Genrate random sentence using                   #
    #     the current unigram model                       #
    #######################################################
    def gen_bigram(self):
        sent = []
        cur_word = '*start*'
        while True:
            num_of_bigram = self.unicount[cur_word]
            pos = random.random() * num_of_bigram
            cur_pos = 0
            for bi in self.bicount:
                first = bi.split()[0]
                second = bi.split()[1]
                if first == cur_word:
                    cur_pos += self.bicount[bi]
                    if cur_pos > pos:
                        if second == '*end*':
                            return sent
                        else:
                            sent.append(second)
                            cur_word = second
                        break
                
#if __name__ == "__main__":
#    model = NGram()
#    sent1 = ['John', 'read', 'a', 'book']
#    sent2 = ['Mary', 'read', 'a', 'different', 'book']
#    model.train_unigram(sent1)
#    model.train_unigram(sent2)
#    model.train_bigram(sent1)
#    model.train_bigram(sent2)
#    sent = model.gen_bigram()
#    print sent
