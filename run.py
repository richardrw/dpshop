# coding=utf-8

from parsing.cate_parsing import GetTagAddr
from parsing.shop_parsing import get_all_msg_from, crawly_addr2_ok
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


if __name__ == '__main__':
    start_url = 'http://www.dianping.com/search/category/219/10/g0r0'
    tag_addr_task = GetTagAddr()

    # 爬取tag1_url
    tag_addr_task.get_tag1_from(start_url)
    print('tag1_url爬取完成')

    # 爬取tag2_url
    tag1_wait = set(i['url'] for i in tag_addr_task.tag1_url_db.find())
    tag1_ok = set(i['url'] for i in tag_addr_task.crawly_tag1_ok.find())
    tag1_task = tag1_wait - tag1_ok
    for tag1_url in tag1_task:
        tag_addr_task.get_tag2_from(tag1_url)
    print('tag2_url爬取完成')

    # 爬取addr1_url
    tag2_wait = set(i['url'] for i in tag_addr_task.tag2_url_db.find())
    tag2_ok = set(i['url'] for i in tag_addr_task.crawly_tag2_ok.find())
    tag2_task = tag2_wait - tag2_ok
    for tag2_url in tag2_task:
        tag_addr_task.get_addr1_from(tag2_url)
    print('addr1_url爬取完成')

    # 爬取addr2_url
    addr1_wait = set(i['url'] for i in tag_addr_task.addr1_url_db.find())
    addr1_ok = set(i['url'] for i in tag_addr_task.crawly_addr1_ok.find())
    addr1_task = addr1_wait - addr1_ok
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(tag_addr_task.get_addr2_from, addr1_task)
    print('addr2_url爬取完成')

    # 根据addr2_url爬取商户信息
    addr2_wait = set(i['url'] for i in tag_addr_task.addr2_url_db.find())
    addr2_ok = set(i['url'] for i in crawly_addr2_ok.find())
    addr2_task = addr2_wait - addr2_ok
    with ThreadPoolExecutor(max_workers=8) as executor:
        for url in addr2_task:
            v = executor.submit(get_all_msg_from, url)
        executor.shutdown(wait=True)
            # executor.map(get_all_msg_from, addr2_task, chunksize=50)
    print('addr2_url_reslut_url爬取完成')