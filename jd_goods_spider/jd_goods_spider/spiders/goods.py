# -*- coding: utf-8 -*-
import scrapy
import os
import json
from jd_goods_spider.items import JdGoodsSpiderItem
from scrapy_splash import SplashRequest

class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['item.jd.com']
    start_urls = ["https://list.jd.com/list.html?cat=12218,13591,13595&ev=1107_89465&sort=sort_rank_asc&trans=1&JL=3_%E5%88%86%E7%B1%BB_%E8%B4%A1%E4%B8%B8#J_crumbsBar"]

    
    def start_requests(self):
        file = os.getcwd() + '/../deal/leaf.json'
        res = []
        with open(file,"r") as f:
            res = json.loads(f.read())
        
        for each in res:
            yield SplashRequest(url=each["url"],callback=self.parse,meta={"name":each["name"],"id":each["id"]})
          
    #采集商品
    def parse(self, response):
        
        res = response.xpath("//li[@class='gl-item']")
        for each in res:
            item = JdGoodsSpiderItem()
            img = each.xpath(".//div[@class='p-img']/a/img/@src").extract()
            if not img:
                img = each.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract()[0].strip()
            else:
                img = img[0].strip()
            url = each.xpath(".//div[@class='p-img']/a/@href").extract()[0].strip()
            title = each.xpath(".//div[@class='p-name']/a/em/text()").extract()[0].strip()
            price = each.xpath(".//strong[@class='J_price']/i/text()").extract()[0]
            
            item = {
                "img" : img[2:],
                "url" : url[2:],
                "title":title,
                "price":price,
                "price_plus":''
            }
            
            #会员价
            price_plus = each.xpath(".//span[@class='price-plus-1']").extract()
            if price_plus:
                price_plus = price_plus[0].xpath("./em/text()").extract()
                
            print(price_plus)
