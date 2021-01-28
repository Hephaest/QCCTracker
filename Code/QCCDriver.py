from selenium import webdriver
from Code.LoginCracker import LoginCracker
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class QCCDriver:
    def __init__(self, phoneNum, password):
        chrome_drive = r"/Users/hephaest/chromedriver"
        hompage_url = "https://www.qcc.com/"

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.username = phoneNum
        self.password = password
        self.driver = webdriver.Chrome(executable_path=chrome_drive, options=options)

        self.wait = WebDriverWait(self.driver, 30, 10)
        self.driver.get(hompage_url)
        self.on_click()

    def on_click(self):
        try:
            # click the navi button
            login_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "navi-btn")))
            login_btn.click()
            time.sleep(3)

            # Click normal login button
            normal_login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "normalLogin")))
            normal_login_button.click()
            time.sleep(3)

            # Call LoginCracker
            LoginCracker(self.username, self.password, self.driver, self.wait).login()
        except:
            print("Error occurs")


phoneNum = "phone"
password = "pwd"
QCCDriver(phoneNum, password)
