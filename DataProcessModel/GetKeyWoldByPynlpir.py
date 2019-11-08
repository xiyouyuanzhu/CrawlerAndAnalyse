import pynlpir as pr
from ToolCode .Tinytool import GetDictFromJsonFile ,Getlloger
import  os

#通过算法获取文本中的关键词集合  调用pynlpir中的getkeywolds来实现。


def FuncStartAnalyse(StartDate="20190615",EndDate="20190625"):
    NewsBaseDir ='/home/yuanzhu/Desktop/NewsData/'
    year = StartDate[0:4]
    sm=StartDate[4:6]
    sd=StartDate[6:]
    em=EndDate[4:6]
    ed=EndDate[6:]

    #分两种情况考虑，分两个月份相同和不同两种情况。
    if sm==em:
        cday  =int(ed)-int(sd)
        for i in range(0,cday+1):
            day = int(sd)+i
            if day<10:
                day = "0{}".format(day)
            else:
                day  =str(day)
            TargetYearDay = '{}{}{}'.format(year, sm, day) # year 为年， sm 开始月份，day  为几号
            FileDir = os.path.join(NewsBaseDir, TargetYearDay)
            controlGetKeyworld(FileDir) #新闻保存目录
    else:
        pass



def controlGetKeyworld(NewsDir):

             #以5月1日的新闻为例
    #NewsDir='/home/yuanzhu/Desktop/NewsData/20190501/'
    newsList=os.listdir(NewsDir)
    allKeysList=[]
    for news in newsList:
        filepath = os.path.join(NewsDir,news)
        if os.path.exists(filepath):
            keyworlds=GetKeyWorld(filepath)
            if keyworlds:
                allKeysList.append(keyworlds)
            else:
                continue
        else:
            strLogErr='{} is not exist'.format(filepath)

    print(allKeysList)#打印所有的关键此项信息
    pr.close()


def GetKeyWorld(filePath):  #使用PYNLPIR getkeywokld来实现
    #filePath='/home/yuanzhu/Desktop/NewsData/20190603/20190603419.json'
    try:
        pr.open()
        #filePath='/home/yuanzhu/Desktop/NewsData/20190501/20190501181.json'
        dicNews=GetDictFromJsonFile(filePath)
        content=dicNews['content']
        # segs=pr.segment(content)
        # for seg in segs:
        #     print(seg)
        tupkeywords=pr.get_key_words(content,weighted=True)  #使用TF-IDF算法提取关键词（貌似还挺有效果）
        keywords=[]
        for i,w in enumerate(tupkeywords):
            keywords.append(w[0])
            if i ==9:
                break
            i+=1
    except Exception as e :
       strLogErr='Get  {}  keyworld error :{}'.format(filePath,e)
       print(strLogErr)
       return None
    print("FilePath=",filePath)
    print('获取热点：',keywords)
    return keywords

if __name__ == '__main__':
    #controlGetKeyworld()
    # keys =GetKeyWorld('/home/yuanzhu/Desktop/NewsData/20190603/20190603419.json')
    # print('keyword= ',keys)
    FuncStartAnalyse()