#coding=utf-8

import pymongo

DB_NAME = 'dp'
COLLECTION_NAME = 'dpshop'
HOST = 127.0.0.1
PORT = 27017



#伪装浏览器
USER_AGENT = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
    ]

PROXY = [
    '101.37.79.125:3128',
    '166.111.77.32:3128',
    '120.24.208.42:9999',
    '120.132.71.212:80',
    '119.90.63.3:3128',
    '42.51.26.29:3128',
    '45.51.26.79:3128',
    '219.141.189.236:3128',
    '42.202.130.246:3128',
    '121.196.226.246:84'
    ]

TIMEOUT = 5