import csv
from http.server import executable
from select import select
import sys
from time import sleep
from unittest import skip
from selenium.webdriver.support.select import Select
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
        driver = webdriver.Chrome(ChromeDriverManager().install())

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
        for i in range(1, len(trs)):
            tds = trs[i].find_elements(By.TAG_NAME, "td")
            line = ""
            for j in range(0, len(tds)):
                if j < len(tds)-1:
                    line += "%s\t" % (tds[j].text)
                else:
                    line += "%s" %(tds[j].text)
            print(line + "\r\n")
        sleep(3)

        driver.quit()

    except ValueError:
        print('Oops! Some Error are occured.')

    return 1

if __name__ == '__main__':
    print("usage: python moneyforwardreport.py")
    sys.exit(createReport())
