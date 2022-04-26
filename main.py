import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # Load cases tracking data
    df = pd.read_csv("db.csv")
    all_tracking_data = df.to_dict(orient="records")  # List of dicts

    # Selenium & Scrapy
    process = CrawlerProcess(get_project_settings())
    process.crawl("casetracker", all_tracking_data=all_tracking_data)
    process.start()


if __name__ == "__main__":
    main()