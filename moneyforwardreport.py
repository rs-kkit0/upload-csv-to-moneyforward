import math
import sys
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import moneyforward

def get_previous_month():
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_previous_month.strftime('%Y%m')

def click_until_date_range(driver, expected_month):
    def click_b_range():
        try:
            elem = driver.find_element(By.ID, "b_range")
            elem.click()
            sleep(3)  # ページが更新されるのを待つ
        except NoSuchElementException:
            print("b_range要素が見つかりませんでした")

    def check_date_range():
        try:
            from_to_elem = driver.find_element(By.CLASS_NAME, "from-to")
            return expected_month in from_to_elem.text.strip()
        except NoSuchElementException:
            return False

    while not check_date_range():
        click_b_range()

def createReport(param):
    reportUrl = "https://moneyforward.com/cf/summary"
    expected_month = param[:4] + "/" + param[4:]

    year = param[:4]
    month = param[4:]
    formatted_month = f"{year}年{month}月"


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

        # 指定した月の値まで遷移する
        click_until_date_range(driver, expected_month)

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
        
        print(f"*** {formatted_month}分 精算 ***")
        total += output(one_third, 3)
        total += output(one_second, 2)
        total += output(one_one, 1)
        total -= output(tatekae, 2, True)

        # TODO 抽象化する
        print("育児手当: 20,000円")
        total -= 20000
        print("児童手当等支給分: 20,000円")
        total -= 20000
        print("お弁当代: 8,000円")
        total -= 8000
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
    if len(sys.argv) == 2:
        param = sys.argv[1]
        if len(param) != 6 or not param.isdigit():
            print("Invalid parameter. Usage: python moneyforwardreport.py YYYYMM")
            sys.exit(1)
    else:
        param = get_previous_month()

    sys.exit(createReport(param))
