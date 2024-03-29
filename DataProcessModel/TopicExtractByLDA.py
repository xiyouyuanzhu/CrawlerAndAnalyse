import lda
import pynlpir as pr
from ToolCode.Tinytool import *
import numpy as np
from math import *
#总的词集
logger = Getlloger('LDA running log')

#获取时间段内的新闻 数据集合 为下一步热点初始化做准备
def GetAllcontent():
    strLog='GetAllcontent running'
    print(strLog)
    #dict=GetDicConfig()
    #FilePath = dict['Testfilepath']
    NewsBaseDir = '/home/yuanzhu/Desktop/NewsData/'
    NewsDir=None
    Allcontent=''
    for i in range(3,4):
        if i <10:
            NewsDir=os.path.join(NewsBaseDir,'2019060{}'.format(i))
        else:
            NewsDir=os.path.join(NewsBaseDir,'201906{}'.format(i))
        if os.path.exists(NewsBaseDir):
            pass
        else:
            strLogerr = 'NewsDir :{} is not exist'.format(NewsDir)
            logger.error(strLogerr)
            continue
        strLog = ' NewsDir :{} is operating  '.format(NewsDir)
        print(strLog)
        FileList = os.listdir(NewsDir)
        index=1
        for file in FileList:
            if index>50 :
                break
            FilePath  = os.path.join(NewsDir,file)
            strLog='NewsPath :{} is operating'.format(FilePath)
            print(strLog)
            dict = GetDictFromJsonFile(FilePath)
            content = dict['content'].replace('\n','').replace(' ','')
            if content:
                Allcontent=Allcontent + '\n' + content
            else:
                strLog='NewsPath:{} content is None'.format(FilePath)
                logger.error(strLog)
                print(strLog)
            index+=1

    # dictworld=fenci(Allcontent)
    # WorlList = dictworld['AllList']
    # corpusList=[]
    # for w1 in WorlList:
    #     if w1 not  in corpusList:
    #         corpusList.append(w1)
    # #keys  = dictworld.keys()  dict_keys(['NameList', 'OtherList', 'AllList'])
    # lencorpulist=len(corpusList)
    # strLogdata  ='len(corpulist)={}'.format(lencorpulist)
    # logger.debug(strLogdata)
    if Allcontent:
        return Allcontent
    else:
        strLogerr='AllContent is None  '
        logger.error(strLogerr)
        print(strLogerr)
        exit(1)

#提取 命名实体集
def GetNamedList():
    Allcontent = GetAllcontent()
    dictworld = fenci(Allcontent)
    NamedList = dictworld['NamedList']
    return NamedList

#分词，得到去重后的corpu预料集合，用于后序稀疏矩阵建立
def GetWordList():
    # dict=GetDicConfig()
    # FilePath = dict['Testfilepath']
    # NewsDir = '/home/yuanzhu/Desktop/NewsData/美食'
    # Allcontent = ''
    # FileList = os.listdir(NewsDir)
    # for file in FileList:
    #     FilePath = os.path.join(NewsDir, file)
    #     dict = GetDictFromJsonFile(FilePath)
    #     content = dict['content'].replace('\n', '').replace(' ', '')
    #     if content:
    #         Allcontent = Allcontent + '\n' + content
    #     else:
    #         print('Ｆｉｎｄ空文件')
    Allcontent= GetAllcontent()
    dictworld = fenci(Allcontent)
    WorlList = dictworld['AllList']
    corpusList = []
    for w1 in WorlList:
        if w1 not in corpusList:
            corpusList.append(w1)
    # keys  = dictworld.keys()  dict_keys(['NameList', 'OtherList', 'AllList'])
    lencorpulist = len(corpusList)
    strLogdata = 'len(corpulist)={}'.format(lencorpulist)
    logger.debug(strLogdata)
    return corpusList, Allcontent

#构建获得LDA模型
def get_lda_matrix():
    corpus_list,Allcontent=GetWordList()
    tempcontentList = Allcontent.split('\n')
    Martrix=[]
    for line in tempcontentList:
        if len(line)!=0:
            Per_Matrix = np.zeros(len(corpus_list), dtype=np.int)
            line.strip()
            seg_dict = fenci(line)
            seg_list=seg_dict['AllList']
            for word in seg_list :
                if word in corpus_list:
                    Per_Matrix[corpus_list.index(word)]+=1
            Martrix.append(Per_Matrix)
    countMatrix=np.array(Martrix)
    #print('countMartrix.shape:{}'.format(self.countMatrix.shape))
    #print('countMartrix:{}'.format(self.countMatrix))
    x,y =countMatrix.shape
    strLogdata ='countMatrix shape={},{}'.format(x,y)
    logger.debug(strLogdata)
    return countMatrix

