# -*- encoding:utf-8 -*-
'''
A crawler framework, can easily config to suit different content.
python3.6
winxos 2017-10-24
'''
import urllib.request
import urllib.error
from lxml import etree
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='log.txt',
    filemode='w',
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def charset_detect(f):
    char_set = ["utf8", "gb2132", "gbk"]
    for c in char_set:
        try:
            f.decode(c)
            return c
        except:
            continue
    return None


def get_content(url, try_times=1):
    logging.debug("visiting:" + url)
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:1080'})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        f = opener.open(url).read()
        try:
            # data = f.decode(f.headers.get_content_charset())
            logging.debug("charset " + charset_detect(f))
            data = f.decode(charset_detect(f))
            return etree.HTML(data)
        except Exception as e:
            logging.debug(e)
        return None
    except urllib.error.URLError or TimeoutError:  # 捕捉访问异常，一般为timeout，信息在e中
        logging.debug("[retry %d] %s" % (try_times, url))
        try_times -= 1
        if try_times > 0:
            return get_content(url)
        return None


def create_pages():
    entry = 'http://www.t66y.com/thread0806.php?fid=22&search=&page=%s'
    return [entry % i for i in range(1, 101)]


def test_py_crawler():
    pages = create_pages()
    get_content(pages[0])
    get_content("http://google.com")


test_py_crawler()
