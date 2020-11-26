# -*- coding: utf-8 -*-
import re
from copy import deepcopy

import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        li_list = response.xpath('//div[@class="menu-list"]//dl')
        for li in li_list:
            item = {}
            item['b_cate'] = li.xpath('./dt/h3/a/text()').get()
            dd_list = li.xpath('./dd/a')
            for dd in dd_list:
                item['s_href'] = dd.xpath('./@href').get()
                item['s_cate'] = dd.xpath('./text()').get()
                item['ci'] = item['s_href'].split['-'][1]
                item['next_url'] = 'https://list.suning.com/emall/showProductList.do?ci=' + item['ci'] + '&pg=03&cp={}'
                yield scrapy.Request(url=(item['s_href']), callback=(self.parse_book_list),
                  meta={'item': deepcopy(item)})
            else:
                page_count = int(re.findall('param.pageNumebers = "(.*?)";', response.text)[0])
                current_page = int(re.findall('param.currentPage = "(.*?)";', response.text)[0])
                if current_page < page_count:
                    next_url = item['next_url'].format(current_page + 1)
                    print(next_url)
                    yield scrapy.Request(url=next_url, callback=(self.parse_book_list), meta={'item': item})

    def parse_book_list(self, response):
        item = response.meta.get('item')
        li_list = response.xpath('//ul[@class="clearfix"]/li')
        for li in li_list:
            item['book_name'] = li.xpath('//div[@class="res-img"]//a/img/@alt').get()
            item['book_iamge'] = li.xpath('//div[@class="res-img"]//a/img/@src2').get()
            item['book_href'] = li.xpath('//div[@class="res-img"]//a/@href').get()
            if item['book_href'] is not None:
                item['book_href'] = 'http:' + item['book_href']
            yield scrapy.Request(url=(item['book_href']), callback=(self.parse_book_info),
              meta={'item': deepcopy(item)})

    def parse_book_info(self, response):
        item = response.meta.get('item')
        item['book_author'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[1]/text()').get()
        if item['book_author'] is not None:
            item['book_author'] = item['book_author'].strip()
        item['book_press'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[2]/text()').get()
        if item['book_press'] is not None:
            item['book_press'] = item['book_press'].strip()
        item['book_time'] = response.xpath('//ul[@class="bk-publish clearfix"]/li[3]/span[2]/text()').get()
        print(item)