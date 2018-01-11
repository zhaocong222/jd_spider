from redis import StrictRedis, ConnectionPool
import hashlib

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