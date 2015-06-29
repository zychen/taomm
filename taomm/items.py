# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TaommItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = scrapy.Field()
    age = scrapy.Field()
    occupation = scrapy.Field()
    city = scrapy.Field()
    fans = scrapy.Field()
    detail = scrapy.Field()
    homepageUrl = scrapy.Field()
    image_urls = scrapy.Field()