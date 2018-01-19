# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGoodsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    #商品主图
    goods_main_img = scrapy.Field() 
    #商品名
    goods_title = scrapy.Field()
    #商品url
    goods_url = scrapy.Field()
    #商品价格
    goods_price = scrapy.Field()
    #商品会员价格
    goods_price_plus = scrapy.Field()
    #商品所属分类名
    cat_name = scrapy.Field()
    #商品所属分类id
    cat_id = scrapy.Field()
    #商品相册
    goods_gallery = scrapy.Field()
    #广告图
    goods_adver = scrapy.Field()
    #商品介绍
    goods_info = scrapy.Field()
    #商品规格包装
    goods_package = scrapy.Field()