import scrapy


class HoundspiderSpider(scrapy.Spider):
    name = "houndspider"

    def start_requests(self):
        url = ""
        yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        pass
