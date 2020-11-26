# -*- coding: utf-8 -*-
from copy import deepcopy

import scrapy
from scrapy_redis.spiders import RedisCrawlSpider


class DangdangSpider(RedisCrawlSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = "dangdang"

    def parse(self, response):

        div_list = response.xpath('//div[@class="con flq_body"]/div')
        for div in div_list:
            item = {}
            item['b_cate'] = div.xpath('./dl/dt//text()').getall()
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip()) > 0]
            # print(item)

            dl_list = div.xpath('.//dl[@class="inner_dl"]')
            for dl in dl_list:
                dt = dl.xpath('./dt/text()').get().strip()
                dt_a = dl.xpath('./dt/a/text()').get()
                if dt_a is not None:
                    item['m_cate'] = dt_a.strip()
                else:
                    item['m_cate'] = dt

                a_list = dl.xpath('./dd')
                for a in a_list :
                    item['s_cate'] = a.xpath('./a/@title').get()
                    item['s_href'] = a.xpath('./a/@href').get()

                    yield scrapy.Request(url= item['s_href'],
                                         callback=self.parse_book_list,
                                         meta={'item':deepcopy(item)})
    def parse_book_list(self,response):
        item = response.meta.get('item')
        diff_html = response.xpath('//ul[@class="list_aa "]/li')
        gen_html = response.xpath('//ul[@class="bigimg"]/li')

        if diff_html is None:
            book_list = gen_html
            for book in book_list:
                item['book_name'] = book.xpath('./p[@class="name"]/a/text()').get()
                item['book_detail'] = book.xpath('./p[@class="detail"]/text()').get()
                item['book_price'] = book.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').get()
                item['book_href'] = book.xpath('./a/@href').get()
                print(item)
        else:
            book_list = diff_html
            for book in book_list:
                item['book_name'] = book.xpath('./p[@class="name"]/a/text()').get()
                item['book_price'] = book.xpath('./p[@class="price"]/span')
                if item['book_price'] is not None:
                    item['book_price'] = item['book_price'][0].xpath('string(.)').get()

                item['book_href'] = book.xpath('./a/@href').get()
                # print(item)


        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            print(response.urljoin(next_page))
            # yield scrapy.Request(url=response.urljoin(next_page),
            #                      callback=self.parse_book_list,
            #                      meta={'item':deepcopy(item)})


