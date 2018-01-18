# -*- coding: utf-8 -*-
import scrapy
import os
import json
from jd_goods_spider.items import JdGoodsSpiderItem
from scrapy_splash import SplashRequest

class GoodsSpider(scrapy.Spider):
    name = 'goods'
    
    def start_requests(self):
        file = os.getcwd() + '/../deal/leaf.json'
        res = []
        with open(file,"r") as f:
            res = json.loads(f.read())
        
        for each in res:
            yield scrapy.Request(url=each["url"],callback=self.parselist,meta={"name":each["name"],"id":each["id"]})
          
            #yield SplashRequest(url=each["url"],callback=self.parselist,meta={"name":each["name"],"id":each["id"]})
          
    #采集商品列表
    def parselist(self, response):
        
        res = response.xpath("//li[@class='gl-item']")
        for each in res:
            
            img = each.xpath(".//div[@class='p-img']/a/img/@src").extract()
            if not img:
                img = each.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract()[0].strip()
            else:
                img = img[0].strip()
            url = each.xpath(".//div[@class='p-img']/a/@href").extract()[0].strip()
            title = each.xpath(".//div[@class='p-name']/a/em/text()").extract()[0].strip()
            #price = each.xpath(".//strong[@class='J_price']/i/text()").extract()[0]
            
            data = {
                "img" : img[2:],
                "url" : "https://"+url[2:],
                "title":title,
            #    "price":price,
                "price_plus":''
            }
            
            #会员价
            #price_plus = each.xpath(".//span[@class='price-plus-1']").extract()
            #if price_plus:
            #    data["price_plus"] = each.xpath(".//span[@class='price-plus-1']/em/text()").extract()[0][1:]

            name = response.meta["name"]
            _id  = response.meta["id"]
        
            yield scrapy.Request(url=data["url"],callback=self.parseDetail,meta={"name":name,"id":_id,"goods":data})
          
    #采集商品详情
    def parseDetail(self, response):
        
        name = response.meta["name"]
        _id  = response.meta["id"]
        data = response.meta["goods"]

        #相册
        res = response.xpath("//div[@id='spec-list']/ul/li")
        gallery = []
        for each in res:
            src = each.xpath("./img/@src").extract()[0]
            gallery.append(src[2:])

        #介绍
        #品牌
        brand = response.xpath("//ul[@id='parameter-brand']li/a/text()").extract()[0]
        
            


    


    