#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys, urllib2
from HTMLParser import HTMLParser
import xml.etree.ElementTree as ET
import re

urlHeader = "https://ja.wikipedia.org/w/api.php"
param = "?action=query&list=categorymembers&format=xml&cmtype=page&cmlimit=500&cmtitle=Category:"
title = "年のテレビアニメ"
year = "2015"

pageGetParam = "?action=query&prop=info&inprop=url&format=xml&pageids="

##################

# 欲しい年を引数に設定してやらないと動かない
if 2 < len(sys.argv) :
	raise Exception("The number of argument must be 0 or 1.")
elif len(sys.argv) == 2:
	year = sys.argv[1]
	url = urlHeader + param + year + title

##################

class urlOpen:
	opener = urllib2.build_opener()

	def __init__(self):
		self.opener.addheaders = [('User-Agent', 'getAnimeTitlesBot/1.1 (https://github.com/toko-m/getAnimeTitles; tokom@ult.sakura.ne.jp)')]
		urllib2.install_opener(self.opener)

	def open(self, url):
		response = urllib2.urlopen(url)
		if response is None:
			raise Exception("No response.")
		return response.read()

##################

# カテゴリページのリンク引っこ抜き
urlOpener = urlOpen()
titleRoot = ET.fromstring(urlOpener.open(url))

pageIds = ""
pageUrls = {}
idLists = []

# ページのURLを取得する準備
# 登録済みbotじゃないと50件までしか取得できないっぽいので50件ずつ
count = 1
cmAll = titleRoot.findall('./query/categorymembers/cm');
for cm in cmAll:
	pageIds =  cm.get('pageid') + "|" + pageIds
	if count % 50 == 0 or count == len(cmAll):
		idLists.append(pageIds)
		pageIds = ""
	count += 1

# 個別ページのURL取得 → 辞書に保存
for idList in idLists:
	getPageUrl = urlHeader + pageGetParam + idList
	pageRoot = ET.fromstring(urlOpener.open(getPageUrl))
	for page in pageRoot.findall('./query/pages/page'):
		pageUrls[page.get('pageid')] = page.get('fullurl')

# タイトルとページのURLを出力
for cm in titleRoot.findall('./query/categorymembers/cm'):
	print cm.get('title')+"\t"+pageUrls[cm.get('pageid')]
