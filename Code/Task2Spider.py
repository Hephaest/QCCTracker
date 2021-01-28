import time
import random
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Code.DBHelper import DBHelper


class Task2Spider:
    def __init__(self, driver, wait):
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.driver = driver
        self.wait = wait
        self.helper = DBHelper()
        self.find_firm_by_page()

    def find_firm_by_page(self):
        page_index = 1
        while page_index < 501:
            print("====== broswer new page ===========")
            time.sleep(random.randint(5, 10))
            self.driver.get("https://www.qcc.com/elib_investfirm_p_" + str(page_index) +".html")
            time.sleep(random.randint(10, 20))
            self.find_firm_info()
            page_index += 1

    def find_firm_info(self):
        # Remove title row
        item_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='ntable']//tr")))[1:]
        for item in item_list:
            item_col_list = item.find_elements_by_xpath('.//td')
            name   = item_col_list[2].text
            url    = item_col_list[2].find_element_by_xpath(".//a").get_attribute("href")
            field  = item_col_list[3].text
            date   = item_col_list[4].text
            region = item_col_list[5].text
            self.helper.set_firm_info(name, url, field, date, region)