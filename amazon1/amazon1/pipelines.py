# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import pymongo 
from pymongo import MongoClient
import json
# from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv

class MongoDBAmazon1Pipeline:
    def __init__(self):
        # connection String
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['dbmycrawler'] # Create Database      
        pass
    
    def process_item(self, item, spider):
        
        collection =self.db['tblamazon'] # Create Colecction or Table
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")       
        pass    

class JsonDBAmazon1Pipeline:
    def process_item(self, item, spider):
        with open('amazon.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item

class CSVDBAmazon1Pipeline:
    '''
    mỗi thông tin cách nhau với dấu $
    Ví dụ: coursename$lecturer$intro$describe$courseUrl
    Sau đó, cài đặt cấu hình để ưu tiên Pipline này đầu tiên
    '''
    def process_item(self, item, spider):
        with open('amazon.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='$')
            writer.writerow([
                item['productName'], 
                item['brand'],
                item['productDescription'],
                item['countryOfOrigin'],
                item['price'], 
                item['typicalPrice'],
                item['boughtInPastMonth'],
                item['comment'], 
                item['rate'],
                item['star']
            
            ])
        return item
    pass
