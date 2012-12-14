import sys
import MySQLdb
import collections
#import requests
import string
import random
import operator

HOST = 'twitwi.mit.edu'
USERNAME = '6863'
PASSWORD = '!trendistic'
DBNAME = 'twitwi'
PORT = 3306

HASHTAG_COUNT = 1000
MENTION_COUNT = 1000
WORD_COUNT    = 10000

SPECIAL_ID = 224371352676573184
RANDOMIZER = 120000000000000

def make_query(num_tweets):
	return "SELECT * FROM twitwi.primary_tweet where id > " + str(random.randint(SPECIAL_ID, SPECIAL_ID + RANDOMIZER)) + " limit " + str(num_tweets) + ";"



class Tokenizer(object):
	
	def __init__(self):
		self.resolver = Resolver()
		self.mention_hist = Histogram(Mention, MENTION_COUNT)	
		self.hashtag_hist = Histogram(Hashtag, HASHTAG_COUNT)
		self.word_hist = Histogram(str, WORD_COUNT)

	def feed(self, tweet):
		tokenized = self.tokenize(tweet, False)
		for token in tokenized['tokens']:
			if token.__class__ == Mention:
				self.mention_hist.add_element(token)
			elif token.__class__ == Hashtag:
				self.hashtag_hist.add_element(token)
			elif token.__class__ == str:
				self.word_hist.add_element(token)
	
	def end_feeding(self):
		for hist in [self.mention_hist, self.hashtag_hist, self.word_hist]:
			sorted_keys = [item[0] for item in sorted(hist.d.iteritems(), key=operator.itemgetter(1), reverse = True)[:hist.max_count]]
			for key in hist.d.keys():
				if key not in sorted_keys:
					del hist.d[key]
			#print sorted_keys[:10]
			print 'feeding ended... '

	def tokenize(self, tweet, check_hists):
		tokenized_tweet = {}

		tokens = []
		entities = tweet.split()
		for entity in entities:
			if entity.startswith('@'):
				mention = Mention(entity[1:])
				if (not check_hists) or self.mention_hist.qualifies(mention):
					tokens.append(mention)
				else:
					tokens.append(RareMention(entity[1:]))
			elif entity.startswith('#'):
				hashtag = Hashtag(entity[1:])
				if (not check_hists) or self.hashtag_hist.qualifies(hashtag):
					tokens.append(hashtag)
				else:
					tokens.append(RareHashtag(entity[1:]))
			elif entity.startswith('http://t.co'):
				domain = Domain(entity) 
				tokens.append(domain)
			elif entity == 'RT':
				tokens.append(Retweet())
			else:
				# get rid of punctuation at end and start
				entity = self.strip_affixes(entity)
				# makes everything lowercase
				entity = entity.lower()

				# strips punctuation from both ends
				entity = entity.strip(string.punctuation)
			
				entity = entity.translate(None, string.punctuation)
				if (not check_hists) or self.word_hist.qualifies(entity):
					tokens.append(entity)
				else:
					tokens.append(RareWord(entity))

		tokenized_tweet['tokens'] = tokens
		return tokenized_tweet

	def strip_affixes(self, entity):
		stripped = entity[-2:]

		if stripped in ['\'s', '\'d', '\'ll']:
			entity = stripped
			
		stripped = entity[-3:]

		if stripped in ['\'ll', '\'re']:
			entity = stripped
		
		return entity

		
class Histogram(object):
	def __init__(self, element_class, max_count):
		self.d = {}
		self.element_class = element_class
		self.max_count = max_count

	def add_element(self, element):
		if not element.__class__ == self.element_class:
			raise RuntimeException("wrong type added to histogram")
		if not (element in self.d):
			self.d[element] = 0
		self.d[element]+=1
	
	def qualifies(self, element):
		return (element in self.d)


class Retweet(object):
	def __init__(self):
		pass
	def __repr__(self):
		return '<RT>'

class Mention(object):
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return '<MENTION: ' + '@' + self.name + '>'

class Hashtag(object):
	def __init__(self, s):
		self.s = s
	def __repr__(self):
		return '<HASHTAG: ' + '#' + self.s + '>'

class Domain(object):
	def __init__(self, domain):
		self.domain = domain
	def __repr__(self):
		return '<DOMAIN: ' + self.domain + '>'



class RareWord(object):
	def __init__(self, word):
		self.word = word
	def __repr__(self):
		return '<RARE WORD: ' + self.word + '>'


class RareMention(Mention):
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return '<RARE MENTION ' + '@' + self.name + '>'

class RareHashtag(Hashtag):
	def __init__(self, s):
		self.s = s
	def __repr__(self):
		return '<RARE HASHTAG ' + '#' + self.s + '>'


#class Resolver(object):
#	def __init__(self):
#		pass
#
#	def resolve(self, url):
#		try:
#			r = requests.get(url)
#			if 'domain' in r.headers:
#				return r.headers['domain']
#		except:
#			return None
#		return None

class Twiterator(collections.Iterator):
	cursor = None

	def __init__(self, cursor, query):
		super(Twiterator, self).__init__()
		self.cursor = cursor
		self.cursor.execute(query)

	def next(self):
		row = self.cursor.fetchone()
		if row:
			d = {}
			d['id'] = row[0]
			d['text'] = row[1]
			d['user_id'] = row[2]
			d['created_at'] = row[3]
			return d
		else:
			raise StopIteration


if __name__ == '__main__':
	cursor = None

	import time
	try:
		connection = MySQLdb.connect(host = HOST, user = USERNAME, 
				passwd = PASSWORD, db = DBNAME, port = PORT)
		cursor = connection.cursor()
	except:
		print 'Server not responding...'
		sys.exit(0)
	
	t = time.time()
	
	twiterator = Twiterator(cursor, make_query(20000))
	tokenizer = Tokenizer()	

	for tweet in twiterator:
		tokenizer.feed(tweet['text'])
	tokenizer.end_feeding()
	
	print len(tokenizer.mention_hist.d.keys())

	t = time.time()

	twiterator = Twiterator(cursor, make_query(20000))

	for tweet in twiterator:
		tokens = tokenizer.tokenize(tweet['text'], True)
		print tweet['text']
		print tokens		

#	for tweet in twiterator:
#		for token in tokenizer.tokenize(tweet['text'])['tokens']:
#			print token

	print time.time() - t

