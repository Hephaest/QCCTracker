import time
import random
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Code.DBHelper import DBHelper


class Task1Spider:
    def __init__(self, driver, wait):
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.driver = driver
        self.wait = wait
        self.helper = DBHelper()
        self.check_funding_company()
        # self.find_company_by_name()

    def find_company_by_name(self):
        c_name_list = self.helper.get_companies()
        for c_name in c_name_list:
            name = c_name[0]
            print("======start find_company_by_name ===========")
            time.sleep(random.randint(10, 20))
            self.driver.get("https://www.qcc.com/web/search?key=" + name)
            self.check_company_title(name)

    def check_company_title(self, name):
        company_block = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="maininfo"]')))
        # Check the 1st one
        name_test = company_block.find_element_by_xpath('.//a[@class="title"]//span').text

        # Simple check
        if name == name_test:
            # Get company url
            detail_url = company_block.find_element_by_xpath(".//a[@class='title']").get_attribute("href")
            self.helper.set_company_url(name, detail_url)
            # Check funding company
            c_id = str(self.helper.get_company_id(name)[0][0])
            self.find_funding_company(company_block, detail_url, c_id)
        else:
            print("Not match")

    def find_funding_company(self, element, url, c_id):
        try:
            print("======start funding_company_name ===========")
            funding_company_name = element.find_element_by_xpath(".//span[@class='hit-reasons']//span[contains(text(),'投资机构')]").text
            # If it exists
            time.sleep(random.randint(8, 10))
            self.driver.get(url)

            funding_company_url = self.wait.until(EC.presence_of_element_located((By.XPATH,  "//span[contains(text(),'投资机构')]/ancestor::a"))).get_attribute("href")
            self.helper.set_funding_info(funding_company_name, funding_company_url, c_id)
        except:
            print("No funding company")

    def check_funding_company(self):
        company_list = self.helper.get_not_found_funding_company_name()
        for company_info in company_list:
            try:
                name = company_info[0]
                time.sleep(random.randint(10, 15))
                self.driver.get("https://www.qcc.com/elib_investfirm?elibkey=" + name)
                time.sleep(random.randint(8, 10))
                tds = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table[@class='ntable']//tr//td")))
                td_name = tds[2].text
                if name != td_name:
                    print("name: " + name + "But found: " + td_name)
                    continue
                url = tds[2].find_element_by_xpath(".//a").get_attribute("href")
                field = tds[3].text
                date = tds[4].text
                region = tds[5].text
                self.helper.set_firm_info(name, url, field, date, region)
            except:
                print("Weird!")


