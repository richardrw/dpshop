# coding=utf-8

import pymongo
from parsing.cate_parsing import Get_Tag_Addr
from parsing.shop_parsing import get_all_msg_from
from concurrent.futures import ProcessPoolExecutor

# client = pymongo.MongoClient('localhost', 27017)
# dp = client['dp']
# tag1_url = dp['tag1_url']                            #存储从start_url中成功爬取到的tag1_url
# tag2_url = dp['tag2_url']                            #存储从tag1_url中成功爬取到的tag2_url
# crawly_tag1_url_bad = dp['crawly_tag1_url_bad']            #存储爬取失败的tag1_url
# addr1_url = dp['addr1_url']                            #存储从tag2_url中成功爬取到的addr1_url
# crawly_tag2_url_bad = dp['crawly_tag2_url_bad']            #存储爬取失败的tag2_url
# addr2_url = dp['addr2_url']                            #存储从addr1_url中成功爬取到的addr2_url
# crawly_addr1_url_bad = dp['crawly_addr1_url_bad']        #存储爬取失败的addr1_url
# dpshop = dp['dpshop']                                #存储从addr2中成功爬取到的dpshop_msg
# crawly_addr2_url_bad = dp['crawly_addr2_url_bad']        #存储爬取失败的addr2_url
# crawly_addr2_url_ok = dp['crawly_addr2_url_ok']            #存储爬取成功的addr2_url


# start_url = 'http://www.dianping.com/search/category/219/10/g0r0'
#
# if __name__ == '__main__':
#     #爬取一级菜系
#     get_tag1_from(start_url)
#     print('tag1_url插入完毕')
#
#
#     #爬取二级菜系
#     tag1_list = tag1_url.find()
#     tag1_set = set(i['url'] for i in tag1_list)
#     for tag1 in tag1_set:
#         url = tag1
#         get_tag2_from(url)
#     print('tag2_url插入完毕')
#
#
#     #爬取二级菜系下的一级地址
#     tag2_list = tag2_url.find()
#     tag2_set = set(i['url'] for i in tag2_list)
#     for tag2 in tag2_set:
#         url = tag2
#         get_addr1_from(url)
#     print('addr1_url插入完毕')
#
#
#     # #爬取二级菜系的的二级地址
#     # addr1_list = addr1_url.find()
#     # addr1_set = set(i['url'] for i in addr1_list)
#     # for addr1 in addr1_set:
#     #     url = addr1
#     #     get_addr2_from(url)
#     # print('addr2_url插入完毕')
#
#
#     #爬取二级菜系的二级地址-多进程
#     addr1_set = set(i['url'] for i in addr1_url.find())
#     with ProcessPoolExecutor(max_workers=2) as executor:
#         executor.map(get_addr2_from, addr1_set, chunksize=10)
#     print('addr2_url插入完毕')
#
#
#     # #爬取商店信息
#     # to_crawly_url = mix_addr2_page_url()
#     # with ProcessPoolExecutor(max_workers=2) as executor:
#     #     executor.map(get_msg_from, to_crawly_url, chunksize=100)
#     # print('dpshop插入完毕')
#
#
#     #爬取商店信息-方法二
#     addr2_set = set(i['url'] for i in addr2_url.find())
#     with ProcessPoolExecutor(max_workers=2) as executor:
#         executor.map(get_all_msg_from, addr2_set, chunksize=50)
#     print('dpshop插入完毕')


if __name__ == '__main__':
    start_url = 'http://www.dianping.com/search/category/219/10/g0r0'
    tag_addr_task = Get_Tag_Addr()

    # 爬取tag1_url
    tag_addr_task.get_tag1_from(start_url)
    print('tag1_url爬取完成')

    # 爬取tag2_url
    tag1_url_set = set(i['url'] for i in tag_addr_task.tag1_url_db.find())
    for tag1_url in tag1_url_set:
        tag_addr_task.get_tag2_from(tag1_url)
    print('tag2_url爬取完成')

    # 爬取addr1_url
    tag2_url_set = set(i['url'] for i in tag_addr_task.tag2_url_db.find())
    for tag2_url in tag2_url_set:
        tag_addr_task.get_addr1_from(tag2_url)
    print('addr1_url爬取完成')

    # 爬取addr2_url
    addr1_url_set = set(i['url'] for i in tag_addr_task.addr1_url_db.find())
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(tag_addr_task.get_addr2_from, addr1_url_set, chunksize=10)
    print('addr2_url爬取完成')