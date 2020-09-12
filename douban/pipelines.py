# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

class DoubanPipeline:
    def __init__(self):
        mongo_client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        mydb = mongo_client['douban']
        self.collection = mydb['douban_movie']

    def process_item(self, item, spider):
        data = dict(item)
        self.collection.insert(data)
        return item
