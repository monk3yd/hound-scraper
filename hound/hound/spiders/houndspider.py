import scrapy
from scrapy_playwright.page import PageCoroutine  # async


class HoundspiderSpider(scrapy.Spider):
    name = "houndspider"

    def start_requests(self):
        url = "https://oficinajudicialvirtual.pjud.cl/indexN.php"
        yield scrapy.Request(url, meta=dict(
                playwright=True,
                playright_include_page=True,
                errback=self.errback, # make sure page is closed even if request fails
                playwright_page_coroutines=[
                    PageCoroutine("wait_for_selector", "button#btnConConsulta")
                ]
            ))

    async def parse(self, response):
        yield {
            "text": response.text
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
