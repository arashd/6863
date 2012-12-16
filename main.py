import os
from ngram import *
from common_descriptors import *

def tokenize_file(input, output):
    print 'tokenizing ' + input
    infile = open(input, 'r')
    sentences = []
    tokenizer = Tokenizer()
    for line in infile:
        parts = line.split('\t')
        id = parts[0]
        uid = parts[1]
        text = parts[2].strip()
        sentences.append([id, uid, text])
        tokenizer.feed(text)
    infile.close()
    tokenizer.end_feeding()
    outfile = open(output, 'w')
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence[2], True)
        line = sentence[0] + '\t' + sentence[1]
        for token in tokens:
            line = line + '\t' + token.__str__()
        outfile.write(line + '\n')
    outfile.close()
def tokenize_folder(input, output):
    filenames = os.listdir(input)
    for filename in filenames:
        tokenize_file(input + "/" + filename, output + "/" + filename)

def get_bigram(model, n = 10):
    for i in range(n):
        print model.gen_bigram() 

def eval_file(model, input, output):
    infile = open(input, 'r')
    outfile = open(output, 'w')
    total_prob = 0
    counter = 0
    for line in infile:
        sentence = line.strip().split('\t')
        if len(sentence) == 2:
            continue
        prob = model.prob_bigram(sentence[2:])
        total_prob += prob
        counter +=1
        outfile.write(sentence[0] + '\t' + sentence[1] + '\t' + str(prob) + '\n')
    infile.close()
    outfile.close()
    print input, total_prob/counter
    return total_prob/counter

def eval_folder(model, input, output):
    filenames = os.listdir(input)
    for filename in filenames:
        eval_file(model, input + "/" + filename, output + "/" + filename)

def train_model(filename):
    print 'training model ' + filename
    model = NGram()
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        tokens = line.split('\t')[2:]
        model.train_unigram(tokens)
        model.train_bigram(tokens)
    file.close()
    return model

def eval_models(train, test, output):
    filenames = os.listdir(train)
    for filename in filenames:
        model = train_model(train + '/' + filename)
        os.makedirs(output + '/' + filename)
        eval_folder(model, test,  output + '/' + filename)

def remove_duplicates(data, reference, output):
    filenames = os.listdir(data)
    for filename in filenames:
        data_file = open(data + '/' + filename, 'r')
        reference_file = open(reference + '/' + filename, 'r')
        output_file = open(output + '/' + filename, 'w')
        ids = {}
        for line in reference_file:
            id = line.split('\t')[0]
            ids[id] = True
        for line in data_file:
            id = line.split('\t')[0]
            if id not in ids:
                output_file.write(line)
        reference_file.close()
        data_file.close()
        output_file.close()
 
def merge_tweet(folder, output_folder):
    filenames = os.listdir(folder)
    for filename in filenames:
        tweets = {}
        for filename2 in filenames:
            input = open(folder + '/' + filename2 + '/' + filename, 'r')
            for line in input:
                parts = line.strip().split('\t')
                id = parts[0]
                prob = parts[2][:7]
                if id in tweets:
                    tweets[id].append(prob)
                else:
                    tweets[id] = [parts[1], prob]
            input.close()
        output = open(output_folder + '/' + filename, 'w')
        for filename2 in filenames:
            output.write('\t' + filename2)
        output.write('\n')
        for id in tweets:
            output.write(list_to_string(id, tweets[id]) + '\n')
        output.close()

def list_to_string(id, list):
    output = id
    for element in list:
        output += '\t' + str(element)[:7]
    return output

def merge_user(folder, output_folder):
    filenames = os.listdir(folder)
    for filename in filenames:
        input = open(folder + '/' + filename, 'r')
        users = {}
        next(input)
        for line in input:
            parts = line.strip().split('\t')
            uid = parts[1]
            if uid in users:
                users[uid] = add_probs(users[uid], parts[2:])
            else:
                users[uid] = add_probs(None, parts[2:])
            if uid == '11308402':
                print users[uid]
        output = open(output_folder + '/' + filename, 'w')
        output.write('uid' + '\t' + 'count')
        for filename2 in filenames:
            output.write('\t' + filename2)
        output.write('\n')
        for uid in users:
            probs = [users[uid][0]] + [x / users[uid][0] for x in users[uid][1:]]
            output.write(list_to_string(uid, probs) + '\n')
            
def add_probs(probs, delta):
    if probs == None:
        probs = [1]
        for prob in delta:
            probs.append(float(prob))
    else:
        probs[0] += 1
        for i in range(1, len(probs)):
            probs[i] += float(delta[i-1])
    return probs
        
if __name__ == '__main__':
    #eval_models('dat/tokenized_tweet', 'dat/tokenized_user_tweet_less', 'dat/tweet_model_less')
    #remove_duplicates('dat/tokenized_user_tweet', 'dat/tokenized_tweet', 'dat/tokenized_user_tweet_less')
    #merge_tweet('dat/tweet_model_less', 'dat/tweet_model_less_merged')
    merge_user('dat/tweet_model_less_merged', 'dat/user_classification')