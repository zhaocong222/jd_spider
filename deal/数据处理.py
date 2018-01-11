import pymongo
import configparser

class dealSpider(object):

    top = ["饮料冲调","茗茶","品牌礼券","地方特产","进口食品","粮油调味","休闲食品","中外名酒","新鲜水果","海鲜水产","冷饮冻食","精选肉类"]

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
            db = client[self.getConfig("dbname")]
            #指定集合
            self.collection = db.sku2

        except pymongo.errors.ConnectionFailure as e:
             print("Could not connect to server: %s" % e)

        
    
    def findData(self):
        print(self.collection.find_one({"top":"进口食品"}))

if __name__ == "__main__":
    deal = dealSpider('./config.ini')
    deal.findData()
    