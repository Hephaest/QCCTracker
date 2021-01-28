import requests
from Code.Task1Spider import Task1Spider
from Code.Task2Spider import Task2Spider
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class LoginCracker:

    def __init__(self, username, password, driver, wait):
        self.driver = driver
        self.wait = wait
        self.username = username
        self.password = password

    def login_with_slider(self):
        try:
            # Get the slider
            slide = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='nc_iconfont btn_slide']")))
            slide_width = int(slide.value_of_css_property('width').replace('px', ''))

            # Get slider background
            slide_bkg = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='scale_text slidetounlock']")))
            slideBkg_width = int(slide_bkg.value_of_css_property('width').replace('px', ''))

            # Get distance
            distance = slideBkg_width - slide_width

            # Move slide
            time.sleep(3)
            ActionChains(self.driver).click_and_hold(slide).perform()
            time.sleep(1)
            ActionChains(self.driver).move_by_offset(xoffset=distance, yoffset=0).perform()

            # Release mouse
            time.sleep(0.1)
            ActionChains(self.driver).release().perform()
            time.sleep(3)

            try:
                pass_logo = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='nc_iconfont btn_ok']")))
                print("success")
                submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary btn-block m-t-lg login-btn']")))
                submit_button.click()
                time.sleep(5)

                # Call Task 1 spider
                Task1Spider(self.driver, self.wait)
                # Call Task 2 spider
                # Task2Spider(self.driver, self.wait)
            except:
                error_hint = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "刷新")))
                print("error")
                error_hint.click()
                time.sleep(3)
                self.login_with_slider()
        except:
            print("Error occurs")
            self.driver.refresh()
            self.login()

    def click_submit(self):
        try:
            # Enter user phone number & password
            username_input = self.driver.find_element_by_id('nameNormal')
            password_input = self.driver.find_element_by_id('pwdNormal')

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)

            self.login_with_slider()
        except:
            print("Error occurs")
            self.driver.refresh()
            self.click_submit()

    def login(self):
        try:
            return self.click_submit()
        except requests.exceptions.ConnectionError:
            self.driver.close()
            return "HTTP Error"
