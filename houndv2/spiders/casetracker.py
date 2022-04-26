import os
import scrapy
import logging
import time

from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from scrapy.utils.log import configure_logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


class CasetrackerSpider(scrapy.Spider):
    name = 'casetracker'
    first_parse = True

    # Create log
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='houndv2.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def start_requests(self):
        # TODO - Implemet on main. Set up credentials from env variables 
        self.rut = os.environ["MY_RUT"]
        self.password = os.environ["MY_PASS"]

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


        # Run just the first time
        if self.first_parse:
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
            print(self.all_tracking_data)

        # Loop through all cases
        # Competencia
        competencia_dropdown = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "competencia"))
        )
        competencia_dropdown.click()
        competencia = Select(competencia_dropdown)
        competencia.select_by_visible_text(f"{self.all_tracking_data[0]['COMPETENCIA']}")

        # Corte
        corte_dropdown = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "conCorte"))
        )
        corte_dropdown.click()
        corte = Select(corte_dropdown)
        corte.select_by_visible_text(f"C.A. de {self.all_tracking_data[0]['CORTE']}")

        # Rol
        rol_input = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "conRolCausa"))
        )
        rol_input.clear()
        rol_input.send_keys(self.all_tracking_data[0]["ROL"])

        # Year
        year_input = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "conEraCausa"))
        )
        year_input.clear()
        year_input.send_keys(self.all_tracking_data[0]["AÑO"])
        year_input.click()

        browser.implicitly_wait(3)

        # Tipo/Libro
        tipo_dropdown = WebDriverWait(browser, timeout=10).until(
            EC.presence_of_element_located((By.ID, "conTipoCausa"))
        )
        tipo_dropdown.click()
        tipo = Select(tipo_dropdown)
        tipo.select_by_visible_text(self.all_tracking_data[0]["TIPO"])


        # General search
        search_btn = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.ID, "btnConConsulta"))
        )
        search_btn.click()

        # Details search
        case_details = WebDriverWait(browser, timeout=10).until(
            EC.element_to_be_clickable(browser.find_element(By.XPATH, "//a[@title='Detalle de la causa']"))
        )
        case_details.click()

        time.sleep(3)

        # Get html for scrapy
        html = browser.find_element(By.XPATH, "//*[@id='movimientosApe']/div/div/table").get_attribute('outerHTML')
        resp = Selector(text=html)  # response_obj = Selector(text=browser.page_source)

        # if not self.scraped_headers:
        #     self.scraped_headers = True
        #     # Get table headers
        #     all_headers = resp.xpath("//thead/tr/th")
        #     for header in all_headers:
        #         yield {
        #             "header": header.xpath(".//text()").get(),
        #         }

        # Get table data
        table_rows = resp.xpath("//tbody/tr")
        for data in table_rows:
            # Extract doc url
            action = data.xpath(".//td[2]/form/@action").get()
            value = data.xpath(".//td[2]/form/input/@value").get()
            doc_url = f"https://oficinajudicialvirtual.pjud.cl/{action}?valorDoc={value}"

            yield {
                "folio": data.xpath(".//td[1]/text()").get(),
                "doc": doc_url,
                # "anexo": data.xpath(".//td[3]/text()").get(),
                "tramite": data.xpath(".//td[4]/text()").get(),
                "descripcion": data.xpath(".//td[5]/span/text()").get(),
                "fecha": data.xpath(".//td[6]/text()").get(),
                "sala": data.xpath(".//td[7]/text()").get(),
                "estado": data.xpath(".//td[8]/text()").get(),
                # "georef": data.xpath(".//td[9]/text()").get()
            }

        # Back to Details search

        # Proof of work
        browser.save_screenshot("proof_of_work.png")

# ADIR_871/apelaciones/documentos/docCausaApelaciones.php?valorDoc=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvb2ZpY2luYWp1ZGljaWFsdmlydHVhbC5wanVkLmNsIiwiYXVkIjoiaHR0cHM6XC9cL29maWNpbmFqdWRpY2lhbHZpcnR1YWwucGp1ZC5jbCIsImlhdCI6MTY1MDk2MzkwNywiZXhwIjoxNjUwOTY3NTA3LCJkYXRhIjp7ImNycl9kb2MiOiIyOTE3MzE4MiIsImNvZF9jb3J0ZSI6IjI1IiwiY3JySWREb2NFc2MiOiIzMjU5MzYwMiIsImNvZF90aXBhcmNoaXZvIjoiMyIsInRyYW1pdGUiOjB9fQ.XNp7aVdukyzDlc5aj5PSiJQBY_vaPH2OjfAZVx45mh0