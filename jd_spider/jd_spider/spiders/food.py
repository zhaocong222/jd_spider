# -*- coding: utf-8 -*-
import scrapy
from jd_spider.items import JdSpiderItem
import hashlib
from jd_spider.cache import CacheTool

class FoodSpider(scrapy.Spider):
    name = 'food'
    #allowed_domains = ['jd.com']
    base_url = 'https://list.jd.com'
    
    def gethash(self,url):
        m2 = hashlib.md5()
        m2.update(url.encode("utf-8"))
        return m2.hexdigest()
    
    #采集10个分类
    def start_requests(self):
        urls = {
            #"饮料冲调":"https://list.jd.com/list.html?cat=1320,1585",
            #"茗茶":"https://list.jd.com/list.html?cat=1320,12202",
            #"品牌礼券":"https://list.jd.com/list.html?cat=1320,2641",
            #"地方特产":"https://list.jd.com/list.html?cat=1320,1581",
            #"进口食品":"https://list.jd.com/list.html?cat=1320,5019",
            #"粮油调味":"https://list.jd.com/list.html?cat=1320,1584",
            #"休闲食品":"https://list.jd.com/list.html?cat=1320,1583",
            #"中外名酒":"https://list.jd.com/list.html?cat=12259,12260",
            #"新鲜水果":"https://list.jd.com/list.html?cat=12218,12221",
            #"海鲜水产":"https://list.jd.com/list.html?cat=12218,12222",
            #"精选肉类":"https://list.jd.com/list.html?cat=12218,13581",
            #"冷饮冻食":"https://list.jd.com/list.html?cat=12218,13591",
        }

        for name,url in urls.items():
            yield scrapy.Request(url=url,callback=self.parse,meta={"name":name})


    def parse(self, response):
            
        res = response.xpath("//div[contains(@class,'J_selectorLine')]")
        skues = []
        for each in res:
            
            key = each.xpath(".//div[@class='sl-key']/span/text()").extract()[0].strip()
            val = each.xpath(".//ul[contains(@class,'J_valueList')]/li")
            sku = []

            for each2 in val:
                img = each2.xpath(".//img")
                name = each2.xpath("./a/text()").extract()[0].strip()
                url = each2.xpath("./a/@href").extract()[0].strip()

                if len(img):
                    src = img.xpath('@src').extract()[0].strip()
                    json = {"name":name,"src":src}
                    sku.append(json)
                else:
                    sku.append(name)

                #采集分类的sku
                md5 = self.gethash(url)
                if key.startswith('分类') and CacheTool.hsetnx("url",md5,url) :
                    yield scrapy.Request(url=self.base_url+url,callback=self.parse,meta={"name":name,"parent":response.meta["name"]},dont_filter=True)                            

            skues.append({key:sku})

        jd = JdSpiderItem()
        jd["sku"] = skues
        jd["top"] = response.meta["name"]
        jd["url"] = response.url
        
        if "parent" in response.meta:
            jd["parent"] = response.meta["parent"]

        yield jd