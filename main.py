from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # Scrapy
    process = CrawlerProcess(get_project_settings())
    process.crawl("casetracker")
    process.start()


if __name__ == "__main__":
    main()