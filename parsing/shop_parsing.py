#coding=utf-8

import requests
import random
import pymongo
import time
from lxml import etree
from config import USER_AGENT, PROXY, TIMEOUT, LINKTIME, PAGE_NUM_MAX


client = pymongo.MongoClient('localhost', 27017)
dp = client['dp']
addr2_url_db = dp['addr2_url_db']  # 存储从addr1_url中成功爬取到的addr2_url
dpshop = dp['dpshop']  # 存储从addr2中成功爬取到的dpshop_msg
crawly_addr2_ok = dp['crawly_addr2_ok']  # 存储爬取成功的addr2_url


# def callback(future):
#     response, addr2_url = future.result()
#     get_msg_from(response, addr2_url)


def get_msg_from(response, addr2_url):
    # 不公开爬虫细节


def get_all_msg_from(addr2_url):
    # 不公开爬虫细节


def requests_url(result_url, linktime=LINKTIME):
    # 不公开爬虫细节


if __name__ == '__main__':
    addr2_url = 'http://www.dianping.com/search/category/219/10/g217r27028p3'