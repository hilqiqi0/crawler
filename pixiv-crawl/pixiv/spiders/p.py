# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import FormRequest, Request


class PSpider(scrapy.Spider):
    """
    自动加载cookie
    """

    name = 'p'
    allowed_domains = ['pixiv.net']
    start_urls = ['https://www.pixiv.net/']
    header = {
        'Origin': 'https://accounts.pixiv.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'accounts.pixiv.net',
    }

    def parse(self, response):
        print response
        token = re.search(r'pixiv.context.token = "(.*?)"', response.body).group(1)

        post_data = {
            "pixiv_id": "xxxxxxxxxxx@qq.com",
            "password": "*********",
            "captcha": "",
            "g_recaptcha_response": "",
            "post_key": token,
            "source": "pc",
            "ref": "wwwtop_accounts_index",
            "return_to": "http://www.pixiv.net/",
        }

        yield FormRequest("https://accounts.pixiv.net/api/login?lang=zh", headers=self.header,
                          formdata=post_data, callback=self.login)

    def login(self, response):
        """
        公开: 'https://www.pixiv.net/bookmark.php?rest=show',
        非公开: 'https://www.pixiv.net/bookmark.php?rest=hide',
        作者栏：'https://www.pixiv.net/member.php?id=2741291'
        搜索（風景）：'https://www.pixiv.net/search.php?s_mode=s_tag&word=%E9%A2%A8%E6%99%AF'
        日榜：'https://www.pixiv.net/ranking.php?mode=daily&date=20181114'
        周榜：'https://www.pixiv.net/ranking.php?mode=weekly&date=20181114'
        月榜：'https://www.pixiv.net/ranking.php?mode=monthly&date=20181114'
        男孩榜：'https://www.pixiv.net/ranking.php?mode=male&date=20181114'
        女孩榜：'https://www.pixiv.net/ranking.php?mode=female&date=20181114'

        '便捷获取数据格式': ['https://www.pixiv.net/ranking.php?mode=daily&p={0}&format=json'.format(i) for i in range(start_page, end_page)],

        推荐作者：'https://www.pixiv.net/rpc/index.php?mode=get_recommend_users_and_works_by_user_ids&user_ids=11&user_num=30&work_num=5&tt=4551803dc533146a9303accf71e23d2e' #  'device_token=458bf3763ef90f07e699577608e90591'
        """

        yield Request("https://www.pixiv.net/", callback=self.center)
        pass

    def center(self, response):
        print response.body
        pass
