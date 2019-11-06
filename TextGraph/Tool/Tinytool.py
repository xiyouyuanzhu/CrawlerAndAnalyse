import json
import os
import logging
import pynlpir as pr
#将Dic对象保存为本地Json文件
def SaveDictToJsonFile(model,FilePath):
    with open(FilePath, 'w', encoding='utf-8') as json_file:
        json.dump(model, json_file, ensure_ascii=False)

#从本地读取Json文件为Dict对象
def GetDictFromJsonFile(FilePath):
    dict = {}
    #FilePath = '/home/yuanzhu/Desktop/NewsData/20190918/201909180.json'
    with open(FilePath, 'r', encoding='utf-8') as f:
        dict = json.load(f)
    return dict

##追加Log信息
#可配置，配置信息为Log日志名称以及Log日志存放地点
def Getlloger(logname):
    loggerpath=os.path.join(os.getcwd(),os.pardir,'DataProcessModel','{}.txt'.format(logname))
    logger = logging.getLogger("loggingmodule.NomalLogger")
    handler = logging.FileHandler(loggerpath)
    formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

#分词以及去除停留词项仅保留动名词
def fenci(content):
    dict={}
    # pr.open()
    # dicConf=GetDicConfig()
    # FilePath=dicConf['Testfilepath']
    # DicNews=GetDictFromJsonFile(FilePath)
    # content=DicNews['content']
    pr.open()
    segs=pr.segment(content,pos_english=False,pos_names='child')
    AllList=[]
    NamedList=[]
    OtherList=[]
    for w,c in segs:
        if len(w)<2:
            continue
        else:
            AllList.append(w)
            if c=='地名' or c=='人名':
                NamedList.append(w)
            else:
                OtherList.append(w)
    #print("NameList=",NamedList)
    #print('OtherList=',OtherList)
    #print('Alllist=',AllList)
    dict.update({'NameList':NamedList})
    dict.update({'OtherList':OtherList})
    dict.update({'AllList':AllList})
    pr.close()
    return  dict

##保存配置文件
def SaveConfig():
    dicConf={}
    configPath=os.path.join(os.getcwd(),os.pardir,'ConfigModel','conf.json')
    if os.path.exists(configPath):
        pass
    else:
        filedir='/home/yuanzhu/Desktop/NewsData/'
        Testfilepath='/home/yuanzhu/Desktop/NewsData/20190501/201905015.json'
        dicConf.update({'filedir':filedir})
        dicConf.update({'Testfilepath':Testfilepath})
        SaveDictToJsonFile(dicConf,configPath)
#读取配置文件DicConfig
def GetDicConfig():
    confPath=os.path.join(os.getcwd(),os.pardir,'ConfigModel','conf.json')
    try:
        dicConf = GetDictFromJsonFile(confPath)
    except Exception as e :
        strLogErr='Get Config error :{}'.format(e)
        print(strLogErr)
        exit(1)
    return dicConf
if __name__ == '__main__':
    #以2019年5月1日的信息为例 /home/yuanzhu/Desktop/NewsData/20190501
    fenci()
