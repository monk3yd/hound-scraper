import os
import time
import logging
import scrapy

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class CasetrackerSpider(scrapy.Spider):
    name = 'casetracker'

    def start_requests(self):
        # Testing need to externalize the password, pass in from pipeline # TODO
        self.rut = os.environ["MY_RUT"]
        self.password = os.environ["MY_PASS"]

        yield SeleniumRequest(
            url="https://oficinajudicialvirtual.pjud.cl/home/index.php",
            wait_time=3,
            callback=self.parse,
            screenshot=True,
        )

    def parse(self, response):
        # with open("proof_of_work.png", "wb") as file:
        #     file.write(response.meta["screenshot"])

        # Initialize browser from SeleniumRequest response
        browser = response.meta["driver"]

        # Manage Login Homepage
        dropdown_btn = browser.find_element(By.CLASS_NAME, 'dropbtn')
        dropdown_btn.click()
        time.sleep(2)

        go_to_login = browser.find_element(By.XPATH, "//div[@id='myDropdown']/a")
        go_to_login.click()
        time.sleep(2)

        # Create Selectors from html, given that the SeleniumRequest was modified by Selenium
        # html = browser.page_source
        # response_obj = Selector(text=html)

        # Mange Login Form
        rut_input = browser.find_element(By.ID, "uname")
        rut_input.send_keys(self.rut)
        time.sleep(2)

        password_input = browser.find_element(By.ID, "pword")
        password_input.send_keys(self.password)
        time.sleep(2)

        login = browser.find_element(By.ID, "login-submit")
        login.click()
        time.sleep(2)

        browser.save_screenshot("proof_of_login.png")
