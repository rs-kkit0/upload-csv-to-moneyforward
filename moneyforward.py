import csv
from http.server import executable
from select import select
import sys
from time import sleep
from unittest import skip
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import settings

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
 
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests

import mapping

def driverInit():
    # driver
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    options = Options()
    options.add_argument('--headless')# ヘッドレス起動
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')# SSLエラー対策
    options.add_argument('--disable-blink-features=AutomationControlled')# webdriver検出を回避
    options.add_argument('--blink-settings=imagesEnabled=false')# 画像非表示
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    ## 最新のバージョンのChromeドライバーを取得する
    try:
        driver_path = ChromeDriverManager().install()
        return webdriver.Chrome(executable_path=driver_path, options=options)
    except ValueError:
        # ValueErrorが発生した場合、バージョンを指定してインストール
        driver_path = ChromeDriverManager(version=response.text).install()
        return webdriver.Chrome(executable_path=driver_path, options=options)

def login(driver):
    topurl = "https://moneyforward.com/"

    user = settings.user
    password = settings.password

    # login
    driver.implicitly_wait(20)
    driver.get(topurl)
    sleep(3)
    elem = driver.find_elements(By.LINK_TEXT, "ログイン")
    elem[0].click()
    sleep(3)
    elem = driver.find_elements(By.LINK_TEXT, "メールアドレスでログイン")
    elem[0].click()

    elem = driver.find_element(By.NAME, "mfid_user[email]")
    elem.clear()
    elem.send_keys(user)
    elem.submit()
    sleep(3)
    elem = driver.find_element(By.NAME, "mfid_user[password]")
    elem.clear()
    elem.send_keys(password)
    elem.submit()
    sleep(3)

    # 生体認証確認スキップ
    elem = driver.find_elements(By.LINK_TEXT, "スキップする")
    elem[0].click()
    sleep(3)

def doUpload(input_file):
    inputFormUrl = "https://moneyforward.com/cf"

    try:
        # driver
        driver = driverInit()

        # login
        login(driver)

        # group
        elem = driver.find_element(By.ID, "group_id_hash")
        select = Select(elem)
        select.select_by_visible_text("グループ選択なし")
        sleep(3)

        # input form
        driver.get(inputFormUrl)
        sleep(3)
        elem = driver.find_elements(By.CLASS_NAME, "cf-new-btn")[1]
        elem.click()
        sleep(3)

        # open
        f = open(input_file, mode='r', encoding='utf-8')
        reader = csv.reader(f)
        count = 1

        for row in reader:
            sleep(1)
            print(row)
            # header skip
            if count == 1:
                count += 1
                continue

            # price info 
            elem = driver.find_element(By.ID, "appendedPrependedInput")
            elem.clear()
            sleep(1)
            elem.send_keys(row[2])

            # expense info
            elem = driver.find_element(By.ID, "user_asset_act_sub_account_id_hash")
            select = Select(elem)
            select.select_by_index(12)

            # 分類、区分が設定されている場合大項目と中項目の設定を行う
            if len(row) >= 5 and row[3] and row[4]:
                key = (row[3], row[4])
                if key in mapping.category_mapping:
                    ids = mapping.category_mapping(key)
                    # 大項目
                    elem = driver.find_element(By.ID, "js-large-category-selected")
                    elem.click()
                    sleep(1)
                    elem = driver.find_element(By.ID, ids["large_category_id"])
                    elem.click()
                    sleep(1)

                    # 中項目
                    elem = driver.find_element(By.ID, "js-middle-category-selected")
                    elem.click()
                    sleep(1)
                    elem = driver.find_element(By.ID, ids["middle_category_id"])
                    elem.click()
                    sleep(1)

            # text info
            elem = driver.find_element(By.ID, "js-content-field")
            elem.clear()
            sleep(1)
            elem.send_keys(row[1])

            # date info
            elem = driver.find_element(By.ID, "updated-at")
            elem.clear()
            sleep(1)
            elem.send_keys(row[0])

            #save
            sleep(1)
            elem = driver.find_element(By.NAME, "commit").click()
            sleep(1)
            # WebDriverWait(driver, 20).until(
            #         EC.presence_of_element_located((By.ID, "confirmation-button"))
            # )
            sleep(1)
            elem = driver.find_element(By.ID, "confirmation-button").click()

            # next
            # sleep(1)
            # WebDriverWait(driver, 20).until(
            #         EC.presence_of_element_located((By.ID, "submit-button"))
            # )
            # sleep(1)
            # WebDriverWait(driver, 20).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, "plus-payment"))
            # )

        f.close()
        print("EOF: " + input_file)
        driver.quit()

    except Exception as e:
         print(f"{e.__class__.__name__}: {e}")

    return 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("no input file")
        print("usage: python moneyforward.py test.csv")
        sys.exit()
    input_file = str(sys.argv[1])
    sys.exit(doUpload(input_file))