#获得LDA模型
def get_fitModel(n_iter=1500,_alpha=0.1,_eta=0.01):
    model=lda.LDA(n_topics=300,n_iter=n_iter,alpha=_alpha,eta=_eta,random_state=1)
    model.fit(get_lda_matrix())
    return model
#输出主题  词项集合
def print_topic_word(n_top_word=10):
    topic_list=[]  #与每个主题词集合相对应
    model = get_fitModel()
    corpus,_ = GetWordList()

    '''
      for i  ,topic_dist in  enumerate(model.topic_word_):
        topic_words=np.array(corpus).ar
    '''
    topic_word = model.topic_word_
    # topic_word =(20,431)
    # print('topic_word.shape:{}'.format(topic_word.shape))
    strLogdata = 'topic_word.shape={}'.format(topic_word.shape)
    logger.debug(strLogdata)
    ##验证topic word 行向量和为1
    for i in range(0, topic_word.shape[0]):
        temp_sum = np.sum(topic_word[i, :])
        print("temp_sum:{}".format(temp_sum))
    ##打印主题操作 ,取出最相关的10个主题词项
    dictTopic={}
    dicTopicSaveJsonPath = os.path.join(os.getcwd(),'jsonTopic.json')
    namedList =GetNamedList()
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(corpus)[np.argsort(topic_dist)][:-(n_top_word + 1):-1]
        change_dist = np.sort(topic_dist)[:-(n_top_word+1):-1]  #posibility
        #------------算法  剔除不含有命名实体的热点话题-------------------------
        boolIsContainNamed=False
        for world in topic_words:
            if world in namedList:
                boolIsContainNamed=True
                break
            else:
                continue
        if boolIsContainNamed:
            print('World Possibility:{}'.format(change_dist))
            # topic_words_prob=topic_dist[np.argsort(topic_dist)]
            # 测试 topic_words=np.array(corpus)[np.argsort(topic_dist)][::-1]
            topic_list.append(topic_words)
            print('topicNumber:{} topic_list:\n {}'.format(i,topic_words))
            try:
                dictTopic.update({'topicNumber-{}'.format(i):topic_words.tolist()})
            except Exception as e :
                continue



    SaveDictToJsonFile(dictTopic,dicTopicSaveJsonPath)

    return topic_list

#得到每个主题对应的主题词项
def get_topic_word_list():
    topic_list=print_topic_word()
    return topic_list

def print_doc_topic():
    model = get_fitModel()
    # corpus=self.get_corpus_list()
    Martrix = get_lda_matrix()
    doc_topic = model.doc_topic_
    topic_word_list = get_topic_word_list()
    # print('doc_topic.shape:\n{} '.format(doc_topic.shape))
    '''
    for i in range(0,doc_topic.shape[0]):
        for j in range(0,doc_topic.shape[1]):
            print('doc_topic[{}][{}]={}'.format(i,j,doc_topic[i][j]))
    '''
    ##doc_topic .shape 为3*20
    topic_word = model.topic_word_
    for i in range(0, len(Martrix)):
        doc_list = doc_topic[i]
        topic_index = doc_topic[i].argmax()
        # print('doc_topic_probility:{}'.format(doc_list))
        print('topic_index:{}'.format(topic_index))
        # print('doc:{}\n top_topic:{} \n topic_distribution  :{}'.format(i,topic_index,doc_list))
        words = topic_word_list[topic_index]
        print('words___91', words)
        sum_prob = np.sum(doc_topic[i])
        print('sum_probility:{}'.format(sum_prob))
#
# # _______________8.31 日新增代码 测试主题词向量的可行性_________________
# def TTmodel_topic_word():
#     model = get_fitModel()
#     topic_worlds = model.topic_word_
#
#     m = topic_worlds.shape[0]
#     # print(m)
#     # 20
#     all_out = 0  ##所有主题间的相似度值和值
#     for j in range(m):
#         temp_all_out = 0
#         for i in range(j + 1, m):
#             out = 0
#             vec1 = topic_worlds[0]
#             vec2 = topic_worlds[i]
#             print(type(vec1), type(vec2))
#
#             out_up = np.dot(vec1, vec2)
#             out_down = sqrt(np.dot(vec1, vec1) + np.dot(vec2, vec2))
#             # print('out_up{} outdown{}'.format(out_up,out_down))
#             out = out_up / out_down
#             temp_all_out += out
#         all_out += temp_all_out
#         print('{}与其他的主题相似度和值为{}'.format(j, temp_all_out))
#
#     print('all_out', all_out)
#     all_sim_num = m * (m - 1) / 2
#     all_average = all_out / all_sim_num
#     print('all_average', all_average)
#
#     '''
#     for i ,topic_dist in enumerate(topic_worlds):
#         vec1=topic_dist

#    '''

    # __________________________上位新增代码___________________________
if __name__ == '__main__':
   #print_doc_topic()
   print_topic_word()  ##初始化热点，初始化热点 ，并保存在本地，以json文件的方式存储