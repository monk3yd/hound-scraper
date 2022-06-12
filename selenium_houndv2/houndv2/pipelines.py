# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SQLlitePipeline(object):
    collection_name = "casetracker"
    run_all_movs = False
    movs_case_counter = 0
    case_being_scraped = 0

    def open_spider(self, spider):
        # Connect to db
        self.connection = sqlite3.connect("casetracker.db")
        self.db = self.connection.cursor()

        # Create table 
        try:
            self.db.execute('''
                CREATE TABLE cases_movs (
                    row_id INTEGER PRIMARY KEY,
                    case_uid INTEGER,
                    folio INTEGER,
                    tramite TEXT,
                    descripcion TEXT,
                    fecha TEXT,
                    sala TEXT,
                    estado TEXT,
                    link TEXT
                );
            ''')
        except sqlite3.OperationalError:
                pass


    def close_spider(self, spider):
        # Close db
        self.connection.close()
    
    def process_item(self, item, spider):
        # If wanted to replace deleted files from database consider making a list of folios and comparing
        # case_folios = self.db.execute('''
        #     SELECT folio 
        # ''')

        
        # NEED FIRST ALL-TIME RUN VARIABLE FOR FILLING ALL MOVEMENTS?
        # NEED VARIABLE FOR KNOWING IF SAME CASE IS BEING SCRAPED ON DIFFERENT ROW ITERATIONS

        # Filter by case_uid and last folio
        # Get db_max_folio of each case from case_movs, search with case_uid # TODO
        max_folio = self.db.execute(f'''
            SELECT MAX(folio) FROM cases_movs WHERE case_uid = {item["case_uid"]} LIMIT 1;
        ''').fetchone()[0]
        print(f"MAX FOLIO: {max_folio}")
        self.case_being_scraped = item["case_uid"]
        # db is empty, first time this case is tracked, need filling of all movs  # make scrape_all_movs()
        if max_folio is None:
            self.run_all_movs = True
        
        if self.run_all_movs:
            self.movs_case_counter

        # db is populated with previews movements
        # max folio in db is less than scraped folio (means new mov so insert)  # scrape_new_movs()
        if int(max_folio) < int(item["folio"]):
            # Insert into db
            self.db.execute('''
                INSERT INTO cases_movs (case_uid, folio, tramite, descripcion, fecha, sala, estado, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(item["case_uid"]), 
                int(item["folio"]),
                item["tramite"],
                item["descripcion"],
                item["fecha"],
                item["sala"],
                item["estado"],
                item["link"]
            ))
            self.connection.commit()
        # else max folio is equal to scraped folio, no new movs
        return item