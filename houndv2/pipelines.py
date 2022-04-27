# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import sqlite3
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SQLlitePipeline(object):
    collection_name = "casetracker"
    case_uid = 1

    def open_spider(self, spider):
        # Connect to db
        self.connection = sqlite3.connect("casetracker.db")
        self.db = self.connection.cursor()

        # Create table 
        try:
            self.db.execute('''
                CREATE TABLE casetracker(
                    row_id INTEGER AUTOINCREMENT,
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
        # logging.info("Spider closed from pipeline")
        # Close db
        self.connection.close()
        # print(self.cases)
        
    
    def process_item(self, item, spider):
        # self.tracking_data = item["tracking_data"]
        # # 'tracking_data': {'COMPETENCIA': 'Corte Apelaciones', 'CORTE': 'San Miguel', 'TIPO': 'Protección', 'ROL': 7780, 'AÑO': 2020, 'ARCHIVADA': True}
        # case = [
        #     item["folio"],
        #     # item["anexo"],
        #     item["tramite"],
        #     item["descripcion"],
        #     item["fecha"],
        #     item["sala"],
        #     item["estado"],
        #     item["doc"],
        #     # item["georef"],
        # ]
        
        # with open(f"causas/C.A. de {self.tracking_data['CORTE']}-{self.tracking_data['ROL']}-{self.tracking_data['AÑO']}.csv", "a") as file:
        #     writer = csv.writer(file)
        #     writer.writerow(case)
        # item["tracking_data"]
        # # Insert into db
        self.db.execute('''
            INSERT INTO casetracker (case_uid, folio, tramite, descripcion, fecha, sala, estado, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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