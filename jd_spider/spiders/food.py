# -*- coding: utf-8 -*-
import scrapy


class FoodSpider(scrapy.Spider):
    name = 'food'
    allowed_domains = ['jd.com']
    
    #采集10个分类
    def start_requests(self):
        urls = {
            #"饮料冲调":"https://list.jd.com/list.html?cat=1320,1585",
            #"茗茶":"https://list.jd.com/list.html?cat=1320,12202",
            #"品牌礼券":"https://list.jd.com/list.html?cat=1320,2641",
            #"地方特产":"https://list.jd.com/list.html?cat=1320,1581",
            "进口食品":"https://list.jd.com/list.html?cat=1320,5019",
            #"粮油调味":"https://list.jd.com/list.html?cat=1320,1584",
            #"休闲食品":"https://list.jd.com/list.html?cat=1320,1583",
            #"中外名酒":"https://list.jd.com/list.html?cat=12259,12260",
            #"新鲜水果":"https://list.jd.com/list.html?cat=12218,12221",
            #"海鲜水产":"https://list.jd.com/list.html?cat=12218,12222",
            #"冷饮冻食":"https://list.jd.com/list.html?cat=12218,13581",
            #"精选肉类":"https://list.jd.com/list.html?cat=12218,13591",
        }

        for name,url in urls.items():
            yield scrapy.Request(url=url,callback=self.parse,meta={"name":name})


    def parse(self, response):
            
        res = response.xpath("//div[contains(@class,'J_selectorLine')]")
        for each in res:
            sky = self.dealsku(each)
            
    def dealsku(self,item):
        key = item.xpath(".//div[@class='sl-key']/span/text()").extract()[0]
        val = item.xpath(".//ul[contains(@class,'J_valueList')]/li/a")
        for each in val:
            img = each.xpath("./img")
            #品牌
            if len(img):
                src = 
            
