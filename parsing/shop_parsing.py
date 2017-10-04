#coding=utf-8

import requests
import random
import pymongo
import time
from lxml import etree
from config import USER_AGENT, PROXY, TIMEOUT, LINKTIME, PAGE_NUM_MAX


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
crawly_addr2_url_ok = dp['crawly_addr2_url_ok']			#存储爬取成功的addr2_url

# global LINKTIME


def mix_addr2_page_url():
	addr2_set = set(i['url'] for i in addr2_url.find())
	addr2_gen = (i for i in addr2_set)
	for item in addr2_gen:
		for page in range(1, PAGE_NUM_MAX):
			url = '{}p{}'.format(item, page)
			yield url


#解析网页，提取“标题-星级-评论数-人均价格-各项评分-菜系-商区-详细地址“信息
def get_msg_from(result_url):
	global LINKTIME
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	try:
		r = s.get(result_url, proxies=proxies, timeout=TIMEOUT)
		tree = etree.HTML(r.text)
		#提取标题信息
		title_items = tree.xpath('//div[@id="shop-all-list"]//div[@class="tit"]/a[1]')

		#提取商户星级
		star_items = tree.xpath('//div[@class="comment"]/span')

		#提取评论数-人均价格
		review_price_items = tree.xpath('//div[@class="comment"]/a')
		review_price_list = []
		for i in review_price_items:
			#判断评论数-价格的a标签是否存在子元素，如果存在，则在子元素中提取评论数-价格，否则评论数-价格都为“None”
			if i.getchildren():
				text = i.getchildren()[0].text
				review_price_list.append(text)
			else:
				review_price_list.append("None")
		# print(review_price_list)
		review_price_list = [review_price_list[i:i+2] for i in range(0, len(review_price_list), 2)]

		#提取各项评分
		score_items = tree.xpath('//span[@class="comment-list"]/span/b')
		score_items = [i.text for i in score_items]
		score_items = [score_items[i:i+3] for i in range(0,len(score_items),3)]

		#提取菜系-商区-详细地址
		tag_items = tree.xpath('//div[@class="tag-addr"]//span')
		tag_items = [i.text for i in tag_items]
		tag_items = [tag_items[i:i+3] for i in range(0,len(tag_items),3)]

		for title_url, star, review_price, score, tag_area_addr in zip(title_items, star_items, review_price_list, score_items, tag_items):
			dpshop_msg = {
			    'title':title_url.attrib['title'],
			    'url':title_url.attrib['href'],
			    'star':star.attrib['title'],
			    'review':review_price[0],
			    'price':review_price[1],
			    'score':score,
			    'tag':tag_area_addr[0],
			    'area':tag_area_addr[1],
			    'addr':tag_area_addr[2]
			}
			dpshop.insert_one(dpshop_msg)
			# print(dpshop_msg)
		addr2_ok = {'url':result_url, 'status':'ok'}
		crawly_addr2_url_ok.insert_one(addr2_ok)
		LINKTIME = 3    #重置LINKTIME
		time.sleep(1)
	except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		if LINKTIME > 0:
			print('爬取失败，现在重新链接')
			get_msg_from(result_url)
			LINKTIME -= 1
		else:
			addr2_bad = {'url':result_url, 'status':'bad'}
			crawly_addr2_url_bad.insert_one(addr2_bad)
			print('{}爬取失败'.format(result_url))


#爬取所有页的商户信息
def get_all_msg_from(get_addr2_url):
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	for page in range(1, PAGE_NUM_MAX+1):
		result_url = "{}p{}".format(get_addr2_url, page)		#根据addr2_url结合页码重新构造url
		r = s.get(result_url, proxies=proxies, timeout=TIMEOUT)
		status_code = r.status_code
		if status_code == 404:
			addr2_bad = {'url':result_url, 'status':404}
			crawly_addr2_url_bad.insert_one(addr2_bad)
			print('{}没有相关商户'.format(result_url))
			break
		else:
			get_msg_from(result_url)


if __name__ == '__main__':
	# url = 'https://www.dianping.com/search/category/219/10/g0r0'
	addr2_url = 'http://www.dianping.com/search/category/219/10/g217r27028p3'
	get_msg_from(addr2_url)