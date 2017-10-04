#coding=utf-8

import requests
import random
import pymongo
import time
from lxml import etree
from config import USER_AGENT, PROXY, TIMEOUT, LINKTIME


#初始化数据库
client = pymongo.MongoClient('localhost', 27017)
dp = client['dp']
tag1_url = dp['tag1_url']							#存储从start_url中成功爬取到的tag1_url
tag2_url = dp['tag2_url']							#存储从tag1_url中成功爬取到的tag2_url
crawly_tag1_url_bad = dp['crawly_tag1_url_bad']			#存储爬取失败的tag1_url
addr1_url = dp['addr1_url']							#存储从tag2_url中成功爬取到的addr1_url
crawly_tag2_url_bad = dp['crawly_tag2_url_bad']			#存储爬取失败的tag2_url
addr2_url = dp['addr2_url']							#存储从addr1_url中成功爬取到的addr2_url
crawly_addr1_url_bad = dp['crawly_addr1_url_bad']		#存储爬取失败的addr1_url
dpshop = dp['dpshop']								#存储从addr2中成功爬取到的dpshop_msg
crawly_addr2_url_bad = dp['crawly_addr2_url_bad']		#存储爬取失败的addr2_url


# global LINKTIME


#获取一级菜系
def get_tag1_from(start_url):
	global LINKTIME
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	try:
		r = s.get(start_url, proxies=proxies, timeout=TIMEOUT)
		tree = etree.HTML(r.text)
		tag1_items = tree.xpath('//div[@id="classfy"]/a')
		for i in tag1_items:
			title = i.getchildren()[0].text
			url = i.attrib['href']
			tag1 = {'title':title, 'url':url, 'status':'ok'}
			tag1_url.insert_one(tag1)
			# print(tag1)
		LINKTIME = 3    #重置LINKTIME
		time.sleep(1)
	except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		if LINKTIME > 0:
			print('爬取失败，现在重新链接')
			get_tag1_from(start_url)
			LINKTIME -= 1
		else:
			print('{}爬取失败'.format(start_url))


#获取二级菜系
def get_tag2_from(tag1_url):
	global LINKTIME
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	try:
		r = s.get(tag1_url, proxies=proxies, timeout=TIMEOUT)
		tree = etree.HTML(r.text)
		tag2_items = tree.xpath('//div[@id="classfy-sub"]/a')
		if len(tag2_items) == 0:
			tag2 = {'title':'None', 'url':tag1_url, 'status':'tag1_not_sub'}
			tag2_url.insert_one(tag2)
		else:
			for i in tag2_items:
				title = i.getchildren()[0].text
				url = i.attrib['href']
				tag2 = {'title':title, 'url':url, 'status':'ok'}
				tag2_url.insert_one(tag2)
		LINKTIME = 3    #重置LINKTIME
		time.sleep(1)
	except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		if LINKTIME > 0:
			print('爬取失败，现在重新链接')
			get_tag2_from(tag1_url)
			LINKTIME -= 1
		else:
			tag1_bad = {'url':tag1_url, 'status':'bad'}
			crawly_tag1_url_bad.insert_one(tag1_bad)
			print('{}爬取失败'.format(tag1_url))


#获取二级菜系下的一级地址
def get_addr1_from(tag2_url):
	global LINKTIME
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	try:
		r = s.get(tag2_url, proxies=proxies, timeout=TIMEOUT)
		tree = etree.HTML(r.text)
		addr1_items = tree.xpath('//div[@id="region-nav"]/a')
		for i in addr1_items:
			title = i.getchildren()[0].text
			url = i.attrib['href']
			addr1 = {'title':title, 'url':url}
			addr1_url.insert_one(addr1)
		LINKTIME = 3    #重置LINKTIME
		time.sleep(1)
	except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		if LINKTIME > 0:
			print('爬取失败，现在重新链接')
			get_addr1_from(tag2_url)
			LINKTIME -= 1
		else:
			tag2_bad = {'url':tag2_url, 'status':'bad'}
			crawly_tag2_url_bad.insert_one(tag2_bad)
			print('{}爬取失败'.format(tag2_url))


#获取二级菜系下的二级地址
def get_addr2_from(addr1_url):
	global LINKTIME
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	try:
		r = s.get(addr1_url, proxies=proxies, timeout=TIMEOUT)
		tree = etree.HTML(r.text)
		addr2_items = tree.xpath('//div[@id="region-nav-sub"]/a')
		if len(addr2_items) == 0:
			addr2 = {'title':'None', 'url':addr1_url, 'status':'addr1_not_sub'}
			addr2_url.insert_one(addr2)
		else:
			for i in addr2_items:
				title = i.getchildren()[0].text
				url = i.attrib['href']
				addr2 = {'title':title, 'url':url}
				addr2_url.insert_one(addr2)
		LINKTIME = 3    #重置LINKTIME
		time.sleep(1)
	except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		if LINKTIME > 0:
			print('爬取失败，现在重新链接')
			get_addr2_from(addr1_url)
			LINKTIME -= 1
		else:
			addr1_bad = {'url':addr1_url, 'status':'bad'}
			crawly_addr1_url_bad.insert_one(addr1_bad)
			print('{}爬取失败'.format(addr1_url))


if __name__ == '__main__':
	url = 'http://www.dianping.com/search/category/219/10/g0r0'
	get_tag1_from(url)