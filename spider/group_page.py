#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-03-16 11:00:06
# Project: douban

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.douban.com/group/685388/members', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        next_page_urls = []
        for each in response.doc('a[href^="http"]').items():
            if 'members?start=' in each.attr.href:
                next_page_urls.append(each.attr.href)
            if '/people/' in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

        next_page_start = min([int(i.split('?start=')[-1]) for i in next_page_urls])
        next_page_url = 'https://www.douban.com/group/685388/members?start=' + str(next_page_start)
        self.crawl(next_page_url, callback=self.index_page)
           
    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
