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
    headers = ['Folio', 'Doc', 'Trámite', 'Descripción', 'Fecha', 'Sala', 'Estado']  # headers = ['Folio', 'Doc', 'Anexo', 'Trámite', 'Descripción', 'Fecha', 'Sala', 'Estado', 'Georeferencia']

    # def open_spider(self, spider):
    #     logging.info("Spider opened from pipeline")
    #     # Connect to db
    #     self.connection = sqlite3.connect("casetracker.db")
    #     self.db = self.connection.cursor()

    #     # Create table 
    #     try:
    #         self.db.execute('''
    #             CREATE TABLE casetracker(
    #                 competencia TEXT,
    #                 corte TEXT,
    #                 tipo TEXT,
    #                 rol TEXT,
    #                 year TEXT
    #             );
    #         ''')
    #     except sqlite3.OperationalError:
    #         pass

    # def close_spider(self, spider):
        # logging.info("Spider closed from pipeline")
        # Close db
        # self.connection.close()
        # print(self.cases)
    
    def process_item(self, item, spider):
        tracking_data = item["tracking_data"]
        # 'tracking_data': {'COMPETENCIA': 'Corte Apelaciones', 'CORTE': 'San Miguel', 'TIPO': 'Protección', 'ROL': 7780, 'AÑO': 2020, 'ARCHIVADA': True}
        case = [
            item["folio"],
            item["doc"],
            # item["anexo"],
            item["tramite"],
            item["descripcion"],
            item["fecha"],
            item["sala"],
            item["estado"],
            # item["georef"],
        ]
        
        with open(f"causas/C.A. de {tracking_data['CORTE']}-{tracking_data['ROL']}-{tracking_data['AÑO']}.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(case)

        # # Insert into db
        # self.db.execute('''
        #     INSERT INTO casetracker (competencia, corte, tipo, rol, year) VALUE (?, ?, ?, ?, ?,)
        # ''', (
        #     item["competencia"],
        #     item["corte"],
        #     item["tipo"],
        #     item["rol"],
        #     item["year"]
        # ))
        # self.connection.commit()
        return item