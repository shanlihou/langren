import urllib2
def getUrl(url):
	resp = urllib2.urlopen(url)
	return resp.read()
print getUrl('http://192.168.0.189:8000/control?isNeedClose=1')	