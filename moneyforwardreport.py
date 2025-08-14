import math
import sys
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re

import moneyforward
from report_config import SETTLEMENT_ITEMS, FIXED_DEDUCTIONS, REPORT_SETTINGS, OUTPUT_FORMAT

class MoneyForwardReporter:
    def __init__(self, config=None):
        self.config = config or REPORT_SETTINGS
        self.driver = None
        
    def get_previous_month(self):
        today = datetime.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        return last_day_of_previous_month.strftime('%Y%m')

    def click_until_date_range(self, expected_month):
        def click_b_range():
            try:
                elem = self.driver.find_element(By.ID, "b_range")
                elem.click()
                sleep(self.config["wait_time"])
            except NoSuchElementException:
                print("b_range要素が見つかりませんでした")

        def check_date_range():
            try:
                from_to_elem = self.driver.find_element(By.CLASS_NAME, "from-to")
                return expected_month in from_to_elem.text.strip()
            except NoSuchElementException:
                return False

        while not check_date_range():
            click_b_range()

    def categorize_expenses(self, trs):
        """経費を設定に基づいて分類"""
        categorized = {key: [] for key in SETTLEMENT_ITEMS.keys()}
        
        for i in range(1, len(trs)):
            tds = trs[i].find_elements(By.TAG_NAME, "td")
            if len(tds) < 2:
                continue
                
            line = []
            line.append(tds[0].text)
            line.append(int(re.sub(r"\D", "", tds[1].text)))
            
            # 設定に基づいて分類
            for category_key, category_config in SETTLEMENT_ITEMS.items():
                if any(keyword in line[0] for keyword in category_config["keywords"]):
                    categorized[category_key].append(line)
                    break
        
        return categorized

    def calculate_settlement(self, items, divisor, rounding_type="floor"):
        """精算計算（汎用化）"""
        if not items:
            return 0, 0
            
        total = sum(item[1] for item in items)
        
        if rounding_type == "floor":
            calculated = math.floor(total / (divisor * self.config["rounding_unit"])) * self.config["rounding_unit"]
        elif rounding_type == "ceil":
            calculated = math.ceil(total / (divisor * self.config["rounding_unit"])) * self.config["rounding_unit"]
        else:  # round
            calculated = round(total / (divisor * self.config["rounding_unit"])) * self.config["rounding_unit"]
            
        return calculated, total

    def output_settlement(self, items, category_config):
        """精算項目の出力（汎用化）"""
        if not items:
            return 0
            
        name = category_config["name"]
        divisor = category_config["divisor"]
        rounding_type = category_config["rounding"]
        
        print(OUTPUT_FORMAT["item_header"].format(name=name))
        
        for item in items:
            print(item)
            
        calculated, total = self.calculate_settlement(items, divisor, rounding_type)
        
        rounding_text = "切り捨て" if rounding_type == "floor" else "切り上げ" if rounding_type == "ceil" else "四捨五入"
        print(OUTPUT_FORMAT["total_format"].format(
            name=name,
            total=total,
            calculated=calculated,
            unit=self.config["rounding_unit"],
            rounding_type=rounding_text
        ))
        
        return calculated if not category_config.get("is_deduction", False) else -calculated

    def create_report(self, param):
        """レポート作成（メイン処理）"""
        expected_month = param[:4] + "/" + param[4:]
        year = param[:4]
        month = param[4:]
        formatted_month = f"{year}年{month}月"

        try:
            # driver初期化
            self.driver = moneyforward.driverInit()
            moneyforward.login(self.driver)

            # グループ選択
            elem = self.driver.find_element(By.ID, "group_id_hash")
            select = Select(elem)
            select.select_by_visible_text(self.config["default_group"])
            sleep(self.config["wait_time"])

            # レポートページに移動
            self.driver.get(self.config["report_url"])
            sleep(self.config["wait_time"])

            # 指定月まで遷移
            self.click_until_date_range(expected_month)

            # テーブル取得と分類
            table_elem = self.driver.find_elements(By.ID, self.config["table_id"])[0]
            trs = table_elem.find_elements(By.TAG_NAME, "tr")
            categorized = self.categorize_expenses(trs)

            # 精算計算
            total = 0
            print(OUTPUT_FORMAT["header"].format(month=formatted_month))
            
            for category_key, items in categorized.items():
                category_config = SETTLEMENT_ITEMS[category_key]
                total += self.output_settlement(items, category_config)

            # 固定控除項目
            for deduction in FIXED_DEDUCTIONS:
                print(f"{deduction['name']}: {deduction['amount']:,}円")
                total -= deduction['amount']

            # 最終合計
            print(OUTPUT_FORMAT["separator"])
            print(OUTPUT_FORMAT["final_total"].format(total=total))
            print(OUTPUT_FORMAT["separator"])

            sleep(self.config["wait_time"])
            self.driver.quit()

        except Exception as e:
            print(repr(e))
            print('Oops! Some Error are occured.')
            if self.driver:
                self.driver.quit()

        return 1

def main():
    if len(sys.argv) == 2:
        param = sys.argv[1]
        if len(param) != 6 or not param.isdigit():
            print("Invalid parameter. Usage: python moneyforwardreport.py YYYYMM")
            sys.exit(1)
    else:
        reporter = MoneyForwardReporter()
        param = reporter.get_previous_month()

    reporter = MoneyForwardReporter()
    sys.exit(reporter.create_report(param))

if __name__ == '__main__':
    main()
