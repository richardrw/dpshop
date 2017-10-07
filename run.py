# coding=utf-8

from parsing.cate_parsing import Get_Tag_Addr
from parsing.shop_parsing import GetAllMsg
from concurrent.futures import ProcessPoolExecutor



if __name__ == '__main__':
    start_url = 'http://www.dianping.com/search/category/219/10/g0r0'
    tag_addr_task = Get_Tag_Addr()
    get_msg_task = GetAllMsg()

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

    # 根据addr2_url爬取商户信息
    addr2_url_set = set(i['url'] for i in get_msg_task.addr2_url_db.find())
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(get_msg_task.get_all_msg_from, addr2_url_set, chunksize=50)
    print('addr2_url_reslut_url爬取完成')