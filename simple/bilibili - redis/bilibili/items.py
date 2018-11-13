# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    aid = scrapy.Field()
    cid = scrapy.Field()
    copyright = scrapy.Field()
    tname = scrapy.Field()
    title = scrapy.Field()
    videos = scrapy.Field()
    ctime = scrapy.Field()
    pubdate = scrapy.Field()
    duration = scrapy.Field()
    coin = scrapy.Field()
    favorite = scrapy.Field()
    likes = scrapy.Field()
    archive = scrapy.Field()
    update_time = scrapy.Field()
