import requests

if __name__ == '__main__':
	r = requests.get('http://t.co/uLW33ZDl')
	print r.headers
