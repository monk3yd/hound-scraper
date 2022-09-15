import scrapy


class HoundspiderSpider(scrapy.Spider):
    name = "houndspider"

    def start_requests(self):
        url = "https://oficinajudicialvirtual.pjud.cl/indexN.php"
        yield scrapy.Request(url, meta={"playwright": True})

    def parse(self, response):
        yield {
            "text": response.text
        }
