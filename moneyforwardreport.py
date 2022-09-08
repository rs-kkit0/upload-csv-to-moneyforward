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

        # input form
        driver.get(reportUrl)
        sleep(3)
        elem = driver.find_elements(By.CLASS_NAME, "cf-new-btn")[1]
        elem.click()
        sleep(3)

        driver.quit()

    except ValueError:
        print('Oops! Some Error are occured.')

    return 1

if __name__ == '__main__':
    print("usage: python moneyforwardreport.py")
    sys.exit(createReport())
