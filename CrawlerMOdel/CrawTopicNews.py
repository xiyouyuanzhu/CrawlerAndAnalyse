from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from ToolCode .Tinytool import  *
from  pyquery import PyQuery as pq
from scrapy.selector import Selector
import requests
import re
import os
# def demo1():
#     browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
#     url = 'http://www.chinanews.com/scroll-news/news1.html'
#     browser.get(url)
#     input=browser.find_element_by_css_selector('#q')
#     input.send_keys('特朗普')
#     button=browser.find_element_by_css_selector('.search_a')
#     button.click()
#     time.sleep(2)
#     print(browser.page_source)
'''
    next_click.click()  # 模拟点击下一页的时候，会出现一个新窗口或者新标签
    n = drive.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
    print('当前句柄: ', n)  # 会打印所有的句柄
    drive.switch_to_window(n[-1])  # driver切换至最新生产的页面
'''
def Start():
    url = 'http://www.chinanews.com/scroll-news/news1.html'
    TopicWorld ='美食'
    chromedriver_path='/usr/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs",
                                    {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
    options.add_experimental_option('excludeSwitches',
                                    [
                                        'enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    wait = WebDriverWait(browser, 10)  # 超时时长为10s
    browser.get(url)
    input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#q')))
    submit = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.search_a')))
    #清空表单里面的内容
    input.clear()
    # 输入主题词项
    input.send_keys(TopicWorld)   #***************关键词
    time.sleep(1)
    submit.click()
    n = browser.window_handles
    #print('n',n)
    browser.switch_to_window(n[-1])  #切换标签页
    SaveFileDir ='/home/yuanzhu/Desktop/NewsData/{}'.format(TopicWorld)
    if os.path.exists(SaveFileDir):
        pass
    else:
        os.mkdir(SaveFileDir)
    index = 12
    ExtractPageUrl(browser,SaveFileDir,index,TopicWorld)

    browser.close()

def  ExtractPageUrl(browser,SaveFileDir,index,topic):
    time.sleep(2)
    wait = WebDriverWait(browser, 10)  # 超时时长为10s
    good_total = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#news_list')))  # 加载主题新闻核心内容
    next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pagediv > a:nth-child(12)')))
    items = browser.find_elements_by_xpath('//ul[@class="news_item"]')
    for item in items:
        try:
            title = item.find_element_by_xpath('./li[@class="news_title"]').text
            href = item.find_element_by_xpath('./li[@class="news_title"]/a').get_attribute('href')
            #content = item.find_element_by_xpath('./li[@class="news_content"]').text
            dict = ExtractDetail(href)
            dict.update({'url':href})
            index=index+1
            SaveFilePath = os.path.join(SaveFileDir, '{}{}.json'.format(topic,index))
            if os.path.exists(SaveFilePath):
                continue
            SaveDictToJsonFile(dict,SaveFilePath)
            '''
            recordcode.text  得到文本内容
            '''
            '''
            get_attribute('')方法
            get_attribute('href'):获取href属性值
            get_attribute('id'):获取id属性值
            '''
        except Exception as e:
            continue
        # print('title=', title)
        # print('href=', href)
        print('{} {} save successful'.format(href,title))
        time.sleep(1)
    next_button.click()
    # n = browser.window_handles
    # print('n',n)
    # browser.switch_to_window(n[-1])  # 切换标签页
    # SaveFilePath= os.path.join(SaveFileDir,'{}.json'.format(index+1))
    ExtractPageUrl(browser,SaveFileDir,index,topic)

## 提取新闻网页内容
def ExtractDetail(url):
    #url='http://www.chinanews.com/sh/2019/05-02/8826407.shtml'
    try:
        dict={}
        res=requests.get(url)
        if res.status_code==200:
            res.encoding='utf-8'
            html=res.text
            selector=Selector(text=html)
            title=selector.xpath('//h1/text()').extract()[0]
            content=selector.xpath('//div[@class="left_zw"]/p/text()').extract()
            content=''.join(content)
            time = selector.xpath('//div[@class="left-t"]/text()').extract_first()
            if '来源' in time:
                time = time.replace('来源：','')
            else:
                pass
        else:
            print('Status Error  :', res.status_code)
    except Exception as e :
        print('Detail extract error  ,  ',e)
        return None
    else:
        print("title  :",title)
        print("content  :",content)
        print('time:',time)
        dict.update({'time':time})
        dict.update({'title':title})
        dict.update({'content':content})
    return dict
if __name__ == '__main__':
    Start()