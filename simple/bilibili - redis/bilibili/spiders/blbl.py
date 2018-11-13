# -*- coding: utf-8 -*-
import json
import math
import random
import re
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from bilibili.items import BilibiliItem

from scrapy_redis.spiders import RedisCrawlSpider

aid_format = "https://www.bilibili.com/video/av{}/"
more_format = "https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_{}&rid={}&type=0&pn={}&ps=20&jsonp=jsonp&_={}"

parse_nav_process_request = 0
parse_nav_more_process_request = 0


class BlblSpider(RedisCrawlSpider):
    # handle_httpstatus_list = [403]
    name = 'blbl'
    redis_key = 'BlblSpider:start_urls'
    allowed_domains = ['www.bilibili.com',
                       'api.bilibili.com']
    # start_urls = ['http://www.bilibili.com/']
    sum = 0
    more_count = 0

    rules = (
        # # 首页中 查找 分类链接: 动漫、番剧、国创、舞蹈游戏。。。。
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="nav-menu"]/li/a'),
             process_request='parse_nav_process',
             callback='parse_nav_item',
             follow=True),
        # 分类链接中 查找 更多
        Rule(LinkExtractor(restrict_xpaths='//div[@class="zone-title"]//a'),
             process_request='parse_nav_more_process',
             callback='parse_nav_more_item',
             follow=True),
        # 番剧、国创
        Rule(LinkExtractor(restrict_xpaths='//div[@class="fcname"]//li/a'),
             process_request='parse_nav_more_process',
             callback='parse_nav_more_item',
             follow=True),
        # 放映厅 未完待续
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="cinema-home-crumb"]//li/a'),
        #      process_request='parse_nav_more_process',
        #      callback='parse_nav_more_item',
        #      follow=True),
        # 未爬取内容栏：广告、放映厅

        # 各个链接中 查找 视频
        # Rule(LinkExtractor(allow=r'/video/av\w*/'), callback='parse_item', follow=True),
    )

    def parse_nav_process(self, request):
        global parse_nav_process_request
        if parse_nav_process_request < 2:
            # parse_nav_process_request += 1
            return request
        pass

    def parse_nav_item(self, response):
        """response：分类页面html"""
        print response.url
        yield

    def parse_nav_more_process(self, request):
        global parse_nav_more_process_request
        if parse_nav_more_process_request < 1:
            # parse_nav_more_process_request += 1
            # time.sleep(60 * 2)
            return request
        pass

    def parse_nav_more_item(self, response):
        """
        response：分类页面html
        功能：提取用于获取分类视频的总页数参数
        """
        print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
        print response.status
        if response.status == 403:
            print "OOOOOOOOOOOOOOOOOOOOOOOOOO parse_nav_more_item OOOOOOOOOOOOOOOOOOOOOOOOOO"
            time.sleep(60 * 6)
            yield scrapy.Request(response.url, meta={"status": 403})
            return

        # https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_5884537460744637&rid=24&type=0&pn=1&ps=20&jsonp=jsonp&_=1540881226302
        # https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_7877505278116677&rid=24&type=0&pn=3&ps=20&jsonp=jsonp&_=1540881171626
        print response.url
        print response
        parse = re.compile(response.url.split('/')[-2] + r'","tid":([\d]*?),')
        rids = re.findall(parse, response.body)
        for rid in rids:
            # print rid
            while True:
                i = random.random()
                if i > 0.1:
                    index = str(int(random.random() * 10 ** 16)) + str(int(random.random() * 10))
                    break

            current_time = time.time() * 1000
            ct = str(int(current_time))

            more_url = more_format.format(index, rid, "1", ct)
            headers = {
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Host': 'api.bilibili.com',
                'Referer': response.url[:-1],
            }
            cookies = {'finger': 'edc6ecda'}

            yield scrapy.Request(more_url, callback=self.page_information_parse, headers=headers, cookies=cookies,
                                 meta={"rid": rid,
                                       "RETRY_TIMES": 10
                                       })

    def page_information_parse(self, response):
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print response.status
        if response.status == 403:
            print "XXXXXXXXXXXXXXXXXXXXXXXXX page_information_parse XXXXXXXXXXXXXXXXXXXXXXXXX"
            time.sleep(60 * 6)
            yield scrapy.Request(response.url, headers=response.request.headers, meta={"status": 403})
            return

        print response.url
        self.sum += 1
        print "计数 : " + str(self.sum)
        try:
            info = json.loads(response.body[38:-1], strict=False)
            for archive in info["data"]["archives"]:
                item = BilibiliItem()
                item["aid"] = archive["aid"]
                item["cid"] = archive["cid"]
                item["copyright"] = archive["copyright"]  # 版权：1、可以正常转载；2、无法转载
                item["tname"] = archive["tname"]  # 类别
                item["title"] = archive["title"]
                item["videos"] = archive["videos"]  # page数量
                item["ctime"] = archive["ctime"]  # 创建时间
                item["pubdate"] = archive["pubdate"]  # 更新时间
                item["duration"] = archive["duration"]  # 视频时长
                item["coin"] = archive["stat"]["coin"]
                item["favorite"] = archive["stat"]["favorite"]
                item["likes"] = archive["stat"]["like"]
                item["archive"] = json.dumps(archive)
                yield item

            total = info["data"]["page"]["count"]
            print total
            sum_page = total // 20
            remainder = total % 20
            if remainder != 0:
                sum_page += 1
            for page in range(1, sum_page + 1):
                rid = response.meta["rid"]
                while True:
                    i = random.random()
                    if i > 0.1:
                        index = str(int(random.random() * 10 ** 16)) + str(int(random.random() * 10))
                        break
                current_time = time.time() * 1000
                ct = str(int(current_time))

                more_url = more_format.format(index, rid, sum_page + 1-page, ct)
                # print more_url
                time.sleep(3)
                yield scrapy.Request(more_url, callback=self.next_information_parse, headers=response.request.headers,
                                     meta={"RETRY_TIMES": 10}
                                     )
        except Exception as e:
            print e
            if "try" not in response.meta:
                yield scrapy.Request(response.url, callback=self.page_information_parse,
                                     headers=response.request.headers,
                                     cookies=response.request.cookies, dont_filter=False,
                                     meta={"rid": response.meta["rid"], "try": 1})

    def next_information_parse(self, response):
        print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
        print response.status
        if response.status == 403:
            print "HHHHHHHHHHHHHHHHHHHHHHHHHH page_information_parse HHHHHHHHHHHHHHHHHHHHHHHHHH"
            time.sleep(60 * 6)
            yield scrapy.Request(response.url, headers=response.request.headers, meta={"status": 403})
            return

        print response.url
        self.sum += 1
        print "计数 : " + str(self.sum)

        try:
            info = json.loads(response.body[38:-1], strict=False)
            for archive in info["data"]["archives"]:
                item = BilibiliItem()
                item["aid"] = archive["aid"]
                item["cid"] = archive["cid"]
                item["copyright"] = archive["copyright"]  # 版权：1、可以正常转载；2、无法转载
                item["tname"] = archive["tname"]  # 类别
                item["title"] = archive["title"]
                item["videos"] = archive["videos"]  # page数量
                item["ctime"] = archive["ctime"]  # 创建时间
                item["pubdate"] = archive["pubdate"]  # 更新时间
                item["duration"] = archive["duration"]  # 视频时长
                item["coin"] = archive["stat"]["coin"]
                item["favorite"] = archive["stat"]["favorite"]
                item["likes"] = archive["stat"]["like"]
                item["archive"] = json.dumps(archive)
                yield item
        except Exception as e:
            print e
            if "try" not in response.meta:
                yield scrapy.Request(response.url, callback=self.next_information_parse,
                                     meta={"try": 1},
                                     headers=response.request.headers, dont_filter=False)

    # def parse_item(self, response):
    #     'https://api.bilibili.com/x/web-interface/archive/related?aid=34658673&callback=jqueryCallback_bili_5547439162420895&jsonp=jsonp&_=1540797485480'
    #     print response.url
    #     parse = re.compile(r'"aid":([\d]*?),')
    #     aids = re.findall(parse, response.body)
    #     set_aid = set()
    #     for aid in aids:
    #         set_aid.add(aid)
    #
    #     for id in set_aid:
    #         aid_url = aid_format.format(id)
    #         print "find" + aid_url
    #         # yield scrapy.Request(aid_url, callback=self.parse_item, headers=headers)
    #         yield scrapy.Request(aid_url, callback=self.parse_item)
    #
    #     try:
    #         # info = re.search('<li><span class="name">嵌入代码[\s\S]*?aid=([\d]*?)&amp;cid=([\d]*?)&amp;page=([\d]*?)&quot;[\s\S]*?</span></li>', response.body)
    #         #
    #         # print info.group(1)
    #         # print info.group(2)
    #         # print info.group(3)
    #         info = re.search(
    #             r'"stat":{"aid":([\d]*?),[\s\S]*?"pages":[\s\S]{"cid":([\d]*?),"page":([\d]*?),"from":"',
    #             response.body)
    #         print info.group(1)
    #         print info.group(2)
    #         print info.group(3)
    #         self.sum += 1
    #         print "计数 : " + str(self.sum)
    #
    #
    #     except:
    #         # https://www.bilibili.com/bangumi/play/ep253836
    #         # "ep_id":253836,"episode_status":2,"from":"bangumi","index":"动画特别篇倒计时2天！！","index_title":"","mid":29305457,"page":1,
    #         #  https://www.bilibili.com/video/av34715309
    #         # "related":[{"aid":32391827,"cid":56674698,"duration":201,"pi
    #         # info = re.search('"ep_id":([\d]*?),"cid":([\d]*?),[\s\S]*?"page":([\d]*?),"pub_real_time"', response.body)
    #         #
    #         # print info.group(1)
    #         # print info.group(2)
    #         # print info.group(3)
    #         print "xxxx"
    #         if response.url[:40] == 'https://www.bilibili.com/bangumi/play/ep'[:40]:
    #             return
    #         if "try" in response.meta:
    #             count = response.meta["try"]
    #             if count < 2:
    #                 count += 1
    #                 yield scrapy.Request(response.url, callback=self.parse_item, dont_filter=True, meta={"try": count})
    #         else:
    #             yield scrapy.Request(response.url, callback=self.parse_item, dont_filter=True,
    #                                  meta={"try": 1})
    #
    #     yield
