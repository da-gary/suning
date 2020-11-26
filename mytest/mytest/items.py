# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MytestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zh_name = scrapy.Field()
    id = scrapy.Field()
    zh_type = scrapy.Field()
    zh_ibility = scrapy.Field()
    zh_require = scrapy.Field()
