import os
import scrapy

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class CasetrackerSpider(scrapy.Spider):
    name = 'casetracker'

    def start_requests(self):
        # Set up credentials from env variables 
        self.rut = os.environ["MY_RUT"]
        self.password = os.environ["MY_PASS"]
        self.first_parse = True

        # TODO - Secure the password

        yield SeleniumRequest(
            url="https://oficinajudicialvirtual.pjud.cl/home/index.php",
            wait_time=3,
            callback=self.parse,
            screenshot=True,
        )

    def parse(self, response):
        # Initialize browser from SeleniumRequest response
        browser = response.meta["driver"]

        # TODO - Stealth browser
        # if self.first_parse:
        self.first_parse = False

        # Intro homepage
        dropdown_btn = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.CLASS_NAME, 'dropbtn')))
        dropdown_btn.click()

        goto_login = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.XPATH, "//div[@id='myDropdown']/a")))
        goto_login.click()

        # TODO - randomize implicit wait
        browser.implicitly_wait(3)

        # Login Form
        rut_input = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "uname")))
        rut_input.send_keys(self.rut)

        password_input = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "pword")))
        password_input.send_keys(self.password)

        login = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "login-submit")))
        login.click()
        
        # Search page (consulta unificada)
        goto_search = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.XPATH, "//a[@onclick='consultaUnificada();']"))
        )
        goto_search.click()

        # TODO - randomize implicit wait
        browser.implicitly_wait(3)
        
        # RIT search page form. Get all search parameter elements
        # competencia_dropdown_element = WebDriverWait(browser, timeout=10).until(
        #     EC.element_to_be_clickable(browser.find_element(By.ID, "competencia"))
        # )
        # corte_dropdown = WebDriverWait(browser, timeout=10).until(
        #     EC.element_to_be_clickable(browser.find_element(By.ID, "conCorte"))
        # )
        # rol_input = WebDriverWait(browser, timeout=10).until(
        #     EC.element_to_be_clickable(browser.find_element(By.ID, "conRolCausa"))
        # )
        # year_input = WebDriverWait(browser, timeout=10).until(
        #     EC.element_to_be_clickable(browser.find_element(By.ID, "conEraCausa"))
        # )
        # tipo_dropdown = WebDriverWait(browser, timeout=10).until(
        #     EC.element_to_be_clickable(browser.find_element(By.ID, "conTipoCausa"))
        # )
        # search_btn = WebDriverWait(browser, timeout=10).until(
        #     EC.element_to_be_clickable(browser.find_element(By.ID, "btnConConsulta"))
        # )

        # Proof of work
        browser.save_screenshot("proof_of_login.png")
