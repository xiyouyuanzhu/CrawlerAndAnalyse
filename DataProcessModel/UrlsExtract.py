#Author  YZ
#Func 实验验证网页中含有的杂质链接，为了提高抓取链接的效率，虽然编写特定模板能够准确的抓取到指定链接，效率偏低而且会有遗漏，为了
#提高抓取链接的效率以及准确率，按照链接的域名进行区分，使用EdetDistance筛选出阈值低的链接。
#Time 19-11-7
import requests
from scrapy.selector import Selector
from ToolCode.Edit_distance import  get_edit_distance
def demo1():
    url =  'http://www.chinanews.com/scroll-news/news1.html'
    res = requests.get(url)
    urlmodel='www.chinanews.com/tp/hd2011/2019/11-06/912423.shtml'
    if res.status_code==200:
        res.encoding='utf-8'
        selector= Selector(text=res.text)
        urlList = selector.xpath('//a/@href').extract()
        for tmepurl in urlList:
            print(tmepurl)
            get_edit_distance(urlmodel,tmepurl)
    pass
if __name__ == '__main__':
    demo1()

