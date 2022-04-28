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
        return item