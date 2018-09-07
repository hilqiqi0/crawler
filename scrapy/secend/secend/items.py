# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecendItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionTitle = scrapy.Field()
    positionPrice = scrapy.Field()
    positionSize = scrapy.Field()
    positionBlock = scrapy.Field()
    positionType = scrapy.Field()

