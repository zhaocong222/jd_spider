# -*- coding: utf-8 -*-
import scrapy


class GoodsSpider(scrapy.Spider):
    name = 'goods'
    allowed_domains = ['item.jd.com']
    start_urls = ['http://item.jd.com/']

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
        pass

    def parse(self, response):
        pass
