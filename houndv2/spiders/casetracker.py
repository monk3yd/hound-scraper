import logging
import scrapy

from scrapy_selenium import SeleniumRequest


class CasetrackerSpider(scrapy.Spider):
    name = 'casetracker'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://oficinajudicialvirtual.pjud.cl/home/index.php",
            wait_time=3,
            callback=self.parse,
            screenshot=True
        )

    def parse(self, response):
        # with open("proof_of_work.png", "wb") as file:
        #     file.write(response.meta["screenshot"])

        browser = response.meta["driver"]
