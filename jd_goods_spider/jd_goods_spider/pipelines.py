# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class JdGoodsSpiderPipeline(object):
    
    def __init__(self):
        pass

    def process_item(self, item, spider):
        pass