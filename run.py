#coding=utf-8

import pymongo
from parsing.cate_parsing import get_tag1_from, get_tag2_from, get_addr1_from, get_addr2_from
from parsing.shop_parsing import get_msg_from
from concurrent.futures import ProcessPoolExecutor


client = pymongo.MongoClient('localhost', 27017)
dp = client['dp']
tag1_url = dp['tag1_url']
tag2_url = dp['tag2_url']
addr1_url = dp['addr1_url']
addr2_url = dp['addr2_url']
dpshop = dp['dpshop']


url = 'http://www.dianping.com/search/category/219/10/g0r0'
get_tag1_from(url)
print('tag1_url插入完毕')


tag1_list = tag1_url.find()
for tag1 in tag1_url:
	url = tag1['url']
	get_tag2_from(url)
print('tag2_url插入完毕')


tag2_list = tag2_url.find()
for tag2 in tag2_list:
	url = tag2['url']
	get_addr1_from(url)
print('addr1_url插入完毕')


addr1_list = addr1_url.find()
for addr1 in addr1_list:
	url = addr1['url']
	get_addr2_from(url)
print('addr2_url插入完毕')


#爬取商店信息
addr2_list = addr2_url.find()
with ProcessPoolExecutor(max_workers=2) as executor:
	for addr2 in addr2_list:
		url = addr2['url']
		executor.submit(get_msg_from, url)
print('dpshop_msg插入完毕')