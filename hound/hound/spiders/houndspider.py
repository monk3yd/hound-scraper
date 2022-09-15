import scrapy
from scrapy_playwright.page import PageCoroutine  # async


class HoundspiderSpider(scrapy.Spider):
    name = "houndspider"

    def start_requests(self):
        url = "https://oficinajudicialvirtual.pjud.cl/indexN.php"
        yield scrapy.Request(url, meta=dict(
                playwright=True,
                playright_include_page=True,
                errback=self.errback,
                playwright_page_coroutines=[
                    PageCoroutine("wait_for_selector", "button#btnConConsulta")
                ]
            ))

    async def parse(self, response):
        yield {
            "text": response.text
        }
