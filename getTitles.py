#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys, urllib2
from HTMLParser import HTMLParser
import re

titles = {}

class parser(HTMLParser):
	startTitles = False
	skip = False
	tagStack = []
	tmpTitle = ""
	tmpUrl = ""

	ptnAlphabet = re.compile("[A-z]|¥*")

	def __init__(self):
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		self.tagStack.append(tag)

		if "div" == tag and ("class", "printfooter") in attrs :
			self.startTitles = False

		if self.startTitles and not self.skip and "a" == tag :
			for attr in attrs :
				if attr[0] == "href" :
					self.tmpUrl = attr[1]

	def handle_endtag(self, tag):
		if "li" == tag and self.tmpTitle != "":
			titles[self.tmpTitle] = self.tmpUrl
			self.tmpTitle = ""
			self.tmpUrl = ""

		self.tagStack.pop()

	def handle_data(self, data):
		if not self.tagStack :
			return

		if "h2" in self.tagStack :
			if "あるページ".decode("utf-8") in data :
				self.startTitles = True
			else :
				self.startTitles = False
		elif "h3" in self.tagStack :
			if re.match(self.ptnAlphabet, data) :
				self.skip = True
			else :
				self.skip = False

		if self.startTitles and not self.skip :
			liNum = self.tagStack.count("li")
			if liNum == 0 :
				return
			self.tmpTitle += data

urlHeader = "http://ja.wikipedia.org/wiki/Category:"
urlFooter = "年のテレビアニメ"
url = "http://localhost/test/costumeData/test.html"
year = "2014"

if 2 < len(sys.argv) :
	raise Exception("The number of argument must be 0 or 1.")
elif len(sys.argv) == 2:
	year = sys.argv[1]
	url = urlHeader + year + urlFooter

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'liteCrawler')]
urllib2.install_opener(opener)

response = urllib2.urlopen(url)

if response is None:
	raise Exception("No response.")

parser = parser()
parser.feed(response.read().decode("utf-8"))
parser.close()

for title in titles :
	pStr =  year + ", " +  title.encode("utf-8") + ", http://ja.wikipedia.org" + titles[title].encode("utf-8")
	print pStr