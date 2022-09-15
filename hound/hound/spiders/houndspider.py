import scrapy
from scrapy_playwright.page import PageCoroutine  # async


class HoundspiderSpider(scrapy.Spider):
    name = "houndspider"

    def start_requests(self):
        url = "https://oficinajudicialvirtual.pjud.cl/indexN.php"
        yield scrapy.Request(url, meta={
            "playwright": True,  # use playwright when performing request
            "playwright_include_page": True,  # Instantiate playwrights' page object
            "playwright_page_coroutines": [
                PageCoroutine("wait_for_selector", "button#btnConConsulta")  # wait for selector to load before returning response
            ]
        })

    async def parse(self, response):
        yield {
            "text": response.text
        }
