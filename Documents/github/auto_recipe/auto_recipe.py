# Coding: UTF-8

### レシピ抽出 ###

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

count = 0

#CSV操作
f = open("cookpad_data1.csv","a")
writer = csv.writer(f, lineterminator="\n")

# WebDriver起動
driver = webdriver.Chrome()
query = "ドリアン"
driver.get("https://cookpad.com/search/" + query)

#クローリング
while True:
    for i in range(len(driver.find_elements_by_css_selector(".recipe-preview"))):
        driver.find_element_by_xpath("//*[@id='recipe_" + str(i) +"']//*[contains(@class,'recipe-title')]").click()
        #スクレイピング準備
        req = 0
        res = 0
        html = 0
        soup = 0
        csv_list = []
        quant_list = []
        order_list = []
        
        #10秒は待ってやる
        driver.set_page_load_timeout(10)
        #現在のURL取得
        url = driver.current_url
        #リクエストのための身分証明
        req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        #リクエストするURLを開く
        res = urlopen(req)
        html = res.read()
        soup = BeautifulSoup(html,"html.parser")

        #タイトル抽出
        recipe_main = soup.find("div", attrs={"id": "recipe-main"})
        recipe_title = recipe_main.find("h1", attrs={"class": "recipe-title fn clearfix"})
        csv_list.append(recipe_title.string)

        #素材抽出
        for ingredient in recipe_main.findAll("div", attrs={"class": "ingredient_name"}):
            csv_list.append(ingredient.text)
        for quantity in recipe_main.findAll("div", attrs={"class":"ingredient_quantity amount"}):
            quant_list.append(quantity.text)
        for i in range(len(quant_list)):
            csv_list[i + 1] += " " + quant_list[i]

        #作り方抽出
        order_list.append("作り方")
        recipe_steps = soup.find("div", attrs={"id": "steps"})

        for step in recipe_steps.findAll("div", attrs={"class": "step"}):
            order_list.append(step.text)

        #CSV書き出し
        writer.writerow(csv_list)
        writer.writerow(order_list)
        driver.set_page_load_timeout(10)
        
        driver.back()
        
    if len(driver.find_elements_by_css_selector(".next_page"))>0:
        url = driver.find_element_by_css_selector("a.next_page").get_attribute("href")
        driver.get(url)
        count += 1
        #driver.find_elements_by_css_selector(".next_page").click()
    else:
        print("no pager exist anymore")
        print(count)
        break

f.close()
driver.quit()