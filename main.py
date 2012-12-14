from ngram import *
from common_descriptors import *
    
if __name__ == '__main__':
    f=open('dat/tweet/artist', 'r')
    sentences = []
    prefixes = []
    tokenizer = Tokenizer()
    for line in f:
        text = line.split("\t")[2].strip()
        sentences.append(text)
        tokenizer.feed(text)
    tokenizer.end_feeding()
    print len(sentences)
    ngram = NGram()
    for sentence in sentences[0:1000]:
        tokens = tokenizer.tokenize(sentence, True)
        print tokens
        ngram.train_bigram(tokens)
    
    
    
    