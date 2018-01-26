#定时脚本维护代理池，每10秒执行一次 (检测如果有200个ip，不再填充)
from cache import CacheTool
import requests
import json

l = CacheTool.llen("proxyip")
if l > 200:
    exit(0)

#填充ip
url = "http://www.mogumiao.com/proxy/api/get_ip_bs?appKey=2a5fa9f1ca5d485c9ee99a07cf917471&count=10&expiryDate=5&format=1"
checkurl = 'https://www.jd.com/?cu=true&utm_source=baidu-pinzhuan&utm_medium=cpc&utm_campaign=t_288551095_baidupinzhuan&utm_term=0f3d30c8dba7459bb52f2eb5eba8ac7d_0_bf0aeea766724134a6f40590e93e8e9c'

try:
    res = requests.get(url)
    res = json.loads(res.text)
    if res["code"] == "0":
        for each in res["msg"]:
            ip = "http://"+each["ip"]+":"+each["port"]
            res1 = requests.get(checkurl, proxies={"http":ip})
            if res1.status_code == 200:
                CacheTool.rpush("proxyip",ip)
except:
    print('failed')