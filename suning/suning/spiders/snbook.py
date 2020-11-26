# -*- coding: utf-8 -*-
import json
import re
from copy import deepcopy

import scrapy


class SnbookSpider(scrapy.Spider):
    name = 'snbook'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        category_list = response.xpath('//div[@class="submenu-left"]/p')
        for cate in category_list:
            item = {}
            b_category = cate.xpath('./a/text()').get()
            item['b_cate'] = b_category
            ul = cate.xpath('./following-sibling::ul[1]/li')
            for li in ul:
                s_category = li.xpath('./a/text()').get()
                s_link = li.xpath('./a/@href').get()
                item['s_cate'] = s_category
                item['s_link'] = s_link
                yield scrapy.Request(url=s_link, callback=(self.parse_book), meta={'item': deepcopy(item)})

    def parse_book(self, response):
        item = response.meta.get('item')
        base_url = 'https://ds.suning.com/ds/generalForTile/0000000{}__2_{}-455-2-0070160861-1--ds0000000001373.jsonp?callback=ds0000000001373'
        book_list = response.xpath('//div[@id="filter-results"]/ul/li//div[@class="res-info"]')
        total_page = re.findall('param.pageNumbers = "(.*?)";', response.text)[0]
        cateid = item['s_link'].split('-')[1]
        for book in book_list:
            item['b_name'] = book.xpath('./p[@class="sell-point"]/a/text()').get()
            item['b_href'] = book.xpath('./p[@class="sell-point"]/a/@href').get()
            item['b_seller'] = book.xpath('./p[4]/a/text()').get()
            sa_data = book.xpath('./p[@class="sell-point"]/a/@sa-data').get()
            sa_data = eval(sa_data)
            prdid = sa_data['prdid']
            shopid = sa_data['shopid']
            new_url = base_url.format(prdid, shopid)
            yield scrapy.Request(url=new_url, callback=(self.parse_book_info), meta={'item': deepcopy(item)})
        else:
            for i in range(1, int(total_page)):
                next_url = 'https://list.suning.com/1-{}-{}-0-0-0-0-14-0-4.html'.format(cateid, i)
                print(next_url)
                yield scrapy.Request(url=(response.urljoin(next_url)), callback=(self.parse_book))

    def parse_book_info(self, response):
        item = response.meta.get('item')
        json_data = re.findall('ds0000000001373\\((.*?)\\);', response.text)[0]
        data = json.loads(json_data)
        price = data['rs'][0]['price']
        item['book_price'] = price
        return item
