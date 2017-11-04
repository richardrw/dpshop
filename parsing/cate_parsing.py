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
        try:
            r = self.s.get(start_url, proxies=self.proxies, timeout=self.timeout)
            tree = etree.HTML(r.text)
            tag1_items = tree.xpath('//div[@id="classfy"]/a')
            for i in tag1_items:
                tag1 = i.getchildren()[0].text
                url = i.attrib['href']
                tag1_url_msg = {'tag1': tag1, 'url': url, 'status': 'ok'}
                self.tag1_url_db.insert_one(tag1_url_msg)
            self.linktime = 3    # 重置linktime
            time.sleep(1)
        except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            if self.linktime > 0:
                print('爬取失败，现在重新链接')
                self.get_tag1_from(start_url)
                self.linktime -= 1
            else:
                print('{}爬取失败'.format(start_url))


    def get_tag2_from(self, tag1_url):
        tag1_url_msg = self.tag1_url_db.find_one({'url': tag1_url})
        tag1 = tag1_url_msg['tag1']
        try:
            r = self.s.get(tag1_url, proxies=self.proxies, timeout=self.timeout)
            tree = etree.HTML(r.text)
            tag2_items = tree.xpath('//div[@id="classfy-sub"]/a')
            if len(tag2_items) == 0:
                tag2 = 'no_sub'
                tag2_url_msg = {'tag1': tag1, 'tag2': tag2, 'url': tag1_url, 'status': 'tag1_not_sub'}
                self.tag2_url_db.insert_one(tag2_url_msg)
            else:
                for i in tag2_items:
                    tag2 = i.getchildren()[0].text
                    url = i.attrib['href']
                    tag2_url_msg = {'tag1': tag1, 'tag2': tag2, 'url': url, 'status': 'ok'}
                    self.tag2_url_db.insert_one(tag2_url_msg)
            self.crawly_tag1_ok.insert_one({'url': tag1_url})
            self.linktime = 3    # 重置linktime
            time.sleep(1)
        except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            if self.linktime > 0:
                print('爬取失败，现在重新链接')
                self.get_tag2_from(tag1_url)
                self.linktime -= 1
            else:
                print('{}爬取失败'.format(tag1_url))


    def get_addr1_from(self, tag2_url):
        tag2_url_msg = self.tag2_url_db.find_one({'url': tag2_url})
        tag1 = tag2_url_msg['tag1']
        tag2 = tag2_url_msg['tag2']
        try:
            r = self.s.get(tag2_url, proxies=self.proxies, timeout=self.timeout)
            tree = etree.HTML(r.text)
            addr1_items = tree.xpath('//div[@id="region-nav"]/a')
            for i in addr1_items:
                addr1 = i.getchildren()[0].text
                url = i.attrib['href']
                addr1_url_msg = {'tag1': tag1, 'tag2': tag2, 'addr1': addr1, 'url': url}
                self.addr1_url_db.insert_one(addr1_url_msg)
            self.crawly_tag2_ok.insert_one({'url': tag2_url})
            self.linktime = 3  # 重置linktime
            time.sleep(1)
        except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
               requests.exceptions.ConnectionError):
            if self.linktime > 0:
                print('爬取失败，现在重新链接')
                self.get_addr1_from(tag2_url)
                self.linktime -= 1
            else:
                print('{}爬取失败'.format(tag2_url))


    def get_addr2_from(self, addr1_url):
        addr1_url_msg = self.addr1_url_db.find_one({'url': addr1_url})
        tag1 = addr1_url_msg['tag1']
        tag2 = addr1_url_msg['tag2']
        addr1 = addr1_url_msg['addr1']
        try:
            r = self.s.get(addr1_url, proxies=self.proxies, timeout=self.timeout)
            tree = etree.HTML(r.text)
            addr2_items = tree.xpath('//div[@id="region-nav-sub"]/a')
            if len(addr2_items) == 0:
                addr2 = 'no_sub'
                addr2_url_msg = {'tag1': tag1, 'tag2': tag2, 'addr1': addr1, 'addr2': addr2, 'url': addr1_url, 'status': 'addr1_not_sub'}
                self.addr2_url_db.insert_one(addr2_url_msg)
            else:
                for i in addr2_items:
                    addr2 = i.getchildren()[0].text
                    url = i.attrib['href']
                    addr2_url_msg = {'tag1':tag1, 'tag2': tag2, 'addr1':addr1, 'addr2': addr2, 'url':url}
                    self.addr2_url_db.insert_one(addr2_url_msg)
            self.crawly_addr1_ok.insert_one({'url': addr1_url})
            self.linktime = 3  # 重置linktime
            time.sleep(1)
        except(
        requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError):
            if self.linktime > 0:
                print('爬取失败，现在重新链接')
                self.get_addr2_from(addr1_url)
                self.linktime -= 1
            else:
                print('{}爬取失败'.format(addr1_url))


if __name__ == '__main__':
    url = 'http://www.dianping.com/search/category/219/10/g0r0'
