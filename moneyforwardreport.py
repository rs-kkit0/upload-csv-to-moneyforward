import csv
from http.server import executable
import math
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
 
def createReport():
    topurl = "https://moneyforward.com/"
    reportUrl = "https://moneyforward.com/cf/summary"

    user = settings.user
    password = settings.password

    try:
        # driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')                 # headlessモードを使用する
        options.add_argument('--disable-gpu')              # headlessモードで暫定的に必要なフラグ(そのうち不要になる)
        options.add_argument('--disable-extensions')       # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
        options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
        options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
        options.add_argument('--start-maximized')          # 起動時にウィンドウを最大化する
        options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

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

        # group
        elem = driver.find_element(By.ID, "group_id_hash")
        select = Select(elem)
        select.select_by_visible_text("グループ選択なし")
        sleep(3)

        # report url
        driver.get(reportUrl)
        sleep(3)

        # 前月に移動している
        # todo
        # 指定した月の値まで遷移するようにしたい 
        elem = driver.find_element(By.ID, "b_range")
        elem.click()
        sleep(3)

        # get table
        tableElem = driver.find_elements(By.ID, "table-outgo")[0]
        trs = tableElem.find_elements(By.TAG_NAME, "tr")
        one_third = []
        one_second = []
        one_one = []
        for i in range(1, len(trs)):
            tds = trs[i].find_elements(By.TAG_NAME, "td")
            line = []
            line.append(tds[0].text)
            import re
            line.append(int(re.sub(r"\D", "", tds[1].text)))
            if "水道・光熱費 合計" in line[0]:
                one_third.append(line)
            if "家賃" in line[0]:
                one_third.append(line)
            if "割勘" in line[0]:
                one_second.append(line)
            if "えり負担" in line[0]:
                one_one.append(line)

        total = 0
        print("*************************")
        total += output(one_third, 3)
        total += output(one_second, 2)
        total += output(one_one, 1)

        print("家事手当: 30,000円")
        total -= 30000
        print("*************************")
        print("*** 請求合計: " + "{:,}".format(total) + "円 ***")
        print("*************************")

        sleep(3)

        driver.quit()

    except Exception as e:
        print(repr(e))
        print('Oops! Some Error are occured.')

    return 1

def output(list: list, val: int) -> int:
    temp = "1/"+ str(val) + "負担"
    print("*** " + temp + " ***")
    total = 0
    for i in list:
        print(i)
        total += i[1]
    
    calc = math.floor(total / (val * 1000)) * 1000
    print(temp + " 合計: "+ "{:,}".format(total) + " => " + "{:,}".format(calc) + "(1,000以下切捨て)")
    return calc
 
if __name__ == '__main__':
    print("usage: python moneyforwardreport.py")
    sys.exit(createReport())
