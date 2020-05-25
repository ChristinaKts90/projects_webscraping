# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class MongodbPipeline(object):
    collection_name = "best_movies"

    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb+srv://christina:testtest@cluster0-x1ioo.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client["IMDB"]

    def close_spider(self,spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLlitePipeline(object):

    def open_spider(self,spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_movies(
                    Title TEXT,
                    Year TEXT,
                    Duration TEXT,
                    Genre TEXT,
                    Rating TEXT,
                    Movie_url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self,spider):
        self.connection.close()


    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO best_movies (Title,Year,Duration,Genre,Rating,Movie_url) VALUES(?,?,?,?,?,?) 
        ''', (
            item.get('Title'),
            item.get('Year'),
            item.get('Duration'),
            item.get('Genre'),
            item.get('Rating'),
            item.get('Movie_url')
        ))
        self.connection.commit()
        return item