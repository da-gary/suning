# -*- coding: utf-8 -*-
import json
import time

import scrapy
from mytest.items import MytestItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&pageIndex={}&pageSize=10'
    datetime = time.time()*1000
    i = 1
    start_urls = [base_url.format(datetime,i)]


    def parse(self, response):
        data = json.loads(response.text)

        for job in data['Data']['Posts']:
            # item ={}
            item = MytestItem()
            # item['zhiwei'] =job['RecruitPostName']
            item['id'] = job['PostId']

            yield scrapy.Request(url='https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp={}&postId={}'.format(self.datetime,item['id']),
                               callback=self.parse_info,meta={'item':item})

    def parse_info(self,response):
        item = response.meta['item']
        data = json.loads(response.text)
        item['zh_name'] = data['Data']['RecruitPostName']
        item['zh_type'] = data['Data']['CategoryName']
        item['zh_ibility'] = data['Data']['Responsibility']
        item['zh_require'] = data['Data']['Requirement']

        print(item)
        if self.i <5:
            self.i+=1
            yield scrapy.Request(url=self.base_url.format(self.datetime,self.i))



