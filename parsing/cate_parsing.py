#coding=utf-8

import requests
import random
import pymongo
import time
from lxml import etree
from config import USER_AGENT, PROXY, TIMEOUT, LINKTIME

# 现已解决以下问题，将数据库链接独立出来，不需每次实例化类的时候进行数据库链接等初始化操作

# tag1_url, tag2_url, addr1_url数量较少，故使用单进程爬取即可，因此将get_tag1_from, get_tag2_from, get_addr1_from这三个函数封装在Get_Tag_Addr类中，
# addr2_url是根据addr1_url 来爬取的，数量较多，需采用多进程爬取。原本也将get_addr2_from一起封装在Get_Tag_Addr类中的，但是实际测试中发现， 由于构造函数__init__
# 定义了数据库链接等操作，在多进程模式下会导致can't pickle _thread.lock objects错误。因此，从简出发，将get_addr2_from函数单独出来不进行封装。

client = pymongo.MongoClient('localhost', 27017)
dp = client['dp']


# 爬取一级菜系、二级菜系、二级菜系下的一级地址
class GetTagAddr(object):
    headers = random.choice(USER_AGENT)
    proxies = {'http':random.choice(PROXY)}
    s = requests.Session()
    s.headers.update({'User-Agent':headers})
    linktime = LINKTIME
    timeout = TIMEOUT
    tag1_url_db = dp['tag1_url_db']             # 存储从start_url中成功爬取到的tag1_url
    tag2_url_db = dp['tag2_url_db']                    # 存储从tag1_url中成功爬取到的tag2_url
    crawly_tag1_ok = dp['crawly_tag1_ok']    # 存储爬取成功的tag1_url
    addr1_url_db = dp['addr1_url_db']            # 存储从tag2_url中成功爬取到的addr1_url
    crawly_tag2_ok = dp['crawly_tag2_ok']    # 存储爬取成功的tag2_url
    addr2_url_db = dp['addr2_url_db']            # 存储从addr1_url中成功爬取到的addr2_url
    crawly_addr1_ok = dp['crawly_addr1_ok']  # 存储爬取成功的addr1_url


    def get_tag1_from(self, start_url):
        # 不公开爬虫细节


    def get_tag2_from(self, tag1_url):
        # 不公开爬虫细节


    def get_addr1_from(self, tag2_url):
        # 不公开爬虫细节


    def get_addr2_from(self, addr1_url):
        # 不公开爬虫细节


if __name__ == '__main__':
    url = 'http://www.dianping.com/search/category/219/10/g0r0'
