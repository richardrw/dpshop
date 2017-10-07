#coding=utf-8

import requests
import random
import pymongo
import time
from lxml import etree
from config import USER_AGENT, PROXY, TIMEOUT, LINKTIME, PAGE_NUM_MAX


client = pymongo.MongoClient('localhost', 27017)
dp = client['dp']


class GetAllMsg(object):
    timeout = TIMEOUT
    linktime = LINKTIME
    page_limit = PAGE_NUM_MAX+1
    headers_list = USER_AGENT
    proxy_lsit = PROXY
    s = requests.Session()
    addr2_url_db = dp['addr2_url_db']                         # 存储从addr1_url中成功爬取到的addr2_url
    dpshop = dp['dpshop']                                     # 存储从addr2中成功爬取到的dpshop_msg
    crawly_addr2_url_bad = dp['crawly_addr2_url_bad']              # 存储爬取失败的addr2_url
    crawly_addr2_url_ok = dp['crawly_addr2_url_ok']                # 存储爬取成功的addr2_url
    
    
    
    def get_msg_from(self, html, addr2_url):
        addr2_obj = self.addr2_url_db.find_one({'url': addr2_url})
        tag2 = addr2_obj['tag']
        addr2 = addr2_obj['addr']
        tree = etree.HTML(html)
        # 提取标题信息
        title_items = tree.xpath('//div[@id="shop-all-list"]//div[@class="tit"]/a[1]')
    
        # 提取商户星级
        star_items = tree.xpath('//div[@class="comment"]/span')
    
        # 提取评论数-人均价格
        review_price_items = tree.xpath('//div[@class="comment"]/a')
        review_price_list = []
        for i in review_price_items:
            # 判断评论数-价格的a标签是否存在子元素，如果存在，则在子元素中提取评论数-价格，否则评论数-价格都为“None”
            if i.getchildren():
                text = i.getchildren()[0].text
                review_price_list.append(text)
            else:
                review_price_list.append("None")
        review_price_list = [review_price_list[i:i + 2] for i in range(0, len(review_price_list), 2)]
    
        # 提取各项评分
        score_items = tree.xpath('//span[@class="comment-list"]/span/b')
        score_items = [i.text for i in score_items]
        score_items = [score_items[i:i + 3] for i in range(0, len(score_items), 3)]
    
        # 提取菜系-商区-详细地址
        tag_items = tree.xpath('//div[@class="tag-addr"]//span')
        tag_items = [i.text for i in tag_items]
        tag_items = [tag_items[i:i + 3] for i in range(0, len(tag_items), 3)]
    
        for title_url, star, review_price, score, tag_area_addr in zip(title_items, star_items, review_price_list,
                                                                       score_items, tag_items):
            dpshop_msg = {
                'title': title_url.attrib['title'],
                'url': title_url.attrib['href'],
                'star': star.attrib['title'],
                'review': review_price[0],
                'price': review_price[1],
                'score': score,
                'tag': tag2,
                'addr': addr2,
                'full_addr': tag_area_addr[2]
            }
            self.dpshop.insert_one(dpshop_msg)
        addr2_ok = {'tag': tag2, 'addr': addr2, 'url': addr2_url, 'status': 'ok'}
        self.crawly_addr2_url_ok.insert_one(addr2_ok)


    def get_all_msg_from(self, addr2_url):
        for page in range(1, self.page_limit):
            result_url = '{}p{}'.format(addr2_url, page)
            status_code, html = self.requests_url(result_url)
            if status_code == 'link_bad':
                print('请求失败，请在crawly_addr2_url_bad中查看请求失败url')
                break
            elif status_code == 404:
                addr2_bad = {'url':result_url, 'status':404}
                self.crawly_addr2_url_bad.insert_one(addr2_bad)
                print('{}没有相关商户'.format(result_url))
                break
            else:
                self.get_msg_from(html, addr2_url)
    
    
    def requests_url(self, result_url):
        headers = random.choice(self.headers_list)
        self.s.headers.update({'User-Agent': headers})
        proxies = {'http':random.choice(self.proxy_lsit)}
        try:
            r = self.s.get(result_url, proxies=proxies, timeout=self.timeout)
            self.linktime = 3
            time.sleep(1)
            return r.status_code, r.text
        except(requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,
               requests.exceptions.ConnectionError):
            if self.linktime > 0:
                print('请求失败，现在重新链接')
                self.requests_url(result_url)
                self.linktime -= 1
            else:
                addr2_bad = {'url': result_url, 'status': 'link_bad'}
                self.crawly_addr2_url_bad.insert_one(addr2_bad)
                status_code = 'link_bad'
                html = None
                return status_code, html


if __name__ == '__main__':
    addr2_url = 'http://www.dianping.com/search/category/219/10/g217r27028p3'