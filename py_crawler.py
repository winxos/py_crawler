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
import socket

socket.setdefaulttimeout(3)
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


def get_content(url, try_times=3):
    logging.debug("visiting:" + url)
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:1080'})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        f = opener.open(url).read()
        try:
            # data = f.decode(f.headers.get_content_charset()) #not robust
            logging.debug("charset " + charset_detect(f))
            data = f.decode(charset_detect(f))
            return etree.HTML(data)
        except Exception as e:
            logging.debug(e)
        return None
    except urllib.error.URLError as e:  # 捕捉访问异常，一般为timeout，信息在e中
        logging.debug("%s %s" % (e, url))
        return None
    except TimeoutError:
        logging.debug("[retry %d] %s" % (try_times, url))
        try_times -= 1
        if try_times > 0:
            return get_content(url)
        return None


def create_pages():
    entry = 'http://www.t66y.com/thread0806.php?fid=22&search=&page=%s'
    return [entry % i for i in range(1, 101)]


elements = {"item": {"type": "td[2]/text()",
                     "url": "td[2]/h3/a/@href",
                     "author": "td[3]/a/text()",
                     "title": "td[2]/h3/a/text()", },
            "sub_item": {"text": "//div[@class=\"tpc_content do_not_catch\"]/a/@href"},
            "root": "//tr[@class=\"tr3 t_one tac\"]"}


def test_py_crawler():
    pages = create_pages()
    for ip, page in enumerate(pages[1:]):
        items = get_content(page).xpath(elements["root"])
        for ii, item in enumerate(items):
            print("%5d" % (ip * 100 + ii), end=".")
            sub_page_url = "http://www.t66y.com/" + ''.join(item.xpath(elements["item"]["url"]))
            print("%30s" % sub_page_url, end=" ")
            for i in elements["item"]:
                print(''.join(item.xpath(elements["item"][i])).strip(), end="|")
            d = get_content(sub_page_url)
            real_url = str(d.xpath(elements["sub_item"]["text"])[0])
            print(real_url[24:].replace("______", "."))


test_py_crawler()
