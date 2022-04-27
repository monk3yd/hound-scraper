import csv
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # Load cases tracking data  # TODO cases tracking data db
    df = pd.read_csv("db.csv")
    all_tracking_data = df.to_dict(orient="records")  # List of dicts

    # Create case file and include header
    # header = ['Folio', 'Trámite', 'Descripción', 'Fecha', 'Sala', 'Estado', 'Link']  # headers = ['Folio', 'Doc', 'Anexo', 'Trámite', 'Descripción', 'Fecha', 'Sala', 'Estado', 'Georeferencia']
    # for tracking_data in all_tracking_data:
    #     with open(f"causas/C.A. de {tracking_data['CORTE']}-{tracking_data['ROL']}-{tracking_data['AÑO']}.csv", "a") as file:
    #         writer = csv.writer(file)
    #         writer.writerow(header)

    # Scrape with Selenium & Scrapy
    process = CrawlerProcess(get_project_settings())
    process.crawl("casetracker", all_tracking_data=all_tracking_data)
    process.start()

    # Send via Email


if __name__ == "__main__":
    main()