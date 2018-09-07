# -*- coding: utf-8 -*-
import scrapy

from first.items import FirstItem


class Crawler1Spider(scrapy.Spider):
    name = 'crawler1'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?keywords=python']

    def parse(self, response):
        print("##############")
        #print(response.body.decode("utf-8"))
        for each in response.xpath("//tr[@class='even']|//tr[@class='odd']"):
            item = FirstItem()
            item['positionName'] = each.xpath('./td[1]/a/text()').extract()[0]
            item['positionLink'] = "https://hr.tencent.com/"+each.xpath('./td[1]/a/@href').extract()[0]
            item['positionType'] = each.xpath('./td[2]/text()').extract()[0]
            yield item #返回给pipelines process_item

