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

import moneyforward
 
def createReport():
    reportUrl = "https://moneyforward.com/cf/summary"

    try:
        # driver
        driver = moneyforward.driverInit()

        # login
        moneyforward.login(driver)

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
        tatekae = []

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
            if "立替" in line[0]:
                tatekae.append(line)

        total = 0
        print("*************************")
        total += output(one_third, 3)
        total += output(one_second, 2)
        total += output(one_one, 1)
        total -= output(tatekae, 2, True)

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

def output(list: list, val: int, flg = False) -> int:
    if (flg):
        temp = "立替清算 1/"+ str(val) + "負担"
        print("*** " + temp + " ***")
    else:
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
