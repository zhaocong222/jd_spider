#coding=utf-8 

import pymongo
import configparser
import json
import pymysql
import time

class dealSpider(object):

    top = [
            ("ylct","饮料冲调","https://list.jd.com/list.html?cat=1320,1585"),
            ("mc","茗茶","https://list.jd.com/list.html?cat=1320,12202"),
            ("pplj","品牌礼券","https://list.jd.com/list.html?cat=1320,2641"),
            ("dftc","地方特产","https://list.jd.com/list.html?cat=1320,1581"),
            ("jksp","进口食品","https://list.jd.com/list.html?cat=1320,5019"),
            ("lytw","粮油调味","https://list.jd.com/list.html?cat=1320,1584"),
            ("xxsp","休闲食品","https://list.jd.com/list.html?cat=1320,1583"),
            ("zwmj","中外名酒","https://list.jd.com/list.html?cat=12259,12260"),
            ("xxsg","新鲜水果","https://list.jd.com/list.html?cat=12218,12221"),
            ("hxsc","海鲜水产","https://list.jd.com/list.html?cat=12218,12222"),
            ("ldys","精选肉类","https://list.jd.com/list.html?cat=12218,13581"),
            ("jxrl","冷饮冻食","https://list.jd.com/list.html?cat=12218,13591")
        ]

    def __init__(self,file):
        #读取配置
        self.initConfig(file)
        #连接mongo
        self.mongoInit()
        #连接mysql
        self.sqlInit()
        
       
    def initConfig(self,file):
        conf = configparser.ConfigParser()
        conf.read(file)
        self.conf = conf
    
    def getConfig(self,types,key):
        return self.conf.get(types,key)

    #mysql
    def sqlInit(self):
        try:
            self.link = pymysql.connect(
                host = self.getConfig("mysql","host"),
                port = int(self.getConfig("mysql","port")),
                user = self.getConfig("mysql","user"),
                password = self.getConfig("mysql","pwd"),
                db = self.getConfig("mysql","dbname"),
                charset = self.getConfig("mysql","charset"),
                cursorclass = pymysql.cursors.DictCursor
            )
            # 使用cursor()方法获取操作游标
            self.cur = self.link.cursor() 

        except Exception as e:
            print(e)
            exit()

    #mongodb
    def mongoInit(self):
        
        try:

            client = pymongo.MongoClient(host=self.getConfig("mongo","host"),port=int(self.getConfig("mongo","port")),\
                                            username=self.getConfig("mongo","user"),password=self.getConfig("mongo","pwd"))
            #指向指定的数据库
            self.db = client[self.getConfig("mongo","dbname")]
            #指定集合
            #self.collection = db[collection]

        except pymongo.errors.ConnectionFailure as e:
             print("Could not connect to server: %s" % e)

    #指定集合
    def setCollection(self,collection):
        self.collection = self.db[collection]

    #无线分类
    def generateTree(self,key,level):
        data = []
        level += 1

        for each in self.findData({"parent":key}):

            res1 = {"name":each["top"],"url":each["url"]}
            if each["top"] != each["parent"]:
                children = self.generateTree(res1["name"],level)
                if children:
                    res1["children"] = children
                
            res1["level"] = level
            data.append(res1)

        return data
            

    #格式化树形
    def getTreeData(self,tree):
        for value in tree:
            str = (value["level"] - 1 ) * ' ' * 3
            print(str + value["name"] + "\n")
            if "children" in value:
                self.getTreeData(value["children"])

    #显示品牌
    def showbrand(self):
        data = []
        for k,v,m in self.top:
            self.setCollection(k)
            res = self.findData({})
            for each in res:
                for res1 in each["sku"]:
                    if "品牌：" in res1:
                        for res2 in res1["品牌："]:
                            data.append(res2)
                        
        return data    

    #mongo
    def findData(self,condition):
       return self.collection.find(condition)

    #mysql
    def findBysql(self,sql):
        try: 
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:  
            raise e 

    def exeDelete(self,sql):
        try:
            self.cur.execute(sql)
             #提交  
            self.link.commit()  

        except Exception as e:  
            #错误回滚  
            self.link.rollback()  
            print(e)   

    def insertBysql(self,sql):
        try:
            self.cur.execute(sql)
             #提交  
            self.link.commit()  
            #返回主键id
            return self.cur.lastrowid
        except Exception as e:  
            #错误回滚  
            self.link.rollback()  
            print(e) 

    #写入顶级分类
    def initTop(self):
        for key,name,url in self.top:
                sql = 'insert into yj_category(name,url,parent_id,level) \
                        values ("'+name+'","'+url+'",0,1)'
                print(deal.insertBysql(sql))

    #写入品牌
    def insetBrand(self,data):

        brand = set([])

        for each in data:
            src = ''
            name = each
            t = int(time.time())
       
            if isinstance(each,dict):
                name = each["name"]
                src = each["src"]
            #防止重复写入
            if name in brand:
                continue
            else:
                sql = 'insert into yj_brand(brand_name,logo,creatime) \
                        values ("'+name+'","'+src[2:]+'",'+str(t)+')'
                print(deal.insertBysql(sql))
                brand.add(name)
          
        print("ok")


    #转换json
    def toJson(self,list):
        return json.dumps(list, indent=2,ensure_ascii=False)
    
    #show
    def showAll(self):
        for key,name,url in self.top:
            deal.setCollection(key)
            res = deal.generateTree(name,1)
            print(self.toJson(res))

    def showOne(self,key,name):
        deal.setCollection(key)
        res = deal.generateTree(name,1)
        print(self.toJson(res))

    #处理数据
    def dealInsert(self,res,pid):
        if res:
            for item in res:
                name = item["name"]
                url = item["url"]
                level = item["level"] 
                #print(name+'-'+url+'-'+str(level)+'-'+str(pid))
                sql = 'insert into yj_category(name,url,parent_id,level) \
                        values ("'+name+'","'+url+'",'+str(pid)+','+str(level)+')'
                lastid = self.insertBysql(sql)
                print(lastid)
                if "children" in item:
                    self.dealInsert(item["children"],lastid)

    #过滤数据(全部写入到mysql后执行，删除重复的分类)
    #查询出 level > 3的记录，删除 对应的patentid并且删除本身
    def filterData(self):
        sql = 'select id,parent_id from yj_category where `level` > 3'
        res = self.findBysql(sql)
        for each in res:
            sql = 'delete from yj_category where id in ('+str(each["parent_id"])+','+str(each["id"])+')'
            self.exeDelete(sql)
        
        print("ok")

    #获取叶子节点的url
    def getUrls(self):
        pass

'''
("ylct","饮料冲调","https://list.jd.com/list.html?cat=1320,1585"),
("mc","茗茶","https://list.jd.com/list.html?cat=1320,12202"),
("pplj","品牌礼券","https://list.jd.com/list.html?cat=1320,2641"),
("dftc","地方特产","https://list.jd.com/list.html?cat=1320,1581"),
("jksp","进口食品","https://list.jd.com/list.html?cat=1320,5019"),
("lytw","粮油调味","https://list.jd.com/list.html?cat=1320,1584"),
("xxsp","休闲食品","https://list.jd.com/list.html?cat=1320,1583"),
("zwmj","中外名酒","https://list.jd.com/list.html?cat=12259,12260"),
("xxsg","新鲜水果","https://list.jd.com/list.html?cat=12218,12221"),
("hxsc","海鲜水产","https://list.jd.com/list.html?cat=12218,12222"),
("jxrl","精选肉类","https://list.jd.com/list.html?cat=12218,13581"),
("ldys","冷饮冻食","https://list.jd.com/list.html?cat=12218,13591")
'''

if __name__ == "__main__":
    deal = dealSpider('./config.ini')
    '''
    #写入品牌
    data = deal.showbrand()
    #写入数据库
    deal.insetBrand(data)
    '''