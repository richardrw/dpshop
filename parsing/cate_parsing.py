#coding=utf-8

import requests
import random
import pymongo
from lxml import etree
from config import USER_AGENT, PROXY, TIMEOUT


#初始化数据库
client = pymongo.MongoClient('localhost', 27017)
dp = client['dp']
tag1_url = dp['tag1_url']
tag2_url = dp['tag2_url']
addr1_url = dp['addr1_url']
addr2_url = dp['addr2_url']
dpshop = dp['dpshop']


#获取一级菜系
def get_tag1_from(url):
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	r = s.get(url, proxies=proxies, timeout=TIMEOUT)
	tree = etree.HTML(r.text)
	tag1_items = tree.xpath('//div[@id="classfy"]/a')
	for i in tag1_items:
		title = i.getchildren()[0].text
		url = i.attrib['href']
		tag1 = {'title':title, 'url':url}
		tag1_url.insert_one(tag1)
		# print(tag1)


#获取二级菜系
def get_tag2_from(tag1_url):
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	r = s.get(url, proxies=proxies, timeout=TIMEOUT)
	tree = etree.HTML(r.text)
	tag2_items = tree.xpath('//div[@id="classfy-sub"]/a')
	if len(tag2_items) == 0:
		tag2 = {'title':'None', 'url':tag1_url}
		tag2_url.insert_one(tag2)
	else:
		for i in tag2_items:
			title = i.getchildren()[0].text
			url = i.attrib['href']
			tag2 = {'title':title, 'url':url}
			tag2_url.insert_one(tag2)


#获取二级菜系下的一级地址
def get_addr1_from(tag2_url):
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	r = s.get(url, proxies=proxies, timeout=TIMEOUT)
	tree = etree.HTML(r.text)
	addr1_items = tree.xpath('//div[@id="region-nav"]/a')
	for i in addr1_items:
		title = i.getchildren()[0].text
		url = i.attrib['href']
		addr1 = {'title':title, 'url':url}
		addr1_url.insert_one(addr1)


#获取二级菜系下的二级地址
def get_addr2_from(addr1_url):
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	r = s.get(url, proxies=proxies, timeout=TIMEOUT)
	tree = etree.HTML(r.text)
	addr2_items = tree.xpath('//div[@id="region-nav-sub"]/a')
	if len(addr2_items) == 0:
		addr2 = {'title':'None', 'url':addr1_url}
		addr2_url.insert_one(addr2)
	else:
		for i in addr2_items:
			title = i.getchildren()[0].text
			url = i.attrib['href']
			addr2 = {'title':title, 'url':url}
			addr2_url.insert_one(addr2)


if __name__ == '__main__':
	url = 'http://www.dianping.com/search/category/219/10/g0r0'
	get_tag1_from(url)