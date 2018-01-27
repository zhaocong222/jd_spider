# -*- coding: utf-8 -*-
import scrapy
import os
import json
import random
from jd_goods_spider.items import JdGoodsSpiderItem
from scrapy_splash import SplashRequest
from scrapy.conf import settings
from jd_goods_spider.cache import CacheTool

class GoodsSpider(scrapy.Spider):
    name = 'goods'

    myheader = {
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    #从队列中获取一个ip
    def getProxyIp(self):
        return CacheTool.lpop("proxyip")

    def getargs(self):
        ip = self.getProxyIp()
        return {'proxy':ip}

    def getRandomHeader(self,referer = "https://www.jd.com/?cu=true&utm_source=baidu-pinzhuan&utm_medium=cpc&utm_campaign=t_288551095_baidupinzhuan&utm_term=0f3d30c8dba7459bb52f2eb5eba8ac7d_0_566711d8905d4aeaa03ad36c79c12e98"):
        self.myheader["User-Agent"] = random.choice(settings['USER_AGENTS'])
        self.myheader["Referer"] = referer
        return self.myheader
         
    def start_requests(self):
       
        file = os.getcwd() + '/../deal/leaf.json'
        res = []
        with open(file,"r") as f:
            res = json.loads(f.read())
        
        for each in res:
            myargs={'wait': 2.5, 'proxy':self.getProxyIp(),}
            yield SplashRequest(url=each["url"],callback=self.parselist,meta={"name":each["name"],"id":each["id"]},headers=self.getRandomHeader(),args=myargs)

    #采集商品列表
    def parselist(self, response):

        print(response.url)
        '''
        name = response.meta["name"]
        _id  = response.meta["id"]
        res = response.xpath("//li[@class='gl-item']")
        
        for each in res:
            
            img = each.xpath(".//div[@class='p-img']/a/img/@src").extract()
            if not img:
                img = each.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract()[0].strip()
            else:
                img = img[0].strip()
                
            url = each.xpath(".//div[@class='p-img']/a/@href").extract()[0].strip()
            title = each.xpath(".//div[@class='p-name']/a/em/text()").extract()[0].strip()
            price = each.xpath(".//strong[@class='J_price']/i/text()").extract()
            
            data = {
                "img" : img[2:],
                "url" : "https://"+url[2:],
                "title":title,
                "price":'',
                "price_plus":''
            }

            if price:
                data["price"] = price[0]

            #会员价
            price_plus = each.xpath(".//span[@class='price-plus-1']").extract()
            if price_plus:
                data["price_plus"] = each.xpath(".//span[@class='price-plus-1']/em/text()").extract()[0][1:]

            #yield SplashRequest(url=data["url"],callback=self.parseDetail,meta={"name":name,"id":_id,"goods":data},headers=self.getRandomHeader(response.url))
            #yield scrapy.Request(url=data["url"],callback=self.parseDetail,meta={"name":name,"id":_id,"goods":data})
        
        #获取下一页的page url
        next_page = response.xpath("//a[@class='pn-next']/@href").extract()
        if next_page:
            url = 'https://list.jd.com'+next_page[0]
            #yield SplashRequest(url=url,callback=self.parselist,meta={"name":name,"id":_id},headers=self.getRandomHeader(response.url))
        '''

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

        #品牌
        goods_brand = ''
        brand = response.xpath("//ul[@id='parameter-brand']/li/a/text()").extract()
        if brand:
            goods_brand = brand[0]

        #商品介绍
        info  = response.xpath("//ul[contains(@class,'parameter2')]/li/text()").extract()
        goods_info = {}
        #转换dict
        if info:
            for each in info:
                _res = each.split('：')
                goods_info[_res[0]] = _res[1]
                
        #规格与包装
        package_info = {}
        package = response.xpath("//div[@class='Ptable-item']/dl/*/text()").extract()
        if package:
            package_info = dict(zip(package[0::2],package[1::2]))
        
        #广告图
        adver_map = []
        adver_map = response.xpath("//div[@class='detail-content-item']//img/@data-lazyload").extract()
        adver_map = [i[2:] for i in adver_map]

        #定义数据返回管道
        item = JdGoodsSpiderItem()
        item["goods_main_img"] = data["img"]
        item["goods_title"] = data["title"]
        item["goods_url"] = data["url"]
        item["goods_price"] = data["price"]
        item["goods_price_plus"] = data["price_plus"]
        item["cat_name"] = name
        item["cat_id"] = _id
        item["goods_gallery"] = gallery
        item["goods_adver"] = adver_map
        item["goods_info"] = package_info
        item["goods_package"] = package_info
        item["goods_brand"] = goods_brand
        
        yield item



    


    