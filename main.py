import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # Load cases data for search from db
    df = pd.read_csv("db.csv")
    all_tracked_data = df.to_dict(orient="index")

    # Selenium

    # Scrapy
    process = CrawlerProcess(get_project_settings())
    process.crawl("casetracker", all_tracked_data=all_tracked_data)
    process.start()


if __name__ == "__main__":
    main()