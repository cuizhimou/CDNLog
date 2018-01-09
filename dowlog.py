# -* - coding: UTF-8 -* -
import os
import requests
import gzip
import cdn
import json


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
    # g = gzip.GzipFile(mode='rb', fileobj=open('./'+Logname,'rb'))
    # open('./'+Logname, 'wb').write(g.read())
#解析json数据,迭代器
def Parsers(requesturl):
    r = requests.get(requesturl, stream=True)
    data = json.loads(r.content)
    alist=data['DomainLogModel']['DomainLogDetails']['DomainLogDetail']
    for con in alist:
       yield  con['LogName'], con['LogPath']


if __name__ == '__main__':
    cdn.setup_credentials()
    user_params = {
        "Action": "DescribeCdnDomainLogs","DomainName":"cdn.feellike21.com","LogDay": "2017-12-22"
    }
    apiurl=cdn.make_request(user_params)
    print apiurl
    Parsers(apiurl)
    for name,path in Parsers(apiurl):
        path='https://'+path
        dowlog(name,path)