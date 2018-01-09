# -* - coding: UTF-8 -* -
import os
import requests
import gzip
import cdn
import json
import datetime


#设置下载后的存放路径
path=r'/Users/cui/yourdisk/cdn-api'
file_name=r'hello.gz'
dest_dir=os.path.join(path,file_name)

#下载日志
def dowlog(Logname,Logpath):
    r = requests.get(Logpath,stream=True)
    with open('./'+Logname, "wb") as f:
        for con in r.iter_content(chunk_size=128):
            if con:
                f.write(con)

    g = gzip.GzipFile(mode='rb', fileobj=open('./'+Logname,'rb'))
    name=Logname.split('.gz')
    open('./'+name[0], 'wb').write(g.read())
#解析json数据,迭代器
def Parsers(requesturl):
    r = requests.get(requesturl, stream=True)
    data = json.loads(r.content)
    alist=data['DomainLogModel']['DomainLogDetails']['DomainLogDetail']
    for con in alist:
       yield  con['LogName'], con['LogPath']


if __name__ == '__main__':
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    domainname='kaiwu.feellike21.com'

    user_params = {
        "Action": "DescribeCdnDomainLogs", "DomainName": domainname, "LogDay": str(yesterday)
    }

    cdn.setup_credentials()
    apiurl=cdn.make_request(user_params)
    print apiurl
    for name,path in Parsers(apiurl):
        path='https://'+path
        dowlog(name,path)