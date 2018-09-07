# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class FirstPipeline(object):
    def process_item(self, item, spider):

        with open("crawler.txt", "ab") as f:
            text = json.dumps(dict(item), ensure_ascii=False)+"\n"
            f.write(text.encode("utf-8"))

        return item
