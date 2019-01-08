# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request


class douyinSpider(scrapy.Spider):
    name = 'douyin'
    chinese_name = "抖音"
    allowed_domains = ['aweme.snssdk.com']

    headers = {
        "Host": "aweme.snssdk.com",
        "Connection": "keep-alive",
        "Cookie": "install_id=57005283726; ttreq=1$4a0dbe45de94b2c261ba4470caadb235daaeba62; odin_tt=4a4e27b35ee49fea4b87c0bf97cc6045521eb2cb1a6eba2bd57a992e322ce1fe144690bbd3f5b070d4e64fdb4022a3b3; sid_guard=7f0b613c53151e8f663d5667aa2ab4a8%7C1546931191%7C5184000%7CSat%2C+09-Mar-2019+07%3A06%3A31+GMT; uid_tt=ba8a9bf01162a3fe45ecee17a222ac70; sid_tt=7f0b613c53151e8f663d5667aa2ab4a8; sessionid=7f0b613c53151e8f663d5667aa2ab4a8",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": "1546931874666",
        "X-Tt-Token": "007f0b613c53151e8f663d5667aa2ab4a83581edb01c9fc144a35eb8deee9efdf03906d2746df2a2fc862d2c264ae23dfd36",
        "sdk-version": "1",
        "X-SS-TC": "0",
        "User-Agent": "com.ss.android.ugc.aweme/400 (Linux; U; Android 4.4.2; zh_CN; OPPO R11; Build/NMF26X; Cronet/58.0.2991.0)",
        "X-Gorgon": "01815c6f0a7f59ff5db3810469ab03ed9145722c3a62c70571",
        "X-Khronos": "1546931874",
        "X-Pods": "a1bf8bdca715069f27f9ab3662c19ccec595b790",
        "Content-Length": "0"
    }

    headers_video = {
        "Range": "bytes=0-163840",
        "Vpwp-Type": "preloader",
        # "Vpwp-Raw-Key": "v0200f840000bf5svk8ckqbibu1vt8jg_h264_540p",
        "Vpwp-Flag": "0",
        "Accept-Encoding": "identity",
        "Host": "aweme.snssdk.com",
        # "Connection": "Keep-Alive",
        "User-Agent": "okhttp/3.10.0.1"
    }

    def start_requests(self):
        # url = "https://aweme.snssdk.com/aweme/v1/search/item/?keyword=漫画&offset=10&count=10&source=video_search&is_pull_refresh=1&hot_search=0&ts=1546931874&js_sdk_version=&app_type=normal&openudid=8cec4b81deae6417&version_name=4.0.0&device_type=OPPO R11&ssmix=a&iid=57005283726&os_api=19&mcc_mnc=46007&device_id=59343989226&resolution=720*1280&device_brand=OPPO &aid=1128&manifest_version_code=400&app_name=aweme&_rticket=1546931874668&os_version=4.4.2&device_platform=android&version_code=400&update_version_code=4002&ac=wifi&dpi=240&uuid=863064010113316&language=zh&channel=aweGW&as=a1c594f3425aaceeb44477&cp=4fa6c7592a483fe4e1skao&mas=01801923065ea090cf1bff7e05117a2187ecec2c2c2c46a6a6c686"
        url = "https://aweme.snssdk.com/aweme/v1/search/item/?keyword=漫画&offset=10&count=10&source=video_search&is_pull_refresh=1&hot_search=0&ts=1546931874&js_sdk_version=&app_type=normal&openudid=8cec4b81deae6417&version_name=4.0.0&device_type=OPPO R11&ssmix=a&iid=57005283726&os_api=19&mcc_mnc=46007&device_id=59343989226&resolution=720*1280&device_brand=OPPO &aid=1128&manifest_version_code=400&app_name=aweme&_rticket=1546931874668&os_version=4.4.2&device_platform=android&version_code=400&update_version_code=4002&ac=wifi&dpi=240&uuid=863064010113316&language=zh&channel=aweGW"
        yield Request(url, callback=self.pares, headers=self.headers)

    def pares(self, response):
        # print response.body
        infos = json.loads(response.body)

        for info in infos["aweme_list"]:
            url = info["video"]["play_addr"]["url_list"][0]
            url_key = info["video"]["play_addr"]["url_key"]
            self.headers_video["Vpwp-Raw-Key"] = url_key
            yield Request(url, callback=self.pares_video, headers=self.headers_video,
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [302]
                          })

    def pares_video(self, response):
        print response.body
