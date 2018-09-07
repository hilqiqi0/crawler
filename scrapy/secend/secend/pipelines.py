# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class SecendPipeline(object):
    def process_item(self, item, spider):
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        with open("./house.csv", "a") as f:
            # writer 对象，修改默认分隔符为 "|"
            writer = csv.writer(f, delimiter="|")
            try:
                 writer.writerow([item["positionTitle"], int(item["positionPrice"]), int(item["positionSize"]), item["positionBlock"], item["positionType"]])
                 #print(item["positionBlock"], item["positionSize"], item["positionSize"])
            except:
                  pass
        return item
