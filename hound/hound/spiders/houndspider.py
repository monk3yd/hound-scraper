import scrapy


class HoundspiderSpider(scrapy.Spider):
    name = 'houndspider'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
