# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from bilibili.settings import SQLALCHEMY_DATABASE_URI_1
from bilibili.sql_models import SqlalchemyHelper
from bilibili.sql_table import bilibiliInformation, bilibili_info_base


class BilibiliPipeline(object):
    def process_item(self, item, spider):
        # print item
        item["update_time"] = datetime.datetime.now()
        # print item["archive"]
        # 基本信息保存
        sqlalchemyhelper = SqlalchemyHelper(SQLALCHEMY_DATABASE_URI_1, bilibiliInformation, bilibili_info_base)
        # 查询数据库中是否存在aid记录,存在则更新,不存在则插入数据
        if sqlalchemyhelper.findMatch(bilibili_info_base.aid, item['aid']):
            print("数据库中查询到视频AID：{}，需要更新。。。".format(item["aid"]))
            sqlalchemyhelper.updata_item(spider.name,
                                         item['aid'],
                                         aid=item["aid"],
                                         title=item["title"],
                                         cid=item["cid"],
                                         copyright=item["copyright"],
                                         tname=item["tname"],
                                         videos=item["videos"],
                                         ctime=datetime.datetime.fromtimestamp(item["ctime"]),
                                         pubdate=datetime.datetime.fromtimestamp(item["pubdate"]),
                                         duration=item["duration"],
                                         coin=item["coin"],
                                         favorite=item["favorite"],
                                         likes=item["likes"],
                                         archive=item["archive"],
                                         update_time=item["update_time"])
        else:
            print("数据库中未查询到视频AID：{}，需要添加。。。".format(item["aid"]))
            Dataitem = bilibili_info_base(aid=item["aid"],
                                          title=item["title"],
                                          cid=item["cid"],
                                          copyright=item["copyright"],
                                          tname=item["tname"],
                                          videos=item["videos"],
                                          ctime=datetime.datetime.fromtimestamp(item["ctime"]),
                                          pubdate=datetime.datetime.fromtimestamp(item["pubdate"]),
                                          duration=item["duration"],
                                          coin=item["coin"],
                                          favorite=item["favorite"],
                                          likes=item["likes"],
                                          archive=item["archive"],
                                          update_time=item["update_time"])
            sqlalchemyhelper.insert_item(Dataitem)

        return item
