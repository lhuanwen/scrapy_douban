#!/usr/local/bin/python3
#-*- coding:UTF-8 -*-

from scrapy import cmdline

cmdline.execute('scrapy crawl douban_spider'.split())