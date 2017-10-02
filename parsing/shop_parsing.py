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
# tag1_url = dp['tag1_url']							#存储从start_url中成功爬取到的tag1_url
# tag2_url = dp['tag2_url']							#存储从tag1_url中成功爬取到的tag2_url
# crawly_tag1_url_bad = dp['crawly_tag1_url_bad']			#存储爬取失败的tag1_url
# addr1_url = dp['addr1_url']							#存储从tag2_url中成功爬取到的addr1_url
# crawly_tag2_url_bad = dp['crawly_tag2_url_bad']			#存储爬取失败的tag2_url
# addr2_url = dp['addr2_url']							#存储从addr1_url中成功爬取到的addr2_url
# crawly_addr1_url_bad = dp['crawly_addr1_url_bad']		#存储爬取失败的addr1_url
dpshop = dp['dpshop']								#存储从addr2中成功爬取到的dpshop_msg
crawly_addr2_url_bad = dp['crawly_addr2_url_bad']		#存储爬取失败的addr2_url


#解析网页，提取“标题-星级-评论数-人均价格-各项评分-菜系-商区-详细地址“信息
def get_msg_from(addr2_url):
	headers = random.choice(USER_AGENT)
	proxies = {'http':random.choice(PROXY)}
	s = requests.Session()
	s.headers.update({'User-Agent':headers})
	try:
		r = s.get(url, proxies=proxies, timeout=TIMEOUT)
		tree = etree.HTML(r.text)
		#提取标题信息
		title_items = tree.xpath('//div[@id="shop-all-list"]//div[@class="tit"]/a[1]')
		# for i in title_items:
		# 	shop_data['title'] = i.attrib['title']
		# 	shop_data['url'] = i.attrib['href']


		#提取商户星级
		star_items = tree.xpath('//div[@class="comment"]/span')
		# for i in star_items:
		# 	star = i.attrib['title']
		# 	print(star)


		#提取评论数
		# review_items = tree.xpath('//div[@class="comment"]/a[@class="review-num"]/b')
		# for i in review_items:
		# 	review = i.text
		# 	print(review)


		#提取人均价格
		# price_items = tree.xpath('//div[@class="comment"]/a[@class="mean-price"]')
		# for i in price_items:
		# 	#判断a标签下是否存在子元素，如果存在，则在子元素中提取价格，否则价格为“-”
		# 	if i.getchildren():
		# 		price = i.getchildren()[0].text
		# 	else:
		# 		price = "-"
		# 	print(price)


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
		# for i in review_price_list:
		# 	print(i)


		#提取各项评分
		score_items = tree.xpath('//span[@class="comment-list"]/span/b')
		score_items = [i.text for i in score_items]
		score_items = [score_items[i:i+3] for i in range(0,len(score_items),3)]
		# for i in score_items:
		# 	print(i)


		#提取菜系-商区-详细地址
		tag_items = tree.xpath('//div[@class="tag-addr"]//span')
		tag_items = [i.text for i in tag_items]
		tag_items = [tag_items[i:i+3] for i in range(0,len(tag_items),3)]
		# for i in tag_items:
			# print(i)


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
		time.sleep(1)
	except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		global LINKTIME
		if LINKTIME < 3:
			pirnt('爬取失败，现在重新链接')
			get_msg_from(addr2_url)
			LINKTIME -= 1
		else:
			addr2_bad = {'url':addr2_url, 'status':'bad'}
			crawly_addr2_url_bad.insert_one(addr2_bad)
			print('{}爬取失败'.format(addr2_url))



if __name__ == '__main__':
	url = 'https://www.dianping.com/search/category/219/10/g0r0'
	get_msg_from(url)