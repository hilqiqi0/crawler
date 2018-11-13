# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random
import time

import requests
from scrapy import signals


class BilibiliSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ChangeProxy(object):

    def __init__(self):
        """
        初始化变量：
        get_url：请求的api
        temp_url： 验证代理ip是否可用的地址
        """

        self.get_url = "http://dps.kdlapi.com/api/getdps/?orderid=954172582204323&num=10&pt=1&format=json&sep=1"
        self.temp_url = "http://pv.sohu.com/cityjson?ie=utf-8"
        self.ip_list = []

        self.count = 0
        self.evecount = 0

    def getIPData(self):
        """
        通过api接口获取ip，并放入ip池
        """
        temp_data = requests.get(url=self.get_url).text
        self.ip_list = []
        for eve_ip in json.loads(temp_data)["data"]["proxy_list"]:
            print eve_ip
            self.ip_list.append(eve_ip)

        if len(self.ip_list) < 1:
            print "等待"
            time.sleep(10)
            self.getIPData()

    def changeProxy(self, request):
        print self.ip_list[self.count-1]
        request.meta["proxy"] = "http://" + self.ip_list[self.count-1]

    def check(self):
        print requests.get(url=self.temp_url, proxies={"http": self.ip_list[self.count-1]}, timeout=5).text

    def ifUsed(self, request):
        try:
            self.check()
            self.changeProxy(request)
        except:
            if self.count == 0 or self.count == len(self.ip_list):
                self.getIPData()
                self.count = 1
            self.count = self.count + 1
            self.ifUsed(request)

    def process_request(self, request, spider):
        print "cccccccccccccccccccccccccc"
        print request.meta
        if "status" in request.meta:
            print request.meta["status"]
            self.count = self.count + 1

        if self.count == 0 or self.count == len(self.ip_list):
            self.getIPData()
            self.count = 1

        if self.evecount == 5:
            self.count = self.count + 1
            self.evecount = 0
        else:
            self.evecount = self.evecount + 1

        self.ifUsed(request)
