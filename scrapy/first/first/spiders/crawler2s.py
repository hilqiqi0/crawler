# -*- coding: utf-8 -*-
import scrapy

from first.items import FirstItem


class Crawler2sSpider(scrapy.Spider):
    name = 'crawler2s'
    allowed_domains = ['hr.tencent.com']

    url = "https://hr.tencent.com/position.php?keywords=python&start="
    offset = 0
    start_urls = [url+str(offset)+"#a"]

    def parse(self, response):
        for each in response.xpath("//tr[@class='even']|//tr[@class='odd']"):
            item = FirstItem()
            item['positionName'] = each.xpath('./td[1]/a/text()').extract()[0]
            item['positionLink'] = "https://hr.tencent.com/"+each.xpath('./td[1]/a/@href').extract()[0]
            item['positionType'] = each.xpath('./td[2]/text()').extract()[0]
            yield item #返回给pipelines process_item

        if self.offset < 540:
            self.offset += 10
            nextPageUrl = self.url + str(self.offset) + "#a"
        else:
            return

        yield scrapy.Request(nextPageUrl, callback = self.parse)