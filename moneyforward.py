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
 
def doUpload(input_file):
    topurl = "https://moneyforward.com/"
    inputFormUrl = "https://moneyforward.com/cf"

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

            # date info
            elem = driver.find_element(By.ID, "updated-at")
            elem.clear()
            sleep(1)
            elem.send_keys(row[0])

            # price info 
            elem = driver.find_element(By.ID, "appendedPrependedInput")
            elem.clear()
            sleep(1)
            elem.send_keys(row[2])

            # expense info
            elem = driver.find_element(By.ID, "user_asset_act_sub_account_id_hash")
            select = Select(elem)
            select.select_by_index(11)

            # 項目
            # js = 'alert("Hello World")'
            # driver.execute_script(js)

            # text info
            elem = driver.find_element(By.ID, "js-content-field")
            elem.clear()
            sleep(1)
            elem.send_keys(row[1])

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

    except ValueError:
        print('Oops! Some Error are occured.')

    return 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("no input file")
        print("usage: python moneyforward.py test.csv")
        sys.exit()
    input_file = str(sys.argv[1])
    sys.exit(doUpload(input_file))
