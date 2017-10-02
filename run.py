#coding=utf-8

import pymongo
from parsing.cate_parsing import get_tag1_from, get_tag2_from, get_addr1_from, get_addr2_from
from parsing.shop_parsing import get_msg_from
from concurrent.futures import ProcessPoolExecutor


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


start_url = 'http://www.dianping.com/search/category/219/10/g0r0'


#爬取一级菜系
get_tag1_from(start_url)
print('tag1_url插入完毕')


#爬取二级菜系
tag1_list = tag1_url.find()
tag1_set = set(i['url'] for i in tag1_list)
for tag1 in tag1_set:
	url = tag1
	get_tag2_from(url)
print('tag2_url插入完毕')


#爬取二级菜系下的一级地址
tag2_list = tag2_url.find()
tag2_set = set(i['url'] for i in tag2_list)
for tag2 in tag2_set:
	url = tag2
	get_addr1_from(url)
print('addr1_url插入完毕')


#爬取二级菜系的的二级地址
addr1_list = addr1_url.find()
addr1_set = set(i['url'] for i in addr1_list)
for addr1 in addr1_set:
	url = addr1
	get_addr2_from(url)
print('addr2_url插入完毕')


#爬取商店信息
addr2_list = addr2_url.find()
addr2_set = set(i['url'] for i in addr2_list)
with ProcessPoolExecutor(max_workers=2) as executor:
	for addr2 in addr2_set:
		url = addr2
		executor.submit(get_msg_from, url)
print('dpshop_msg插入完毕')