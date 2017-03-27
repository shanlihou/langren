#!/usr/bin/python
import urllib2
import time
import os
def getUrl(url):
	resp = urllib2.urlopen(url)
	return resp.read()
def main():
	while(1):
		time.sleep(5)
		getUrl('http://60.205.206.18:80/control?pcOpen=1')
		status = getUrl('http://60.205.206.18:80/control?isNeedClose=1')
		print 'status:' + status
		if status == '0':
			getUrl('http://60.205.206.18:80/control?pcClose=1')
			os.system('shutdown -s -t 300')
			time.sleep(305)
main()