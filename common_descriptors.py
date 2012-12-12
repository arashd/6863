import sys
import MySQLdb
import collections
import requests

HOST = 'twitwi.mit.edu'
USERNAME = '6863'
PASSWORD = '!trendistic'
DBNAME = 'twitwi'
PORT = 3306

QUERY = """SELECT * FROM twitwi.primary_tweet where id > 164371352676573184 limit 1000;"""

class Tokenizer(object):
	
	def __init__(self):
		self.resolver = Resolver()

	def tokenize(self, tweet):
		tokenized_tweet = {}
		tokenized_tweet['retweet'] = False

		tokens = []
		entities = tweet.split()
		for entity in entities:
			if entity.startswith('@'):
				tokens.append(Mention(entity[1:]))
			elif entity.startswith('#'):
				tokens.append(Hashtag(entity[1:]))
			elif entity.startswith('http://t.co'):
				#domain = self.resolver.resolve(entity)
				domain = entity
				if domain:
					tokens.append(Domain(domain))
			elif entity == 'RT':
				tokens.append(Retweet())
				tokenized_tweet['retweet'] = True
			else:
				tokens.append(entity)
		tokenized_tweet['tokens'] = tokens
		return tokenized_tweet

class Retweet(object):
	def __init__(self):
		pass
	def __repr__(self):
		return '<RT>'

class Mention(object):
	def __init__(self, s):
		self.s = s
	def __repr__(self):
		return '<MENTION: ' + '@' + self.s + '>'

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

class Resolver(object):
	def __init__(self):
		pass

	def resolve(self, url):
		try:
			r = requests.get(url)
			if 'domain' in r.headers:
				return r.headers['domain']
		except:
			return None
		return None

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

	try:
		connection = MySQLdb.connect(host = HOST, user = USERNAME, 
				passwd = PASSWORD, db = DBNAME, port = PORT)
		cursor = connection.cursor()
	except:
		print 'Server not responding...'
		sys.exit(0)
	
	twiterator = Twiterator(cursor, QUERY)
	tokenizer = Tokenizer()
	
	domain_count = 0
	for tweet in twiterator:
		for token in tokenizer.tokenize(tweet['text'])['tokens']:
			print token





