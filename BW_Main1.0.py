import requests
import time
from time import sleep
import csv
import os
import sys
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import string
from bs4 import BeautifulSoup
import urllib.request as req
import BW_article_part1_1

#紀錄執行時間
timeArray = time.localtime(int(time.time()))
exetime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
with open("exetime.txt","a+") as exetxt:
    exetxt.write(exetime+"\n")
    exetxt.close()


ua = UserAgent()
#主頁面
url_main = "https://www.businessweekly.com.tw/"

#分頁面
#最新，國際，財經，管理，職場，生活
url_board_set = ["https://www.businessweekly.com.tw/latest",
                "https://www.businessweekly.com.tw/channel/international/0000000316",
                "https://www.businessweekly.com.tw/channel/business/0000000319",
                "https://www.businessweekly.com.tw/channel/management/0000000326",
                "https://www.businessweekly.com.tw/channel/careers/0000000331",
                "https://www.businessweekly.com.tw/channel/style/0000000337"]

#抓取.py路徑
address = str(os.path.dirname(os.path.abspath(__file__))) + "\\"



for url_board in url_board_set:
    #處理下拉式頁面-----------------------------------------------------

    #隨機選擇 User Agent
    opts = Options()
    opts.add_argument("user-agent=" + ua.chrome)
    driver = webdriver.Chrome(chrome_options=opts)
    driver.get(url_board) #最新文章頁面
    
    sleep(3)
    #driver.implicitly_wait(3)
    
    for i in range(0,5):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") #JS的下拉指令
        print(i)
    #driver.implicitly_wait(3)
    sleep(5)    #使頁面充份讀入
    print("----------------------------------------------------------------------------")

    print("當前網站: " + url_board)
    
    agent = driver.execute_script("return navigator.userAgent")
    print("ua: " + agent)

    # 抓取網頁原始碼-------------------------------------------------------------------------------------------------
    print("1")
    latest_code = driver.page_source.encode("utf-8")
    print("2")
    root = BeautifulSoup(latest_code,"html.parser")
    
 
    #載入.csv並記錄之前的URL--------------------------------------------------------------------------------------------
    with open(address + "BW.csv", newline="",encoding="utf-8-sig") as csvFile:
        dic_BW = csv.DictReader(csvFile)#將.csv轉成dictionary
        url_vector = [row["URL"] for row in dic_BW] #將所有"URL" 存入rul_vector

    #尋找文章之url，並呼叫BW_article_part中的gettxt
    url_set = root.find_all("div", class_="Article-content d-xs-flex")
    print("抓取url數量: " + str(len(url_set)))

    for div in url_set:
        if( (div.a["href"][0:5] != "https") and div.a["href"][0:5] != "" ): #過濾掉"商業雜誌"的文章
            article_url = url_main + div.a["href"]  #url_set[0].a["href"]   =>  div 下的 a 的 href
            #檢查是否重複(article_exist = True ==> 文章存在)
            for urlhis in url_vector:
                
                if(article_url == urlhis):
                    article_exist = True
                    break
                else:
                    article_exist = False
                    

            #呼叫BW_article_part
            if(not article_exist):
                print(article_url)
                #BW_article_part.getcontent(article_url)
    
    #關閉driver
    driver.close() 
    driver.quit()
    sleep(10)

print("程式有跑完")