from redis import StrictRedis, ConnectionPool
import hashlib
import requests

pool = ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis = StrictRedis(connection_pool=pool)

class CacheTool:

    @staticmethod
    def hsetnx(key,field,val):
        return redis.hsetnx(key,field,val)

    @staticmethod
    def set(name,value):
        return redis.set(name,value)

    def get(name):
        return redis.get(name)

    @staticmethod
    def sadd(value):
        return redis.sadd('url',value)

    @staticmethod
    def smembers():
        return redis.smembers('url')
    
    @staticmethod
    def rpush(key,val):
        return redis.rpush(key,val)

    @staticmethod
    def lpop(key):
        return redis.lpop(key)

    @staticmethod
    def llen(key):
        return redis.llen(key)

'''
#检测ip
try:
    requests.get('http://wenshu.court.gov.cn/', proxies={"http":"http://140.250.162.201:38272"})
except:
    print('connect failed')
else:
    print('success')
'''

'''
#出队入队
print(CacheTool.rpush("proxyip","213.324.12.22:324"))
print(CacheTool.rpush("proxyip","213.324.12.22:325"))

print(CacheTool.lpop("proxyip"))
print(CacheTool.lpop("proxyip"))
print(CacheTool.lpop("proxyip"))
'''

'''
url = 'www.baidu.com'
m2 = hashlib.md5()
m2.update(url.encode("utf-8"))
print(m2.hexdigest())

print(CacheTool.hsetnx("jd_spider",m2.hexdigest(),url))
print(CacheTool.hsetnx("jd_spider",m2.hexdigest(),url))
'''

'''
print(CacheTool.sadd("www.baidu.com"))
print(CacheTool.sadd("www.baidu.com"))
print(CacheTool.sadd("www.baidu.com"))
print(CacheTool.sadd("www.baidu.com"))
print(CacheTool.sadd("www.qq.com"))
print(CacheTool.smembers())
'''