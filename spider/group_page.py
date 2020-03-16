#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-03-16 11:00:06
# Project: douban

from pyspider.libs.base_handler import *
from config import target_group_id
from utils import gen_headers, random_bid, cookies, headers
import json, requests


class Handler(BaseHandler):
    crawl_config = {
        'headers': gen_headers(),
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(f'https://www.douban.com/group/{target_group_id}/members', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        current_page = int(response.url.replace('#more', '').split('start=')[-1]) if 'start=' in response.url else 0
        next_page_urls = []
        for each in response.doc('a[href^="http"]').items():
            if 'members?start=' in each.attr.href:
                next_page_urls.append(each.attr.href)
                continue
            if '/people/' in each.attr.href:
                member_id = each.attr.href.split('/people/')[-1]
                url = 'https://www.douban.com/j/contact/addtoblacklist'
                data = {
                    'people': member_id,
                    'ck': cookies.get('ck')
                }
                if not member_id.startswith('1'):
                    continue
                headers = {
                    'Connection': 'keep-alive',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Sec-Fetch-Dest': 'empty',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Origin': 'https://www.douban.com',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-Mode': 'cors',
                    'Referer': 'https://www.douban.com/people/87926379/',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6',
                }
                headers['Referer'] = each.attr.href
                ck = response.cookies

                print(response.cookies)
                resp = requests.post(url, data=data, cookies=ck, headers=headers).json()
                print(resp)
                # self.crawl(url, data=data, cookies=response.cookies, callback=self.detail_page, headers=headers, method="POST")
                continue

        next_page_start = min([int(i.replace('#more', '').split('?start=')[-1]) for i in next_page_urls if
                               int(i.replace('#more', '').split('?start=')[-1]) > current_page])
        next_page_url = f'https://www.douban.com/group/{target_group_id}/members?start={next_page_start}'
        self.crawl(next_page_url, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "text": response.content,
            "title": response.doc('title').text(),
        }


