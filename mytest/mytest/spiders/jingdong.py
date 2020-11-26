# -*- coding: utf-8 -*-
import logging

import scrapy

logger = logging.getLogger(__name__)

class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jingdong.com']
    start_urls = ['https://www.jd.com/']

    def parse(self, response):
        # logging.warning('this is warning')
        logger.warning('this is warning')
