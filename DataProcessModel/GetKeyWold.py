import pynlpir as pr
from ToolCode .Tinytool import GetDictFromJsonFile ,Getlloger
import  os

#通过算法获取文本中的关键词集合  调用pynlpir中的getkeywolds来实现。


def controlGetKeyworld():
    logger=Getlloger()
             #以5月1日的新闻为例
    NewsDir='/home/yuanzhu/Desktop/NewsData/20190501/'
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
            logger.error(strLogErr)

    print(allKeysList)#打印所有的关键此项信息
    pr.close()


def GetKeyWorld(filePath):  #使用PYNLPIR getkeywokld来实现
    logger=Getlloger()
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
       logger.error(strLogErr)
       return None
    #print(keywords)
    return keywords

if __name__ == '__main__':
    controlGetKeyworld()