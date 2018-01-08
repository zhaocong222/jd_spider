# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class JdSpiderPipeline(object):
    
    def __init__(self):
        #获取配置文件里的mongo信息
        
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        username = settings['MONGODB_USER']
        password = settings['MONGODB_PWD']
        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host,port=port,username=username,password=password)
        #指向指定的数据库
        db = client[dbname]
        #指定集合
        self.collection = db.sku
        

    def process_item(self, item, spider):
    
        data = dict(item)
        #写入
        self.collection.insert(data)
        return item
