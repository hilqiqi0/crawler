# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 08:38:25 2018

@author: Administrator
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import csv

import myPymysql

# 此函数用于打开浏览器
browser = webdriver.Chrome()

def telparse(xx):
    # 规则
    #.fn-mcun{background:-8.0px -7.0px;}
    #.fn-PV9m{background:-22.0px -7.0px;}
    #.fn-YSfV{background:-36.0px -7.0px;}
    #.fn-kiQs{background:-50.0px -7.0px;}
    #.fn-SbXU{background:-64.0px -7.0px;}
    #.fn-xBtZ{background:-78.0px -7.0px;}
    #.fn-BARz{background:-92.0px -7.0px;}
    #.fn-QQA6{background:-106.0px -7.0px;}
    #.fn-Gypm{background:-120.0px -7.0px;}
    #268534079
    #268534079
    a = xx.replace('<p class="expand-info tel"> <span class="info-name">',"")
    a = a.replace('</span> <span class="',"")
    a = a.replace('"></span><span class="',"")
    a = a.replace('"></span>',"")
    a = a.replace('<span class="',"")
    a = a.replace(' </p>',"")
    a = a.replace('fn-mcun',"2")
    a = a.replace('fn-PV9m',"6")
    a = a.replace('fn-YSfV',"8")
    a = a.replace('fn-kiQs',"5")
    a = a.replace('fn-SbXU',"3")
    a = a.replace('fn-xBtZ',"4")
    a = a.replace('fn-BARz',"0")
    a = a.replace('fn-QQA6',"7")
    a = a.replace('fn-Gypm',"9")
    a = a.replace('   ',",")
    a = a.replace('</span>',",")
    return a
    
# 火锅
url = "http://www.dianping.com/shenzhen/ch10/g110"
browser.get(url)
print(browser.current_window_handle)
handle = browser.current_window_handle

time.sleep(5)
print("开始……")

#for i in range(1,16):
#    shop_path = '//*[@id="shop-all-list"]/ul/li[' + str(i) + ']/div[2]/div[1]/a[1]/h4'
#    shop_path_a = '//*[@id="shop-all-list"]/ul/li[' + str(i) + ']/div[2]/div[1]/a/h4'
##    print(shop_path)
##    print(shop_path_a)
#    
#    try:
#        browser.find_element_by_xpath(shop_path).click()
#        print(shop_path)
#    except:
#        browser.find_element_by_xpath(shop_path_a).click()
#        print(shop_path_a)
#
#    handles = browser.window_handles
#    
#    for newhandle in handles:
#        # 筛选新打开的窗口
#        if newhandle!=handle:
#            # 切换到新打开的窗口B
#            browser.switch_to_window(newhandle)
#    #        print(browser.find_element_by_xpath('//*[@id="basic-info"]/h1/text()'))
#            time.sleep(10)
#            # 关闭当前窗口B
#            browser.close()
#            #切换回窗口A
#            browser.switch_to_window(handles[0]) 

counte = 1;     #查询页数
next_index = 11; #翻页索引
number = 2; #需要查询的总页数
while True:
    
    # 详细信息
    
    for i in range(1,16):
#    for i in range(1,2):
        shop_path = '//*[@id="shop-all-list"]/ul/li[' + str(i) + ']/div[2]/div[1]/a[1]/h4'
        shop_path_a = '//*[@id="shop-all-list"]/ul/li[' + str(i) + ']/div[2]/div[1]/a/h4'
    #    print(shop_path)
    #    print(shop_path_a)
    
        title_path = '//*[@id="shop-all-list"]/ul/li[' + str(i) + ']/div[2]/div[1]'
        
        title = browser.find_element_by_xpath(title_path).text
        print(title)
        ad = ""
        if re.search("广告",title):
            ad = "+"
            print("有广告")
        
        try:
            browser.find_element_by_xpath(shop_path).click()
#            print(shop_path)
        except:
            browser.find_element_by_xpath(shop_path_a).click()
            print(shop_path_a)
    
        handles = browser.window_handles
        
        for newhandle in handles:
            # 筛选新打开的窗口
            if newhandle!=handle:
                # 切换到新打开的窗口B
                browser.switch_to_window(newhandle)
                content = browser.page_source.encode('utf-8')
                bsobj = BeautifulSoup(content, 'html5lib')
                
                name_list = bsobj.find_all("div", {"class": "basic-info default nug_shop_ab_pv-a"})
                #print(len(name_list))

                for shop_name in name_list:
                    name = shop_name.find("h1", {"class": "shop-name"}).get_text()
                    print(name)
#                    print("####")
#                    print(name.strip().split(" ")[0].strip())
                    tel = telparse(str(shop_name.find("p", {"class": "expand-info tel"})))
                    print(tel)
                    #写文件
                    with open("./huoguo.csv", "a") as f:
                        # writer 对象，修改默认分隔符为 "|"
                        writer = csv.writer(f, delimiter="|")
                        try:
                             writer.writerow([name.strip().split(" ")[0].strip(), tel.replace('电话：',"").replace('   ',","), ad])
                        except:
                              pass
                    
                    # 写数据库                                
                    dbhelper = myPymysql.DBHelper()
                    name = name.strip().split(" ")[0].strip()
                    tel = tel.replace('电话：',"")
                    sql = "INSERT INTO dinping.huoguo(name, tel, ad)VALUES(%s,%s,%s);"
                    params = (name, tel, ad)
                    result = dbhelper.execute(sql, params)
                    if result == True:
                        print("插入成功")
                    else:
#                        logger.error("execute: "+sql)
#                        logger.error("params: "+params)
                        print("插入失败")
                        
                time.sleep(5)
                # 关闭当前窗口B
                browser.close()
                #切换回窗口A
                browser.switch_to_window(handles[0])  

                
    if counte > (number-1) :
        print("总计爬取" + str(counte) + "页")
        print("结束")
        break

    print("下一页……")            
    next_page = '/html/body/div[2]/div[3]/div[1]/div[2]/a[' + str(next_index) + ']'
    again_page = '/html/body/div[2]/div[3]/div[1]/div[2]/a[' + str(next_index-1) + ']'
    try:
        browser.find_element_by_xpath(next_page).click()
        next_index += 1;
    except:
        browser.find_element_by_xpath(again_page).click()
    time.sleep(10)
    counte += 1;
#    if counte > (number-1) :
#        print(counte)
#        print("结束")
#        break

    
#browser.find_element_by_xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[1]/a[1]/h4').click()
#handles = browser.window_handles
#
#for newhandle in handles:
#    # 筛选新打开的窗口
#    if newhandle!=handle:
#        # 切换到新打开的窗口B
#        browser.switch_to_window(newhandle)
##        print(browser.find_element_by_xpath('//*[@id="basic-info"]/h1/text()'))
#        time.sleep(5)
#        # 关闭当前窗口B
#        browser.close()
#        #切换回窗口A
#        browser.switch_to_window(handles[0]) 
#        
#time.sleep(5)
#print("11111")
#browser.close()
    
browser.close()


