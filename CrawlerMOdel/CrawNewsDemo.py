import requests
from scrapy.selector import Selector
import time
import json
import os
import logging
def getlloger():
    loggerpath=os.path.join(os.getcwd(),'RunningLog.txt')
    logger = logging.getLogger("loggingmodule.NomalLogger")
    handler = logging.FileHandler(loggerpath)
    formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
# test
#logger.debug("this is a debug msg!")
#logger.info("this is a info msg!")
def loggerdemo():
    logger = getlloger()
    logger.debug('hello this is debug')
    logger.error('this is error')
    logger.info('this is info')



def ParseModel():
    #strYear=input('输入年份')
    #strDate=input('输入月份和日期区间')
    strYear='2019'
    strDay=None
    #从5月第一天开始抓
    for day in range(1,31):
    #for day in range(18,32):
        if day<10:
            strDay='0'+str(day)
        else:
            strDay=str(day)
        strDate='06{}'.format(strDay)
        Time=strYear+strDate
        demo1(Time)
        time.sleep(2)

#  解析输入时间参数  主函数   诱导网页链接提取
def demo1(Time):
    logger=getlloger()
    #Time = input('Input time  like 20191026 ')
    #Time='20190501'
    lenth = len(Time)
    Y=Time[:4]
    O=Time[4:]
    index=0
    FileDir='/home/yuanzhu/Desktop/NewsData/{}'.format(Time)  #日期新闻目录
    if os.path.exists(FileDir):
        pass
    else:
        os.mkdir(FileDir)

    URL='http://www.chinanews.com/scroll-news/{}/{}/news.shtml'.format(Y,O)
    res=requests.get(URL)
    listUrl=[]
    if res.status_code==200:
        res.encoding='utf-8'
        content=res.text
        #print(content)
        selector=Selector(text=content)
        #print(selector.xpath('//title[@lang="eng2"]'))
        #items=selector.xpath('//div[@class="dd_bt"]/a')
        items=selector.xpath('//li')
        baseurl='http://www.chinanews.com'
        for item in items:
            FilePath = '{}/{}{}.json'.format(FileDir, Time, str(index))
            dictNews = {}
            jsonNews = None
            url=''
            try:
                tag =item.xpath('div[@class="dd_lm"]/a/text()').extract()[0]
                title=item.xpath('div[@class="dd_bt"]/a/text()').extract()[0]
                turl=item.xpath('div[@class="dd_bt"]/a/@href').extract()[0]
                url=baseurl+turl
                date=item.xpath('div[@class="dd_time"]/text()').extract()[0]
            except Exception as e :
                continue
            print("tag=:",tag)
            print("title=",title)
            print("url=",url)
            print("date=",date)
            try:
                content=demo2(url)
            except Exception as e :
                logger.error('Content get error')
                continue
            if content==None:
                continue
            listUrl.append(url)
            dictNews.update({'tag':tag})
            dictNews.update({'title':title})
            dictNews.update({'url':url})
            dictNews.update({'date':date})
            dictNews.update({'content':content})
            #jsonNews=json.dumps(dictNews)
            #print(jsonNews)
            try:
                demo3(dictNews,FilePath)
            except Exception as e :
                print('Save faild :',e)
            else:
                print('{} {} Save successful'.format(date,title))
            index = index + 1

    else:
        strLogData='{} Status error status_code :{}'.format(URL,res.status_code)
        print(strLogData)
        logger.error(strLogData)

    #  封测 压力测试 urlList 多久封ip
    # for url in listUrl:
    #     demo2(url)
    #     time.sleep(1)

# 提取网页核心内容
def demo2(url):
    #url='http://www.chinanews.com/sh/2019/05-02/8826407.shtml'
    try:
        res=requests.get(url)
        if res.status_code==200:
            res.encoding='utf-8'
            html=res.text
            selector=Selector(text=html)
            title=selector.xpath('//h1/text()').extract()[0]
            content=selector.xpath('//div[@class="left_zw"]/p/text()').extract()
            content=''.join(content)
        else:
            print('Status Error  :', res.status_code)
    except Exception as e :
        print('Detail extract error  ,  ',e)
        return None
    else:
        print("title  :",title)
        print("content  :",content)
    return content
# 存储demo
def  demo3(model,FilePath):
    with open(FilePath, 'w', encoding='utf-8') as json_file:
        json.dump(model, json_file, ensure_ascii=False)

#读取json文件

def demo4(FilePath):
    dict={}
    FilePath='/home/yuanzhu/Desktop/NewsData/20190918/201909180.json'
    with open(FilePath,'r',encoding='utf-8') as f:
        dict=json.load(f)
    print(type(dict),dict)


if __name__ == '__main__':
    #demo1()
    #demo2()
    #demo4()
    ParseModel()
