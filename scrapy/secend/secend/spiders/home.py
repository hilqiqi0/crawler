# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup

from secend.items import SecendItem


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['sz.lianjia.com/ershoufang']
    urls = 'https://sz.lianjia.com/ershoufang/'
    start_urls = []
    for i in range(10):
        new_url = urls + 'pg' + str(i+1)
        start_urls.append(new_url)

    def parse(self, response):
        html = response.body
        bsobj = BeautifulSoup(html, "html5lib")

        house_list = bsobj.find_all("li", {"class": "clear"})
        print(len(house_list))

        for house in house_list:
            item = SecendItem()
            try:
                # 标题
                #print(house)
                item["positionTitle"] = house.find("div", {"class": "title"}).get_text()
                #print("Title"+item["positionTitle"])

                # 获取信息数据（例：加怡名城 | 2室1厅 | 62.48平米 | 西 | 精装），通过“|”符号分割字符串
                info = house.find("div", {"class": "houseInfo"}).get_text().split("|")
                #print("info"+str(info))

                # 小区（例：加怡名城），strip()去除字符串两边的空格，encode，将字符串编码成 utf-8 格式
                item["positionBlock"] = info[0].strip()
                # print(block)

                # 房型（例：2室一厅）
                item["positionType"] = info[1].strip()
                # print(house_type)

                # 面积大小，保留整数（例：62.48平米，保留整数后为 62）
                size_info = info[2].strip()
                item["positionSize"] = re.findall(r"\d+", size_info)[0]
                #print(item["positionSize"])

                # 价格，保留整数（例：120.3万，保留整数后为 120）
                price_info = house.find("div", {"class": "totalPrice"}).span.get_text()
                item["positionPrice"] = re.findall(r"\d+", price_info)[0]
                #print(item["positionPrice"])

            except IndexError:
                pass
            #print(item)
            yield item
