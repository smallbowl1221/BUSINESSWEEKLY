import requests
import json,time,string,re,os,csv
import codecs
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request as req

address = str(os.path.dirname(os.path.abspath(__file__))) + "\\Data\\"

# url = article's net
def getcontent( url ):

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
        print("json_set have something")
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

    else:
        nothing = True
        print("nothing")
    
    # 開啟輸出的 CSV 檔案--------------------------------------------------------------------------------------------------------------------------------
    if(nothing != True):

        #抓取.py路徑
        address = str(os.path.dirname(os.path.abspath(__file__))) + "\\"
        # utf-8-sig ===> 解決亂碼
        with open(address + "BW.csv", "a+", newline='',encoding="utf-8-sig") as csvFile:
        # 建立 CSV 檔寫入器
            #csvFile.write(codecs.BOM_UTF8)
            writer = csv.writer(csvFile)

            #寫出-標題(first time)
            #writer.writerow(['URL','公司',"sponsor",'版','標題','時間','描述','內容'])

            #寫出-資料
            writer.writerow([url,"商業週刊",sponsor,json_data["articleSection"],json_data["headline"],date,json_data["description"],json_data["articleBody"]])
            
            