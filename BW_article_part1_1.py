import requests
import json,time,string,re,os,csv
from os.path import isfile, isdir, join
from os import listdir
import codecs
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as req

#新增月份.csv
def newcsv ( address , mouth ):
    with open(address + mouth +".csv", "w", newline='',encoding="utf-8-sig") as csvFile:
        writer = csv.writer(csvFile)
        #寫出-標題(first time)
        writer.writerow(['URL','公司',"sponsor",'版','標題','時間','描述','內容'])


# url = article's net
def getcontent( url ):
    address = str(os.path.dirname(os.path.abspath(__file__))) + "\\Data\\"
    nothing = False 
    #Ture ==> 沒有資料
    #False ==> 有資料

    # 抓取網頁原始碼---------------------------------------------------------------------------------------------------------------------------------------
    with req.urlopen(url) as response:
        data = response.read().decode("utf-8")

    # 取得文章標籤-----------------------------------------------------------------------------------------------------------------------------------------
    root = bs4.BeautifulSoup(data, "html.parser")

    # 將原始碼存入txt中------------------------------------------------------------------------------------------------------------------------------------
    # with open("fuck.txt","w",encoding="utf-8") as fuck:
    #     fuck.write(str(root.prettify()))
    #     fuck.close()
    # print(root.title.string)    #root:原始檔 title:標籤 string:內部字串

    # 搜尋出 "script" 且 type = "application/ld+json" 的資料
    json_set = root.find_all("script", type="application/ld+json")
    # json_set 為一set格式
    
    #確認格式是否符合---------------------------------------------------------------------------------------------------------------------------------------
    if(json_set):
        json_data = json.loads(json_set[1].string,strict=False)  # 將json_set[1]裡面的內容轉為josn格式    strict=False ==> 非嚴格模式的json
        # json_set[1].text為script tag內的文字
        date = json_data["dateCreated"]

        #整理時間格式
        date = date.replace("/","年",1)
        date = date.replace("/","月",1)
        date = date.replace("/","日",1)
        for i in range(len(date)):
            if(date[i] == "日"):
                date = date[0:i+1] + " " + date[i+1:len(date)]
                break

        #是否為sponsor(贊助)----------------------------------------------------------------------------------------------------------------------------
        spon = root.find("div",class_="Tag-sponsor")
        if(spon):
            sponsor = "V"
        else:
            sponsor = ""

        #抓出月份   xxxx年xx月
        mouth = date[:date.index("月")+1]
        #將Data內的.csv檔列出來(list)
        files = listdir(str(os.path.dirname(os.path.abspath(__file__))) + "\\Data\\")

        if mouth+".csv" in files:
            None
        else:
            newcsv( address , mouth )

        #載入.csv並記錄之前的URL--------------------------------------------------------------------------------------------
        with open(address + mouth +".csv", newline="",encoding="utf-8-sig") as csvFile:
            dic_BW = csv.DictReader(csvFile)#將.csv轉成dictionary
            url_vector = [row["URL"] for row in dic_BW] #將所有"URL" 存入rul_vector

        #檢查是否重複(article_exist = True ==> 文章存在)        
        article_exist = False
        for urlhis in url_vector:

            if(url == urlhis):
                article_exist = True
                break
            else:
                article_exist = False

    else:
        nothing = True
        print("json is nothing")
    
    
        
    # 開啟輸出的 CSV 檔案--------------------------------------------------------------------------------------------------------------------------------
    if( (not nothing) and (not article_exist) ):
        print("write:" + url)
        # utf-8-sig ===> 解決亂碼
        with open(address + mouth +".csv", "a+", newline='',encoding="utf-8-sig") as csvFile:
            # 建立 CSV 檔寫入器
            writer = csv.writer(csvFile)

            #寫出-標題(first time)
            #writer.writerow(['URL','公司',"sponsor",'版','標題','時間','描述','內容'])

            #寫出-資料
            writer.writerow([url,"商業週刊",sponsor,json_data["articleSection"],json_data["headline"],date,json_data["description"],json_data["articleBody"]])
            

