# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 23:22:19 2018

@author: Administrator
"""


import re
import json
import time
import random
import requests
from pyquery import PyQuery as pq
import hashlib

url_base = 'https://www.instagram.com/instagram/'
uri = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables=%7B%22id%22%3A%22{user_id}%22%2C%22first%22%3A12%2C%22after%22%3A%22{cursor}%22%7D'

headers = {
'Connection':'keep-alive',
'Host':'www.instagram.com',
'Referer':'https://www.instagram.com/instagram/',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'
}

proxy = {
    'http': 'http://127.0.0.1:52212',
    'https': 'http://127.0.0.1:52212'
}


def hashStr(strInfo):
    h = hashlib.md5()
    h.update(strInfo.encode("utf-8"))
    return h.hexdigest()

def get_html(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_json(headers,url):
    try:
        response = requests.get(url, headers=headers,proxies=proxy, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print('请求网页json错误, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(headers,url)



def get_samples(html):
    samples = []
    user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
    GIS_rhx_gis = re.findall('"rhx_gis":"([0-9a-z]+)"', html, re.S)[0]

    print('user_id：' + user_id)
    print(GIS_rhx_gis)
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()
    for item in items:
        if item.text().strip().startswith('window._sharedData'):
            # window._sharedData 的内容转换为字典
            js_data = json.loads(item.text()[21:-1], encoding='utf-8')
            
            # 12 张初始页面图片信息
            edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
            # 网页页面信息
            page_info = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]['page_info']
            # 下一页的索引值AQCSnXw1JsoV6LPOD2Of6qQUY7HWyXRc_CBSMWB6WvKlseC-7ibKho3Em0PEG7_EP8vwoXw5zwzsAv_mNMR8yX2uGFZ5j6YXdyoFfdbHc6942w
            cursor = page_info['end_cursor']
            # 是否有下一页
            flag = page_info['has_next_page']
            
            # 节点信息筛选
            for edge in edges:               
                
                # 如果是视频直接跳过
                if edge['node']['is_video'] == "true":
                    continue
                
                time.sleep(1)
                # 图片信息筛选
                sample = {}
                if edge['node']['display_url']:
                    display_url = edge['node']['display_url']
#                    print(display_url)
                    sample["img_url"] = display_url
                    sample["comment_count"] = edge['node']['edge_media_to_comment']["count"]
                    sample["like_count"] = edge['node']['edge_liked_by']["count"] 
                    print(sample["img_url"])
                    print(sample["comment_count"])
                    print(sample["like_count"])
                                                            
                if edge['node']['shortcode']:
                    shortcode = edge['node']['shortcode']
                    # https://www.instagram.com/p/{shortcode}/?__a=1
                    textUrl = 'https://www.instagram.com/p/' + shortcode + '/?__a=1'
                    textRespose = get_json(headers,textUrl)
#                    print(textRespose)
#                    print(type(textRespose))    
                    textDict = textRespose['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']
                    sample["text"] = str(textDict)[10:-2]
                    print(sample["text"])
                    
                samples.append(sample)
                
            print(cursor, flag)
            
    # AJAX 请求更多信息                     
    while flag:
        url = uri.format(user_id=user_id, cursor=cursor)
        print(url)
        queryVariables = '{"id":"' + user_id + '","first":12,"after":"' +cursor+ '"}'
        print(queryVariables)
        headers['X-Instagram-GIS'] = hashStr(GIS_rhx_gis + ":" + queryVariables)
        print(headers)
        js_data = get_json(headers,url)
#        print(js_data)
        infos = js_data['data']['user']['edge_owner_to_timeline_media']['edges']
        cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        flag = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        
#        print(infos)
        for info in infos:
            if info['node']['is_video']:
                continue
            else:
                sample = {}
                display_url = info['node']['display_url']
#                print(display_url)
                sample["img_url"] = display_url
                sample["comment_count"] = info['node']['edge_media_to_comment']["count"]
                sample["like_count"] = info['node']['edge_media_preview_like']["count"]                    
                                                        
                if info['node']['shortcode']:
                    time.sleep(1)
                    shortcode = info['node']['shortcode']
                    # https://www.instagram.com/p/{shortcode}/?__a=1
                    textUrl = 'https://www.instagram.com/p/' + shortcode + '/?__a=1'
                    textRespose = get_json(headers,textUrl)
#                    print(textRespose)
#                    print(type(textRespose))    
                    textDict = textRespose['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']
                    sample["text"] = str(textDict)[10:-2]
                                        
                print(sample["img_url"])
                print(sample["comment_count"])
                print(sample["like_count"])  
                print(sample["text"])
                samples.append(sample)
                
        print(cursor, flag)
        
        # 下载120个 返回
        if len(samples) > 120:
            return samples

    return samples


def main():

    url = url_base
    html = get_html(url)
    samples = get_samples(html)
#    print(samples)
    with open("./samples.txt","a",encoding='utf-8') as f:
        f.write(str(samples))



if __name__ == '__main__':
    start = time.time()
    main()

