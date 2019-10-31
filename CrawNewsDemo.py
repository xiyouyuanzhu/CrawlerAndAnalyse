import requests
from scrapy.selector import Selector
import time
def demo():
    #Time = input('Input time  like 20191026 ')
    Time='20191012'
    lenth = len(Time)
    Y=Time[:4]
    O=Time[4:]
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
            listUrl.append(url)
    else:
        print('Status error')
    for url in listUrl:
        demo2(url)
        time.sleep(1)

#Detail  data
def demo2(url):
    #url='http://www.chinanews.com/gn/2019/10-31/8994866.shtml'
    res=requests.get(url)
    try:
        if res.status_code==200:
            res.encoding='utf-8'
            html=res.text
            selector=Selector(text=html)
            title=selector.xpath('//h1[@style="display:block; position:relative; clear:both"]/text()').extract()
            content=selector.xpath('//div[@class="left_zw"]/p/text()').extract()
            content=''.join(content)

        else:
            print('Status Error  :', res.status_code)
    except Exception as e :
        print('Detail extract error  ,  ',e)
    else:
        print(title)
        print(content)





if __name__ == '__main__':
    demo()
    #demo2()