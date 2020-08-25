import requests
import time
from time import sleep
import string,csv
import os,sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
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

#設定每一次的
url_board = url_board_set[int(sys.argv[1])]


#處理下拉式頁面-----------------------------------------------------

#隨機選擇 User Agent
opts = Options()
opts.add_argument("user-agent=" + ua.chrome)
driver = webdriver.Chrome(chrome_options=opts)
driver.get(url_board) #最新文章頁面
#driver.implicitly_wait(3)
sleep(3)

for i in range(0,5):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") #JS的下拉指令
    print(i)
sleep(5)    #使頁面充份讀入

print("----------------------------------------------------------------------------")
print("當前網站: " + url_board)

#agent = driver.execute_script("return navigator.userAgent")
#print("ua: " + agent)

# 抓取網頁原始碼-------------------------------------------------------------------------------------------------
print("driver to utf-8")
latest_code = driver.page_source.encode("utf-8")

print("use bs4 deal with html")
root = BeautifulSoup(latest_code,"html.parser")


#尋找文章之url，並呼叫BW_article_part中的gettxt
url_set = root.find_all("div", class_="Article-content d-xs-flex")
print("抓取url數量: " + str(len(url_set)))


for div in url_set:
    #過濾掉"商業雜誌"的文章
    if( (div.a["href"][0:5] != "https") and div.a["href"][0:5] != "" ):
        article_url = url_main + div.a["href"]  #url_set[0].a["href"]   =>  div 下的 a 的 href
        print( "deal with url :" + article_url + "---------------------------------------------------------------------")
        BW_article_part1_1.getcontent(article_url)

#關閉driver
driver.close() 
driver.quit()

print("程式有跑完")
#緩衝一下
sleep(10)