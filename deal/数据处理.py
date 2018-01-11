import pymongo
import configparser
import json

class dealSpider(object):

    top = [
            ("ylct","饮料冲调"),
            ("mc","茗茶"),
            ("pplj","品牌礼券"),
            ("dftc","地方特产"),
            ("jksp","进口食品"),
            ("lytw","粮油调味"),
            ("xxsp","休闲食品"),
            ("zwmj","中外名酒"),
            ("xxsg","新鲜水果"),
            ("hxsc","海鲜水产"),
            ("ldys","精选肉类"),
            ("jxrl","冷饮冻食")
        ]

    def __init__(self,file):
        #读取配置
        self.initConfig(file)
        #连接mongo
        self.dbInit()
       
    def initConfig(self,file):
        conf = configparser.ConfigParser()
        conf.read(file)
        self.conf = conf
    
    def getConfig(self,key):
        return self.conf.get("mongo",key)

    def dbInit(self):
        
        try:

            client = pymongo.MongoClient(host=self.getConfig("host"),port=int(self.getConfig("port")),\
                                            username=self.getConfig("user"),password=self.getConfig("pwd"))
            #指向指定的数据库
            self.db = client[self.getConfig("dbname")]
            #指定集合
            #self.collection = db[collection]

        except pymongo.errors.ConnectionFailure as e:
             print("Could not connect to server: %s" % e)

    #指定集合
    def setCollection(self,collection):
        self.collection = self.db[collection]

    #无线级分类
    def generateTree(self,key,level):
        data = []
        level += 1

        for each in self.findData({"parent":key}):
            res1 = {"name":each["top"]}
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

    def findData(self,condition):
        return self.collection.find(condition)

    def toJson(self,list):
        return json.dumps(list, indent=2,ensure_ascii=False)
    

if __name__ == "__main__":
    deal = dealSpider('./config.ini')
    #设置集合
    deal.setCollection("mc")
    res = deal.generateTree("茗茶",0)
    #print(deal.toJson(res))
    deal.getTreeData(res)