import subprocess, os

class POSTagger(object):
	# initializes tagger by calling shell script.
	# the first call basically trains the tagger.
	def __init__(self):
		self.p = subprocess.Popen([os.getcwd() + '/runTagger.sh'], 
			stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	# tags the tweet by putting it on stdin and reading 
	# the result off stdout

	# returns a tuple containing as its first element a list of tags 
	# and as its second element a list of tag probabilities
	
	#  !!!!  don't use the same POS tagger with multiple threads. it will create deadlocks !!!!
	def tag(self, tweet):
		self.p.stdin.write(tweet + '\n')
		split_result = self.p.stdout.readline().split('\t')
		if len(split_result) != 4:
			return None
		return (split_result[1].split(), split_result[2].split())

if __name__ == '__main__':
	tagger = POSTagger()
	for i in range(1000):
		print tagger.tag('This is a random tweet!')
		
