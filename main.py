# import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    # Connect to db
    engine = create_engine("sqlite:///casetracker.db")
    db = engine.connect()
    # connection = sqlite3.connect("casetracker.db")
    # db = connection.cursor()
    try:
        db.execute('''
            CREATE TABLE cases_track_data (
                uid INTEGER PRIMARY KEY,
                competencia TEXT,
                corte TEXT,
                tipo TEXT,
                rol INTEGER,
                year INTEGER,
                archivada TEXT
            );
        ''')
    except OperationalError:
        pass
    
    # Get cases track data csv -> df -> db
    df = pd.read_csv("cases_track_data.csv")
    df.to_sql("cases_track_data", db, if_exists="replace", index=True, index_label="uid")
    print(df)

    # Extract tracking data from db  
    all_tracking_data_df = pd.read_sql_query("SELECT uid, COMPETENCIA, CORTE, TIPO, ROL, AÑO FROM cases_track_data WHERE archivada = FALSE", db)
    print(all_tracking_data_df)
    # all_tracking_data = df.to_dict(orient="records")
    # print(all_tracking_data)
    exit()
    # Scrape with Selenium & Scrapy
    process = CrawlerProcess(get_project_settings())
    process.crawl("casetracker", all_tracking_data=all_tracking_data)
    process.start()

    # Send via Email


if __name__ == "__main__":
    main()