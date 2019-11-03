
## Test git
import urllib.request
import json
import time
import os

def Crawl(index):
    host = 'http://toutiao-ali.juheapi.com'
    path = '/toutiao/index'
    method = 'GET'
    appcode = 'bbe5db8dbc634e45b6a7365fb3d57126'
    appkey ="6ng60wibgp5vmby0pm5jlf8tykiia6p7"
    querys = 'type=type'
    bodys = {}
    url = host + path + '?' + querys
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")
    path="/home/yuanzhu/Desktop/Crawler/CrawlerAndAnalyse/DataSet/{}.txt".format(index)
    with open(path,'w')as f :
        f.write(content)
    print("{} 新闻存储成功".format(index))
    jsonc=json.loads(content)
    datalist = jsonc['result']['data']
    keys  =jsonc.keys()
    for data in datalist:
        print(type(data))
        keys=None
        if(isinstance(data,dict)):
            keys = data.keys()
            #dict_keys(['uniquekey', 'title', 'date', 'category', 'author_name', 'url', 'thumbnail_pic_s', 'thumbnail_pic_s02', 'thumbnail_pic_s03'])
            #print(keys)
        for key in keys:
            print("{}:{}".format(key,data[key]))


def StartCrwal():
    index=1
    while True:
        if(index>1500):
            print("______________Crawler end______________")
            break
        Crawl(index)
        index+=1
        time.sleep(120)

def Extral(filepath):
    #path = "/home/yuanzhu/Desktop/Crawler/CrawlerAndAnalyse/DataSet"
    #filepath = os.path.join(path,"{}.txt".format(index))
    if os.path.isfile(filepath):
        with open(filepath,'r')as f:
            data = f.read()
        jsonc  =json.loads(data)
        #jsonkeys=jsonc.keys()   ===>dict_keys(['reason', 'result', 'error_code'])
        resultdic  =jsonc['result']
        #resultdickeys =resultdic.keys()===>dict_keys(['stat', 'data'])
        #print(resultdickeys)
        datalist=jsonc['result']['data']
        for data in datalist:
            datakeys = data.keys()
            #print(datakeys) ['uniquekey', 'title', 'date', 'category', 'author_name', 'url',
            # 'thumbnail_pic_s', 'thumbnail_pic_s02', 'thumbnail_pic_s03']
            for key in datakeys:
                value = data[key]
                print("{}:{}".format(key,value))
            break
    else:
        print("file is not exist")

def InsertToMySQL():
    path = "/home/yuanzhu/Desktop/Crawler/CrawlerAndAnalyse/DataSet"
    filelist = os.listdir(path)
    for file in filelist:
        filepath = os.path.join(path,file)
        Extral(filepath)




def t1():
    InsertToMySQL()

if __name__ == '__main__':
    #StartCrwal() 启动爬虫
    #Extral(1)
    InsertToMySQL()

