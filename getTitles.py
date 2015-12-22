#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys, urllib2
from HTMLParser import HTMLParser
import xml.etree.ElementTree as ET
import re

urlHeader = "https://ja.wikipedia.org/w/api.php"
param = "?action=query&list=categorymembers&format=xml&cmtype=page&cmlimit=500&cmtitle=Category:"
title = "年のテレビアニメ"

# 欲しい年を引数に設定してやらないと動かないよ
if 2 < len(sys.argv) :
	raise Exception("The number of argument must be 0 or 1.")
elif len(sys.argv) == 2:
	year = sys.argv[1]
	url = urlHeader + param + year + title

# urlopener用意
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'liteCrawler')]
urllib2.install_opener(opener)

# XML取得
response = urllib2.urlopen(url)
if response is None:
	raise Exception("No response.")
result = response.read()

root = ET.fromstring(result)

# タイトルとwikipediaのページを返してやりたい
for cm in root.findall('./query/categorymembers/cm'):
	response
	print cm.get('title')+"\t"+cm.get('pageid')
