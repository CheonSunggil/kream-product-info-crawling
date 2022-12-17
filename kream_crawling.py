import pandas as pd
from bs4 import BeautifulSoup as 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import requests
from tqdm import tqdm

def down_scroll(browser):
    scroll_location = browser.execute_script("return document.body.scrollHeight")
    print(scroll_location)
    for i in tqdm(range(300)) :
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(2)

        scroll_height = browser.execute_script("return document.body.scrollHeight")
        
        if scroll_location == scroll_height:
            break

        else:
            scroll_location = browser.execute_script("return document.body.scrollHeight")
    return browser

def extract_info(product_list):
    brand_list = list()
    name_list = list()
    price_list = list()
    wish_cnt_list = list()
    review_cnt_list = list()
    for product in product_list :
        text_list = product.find_all(text=True)
        brand = text_list[4]
        name = text_list[7]
        price = text_list[10]
        wish_cnt = text_list[12]
        review_cnt =text_list[13]

        brand_list.append(brand)
        name_list.append(name)
        price_list.append(price)
        wish_cnt_list.append(wish_cnt)
        review_cnt_list.append(review_cnt)
    info_df = pd.DataFrame({'brand': brand_list, 'name':name_list, 'price' : price_list, 'wish' : wish_cnt_list, 'review' : review_cnt_list})
    
    return info_df

if __name__ == "__main__" :
    
    category_list = ['shoes','clothes', 'fashion', 'stuff', 'life','tech']
    url_list = ['https://kream.co.kr/search?category_id=34&per_page=40',
                'https://kream.co.kr/search?category_id=2&per_page=40',
                'https://kream.co.kr/search?category_id=7&per_page=40',
                'https://kream.co.kr/search?category_id=15&per_page=40',
                'https://kream.co.kr/search?category_id=11&per_page=40']

    product_info = pd.DataFrame()
    for category, url in zip(tqdm(category_list), url_list) :
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') # 창 새로 띄우는 것 없이
        options.add_argument('--disable-gpu') # gpu 사용안하겠다 괜한 오류나오니깐

        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        browser.get(url)

        browser = down_scroll(browser)
        soup = BeautifulSoup(browser.page_source,'lxml')
        product_list = soup.find_all('div', class_= 'product_card')


        update_info = extract_info(product_list)
        update_info['category']=category
        product_info = pd.concat([product_info, update_info])
    
    product_info.to_csv("kream_product_info.csv", index=False)