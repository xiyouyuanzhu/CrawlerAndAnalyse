from ToolCode.Tinytool import *



def  OriginFenci():
    dict = {}
    pr.open()
    dicConf = GetDicConfig()
    FilePath = dicConf['Testfilepath']
    DicNews = GetDictFromJsonFile(FilePath)
    content = DicNews['content']
    segs = pr.segment(content, pos_english=False, pos_names='child')
    AllList = []
    NamedList = []
    OtherList = []
    for w, c in segs:
        AllList.append(w)
    print(AllList)


def NewFunc():
    # def FuncFenci():
    #     dict = fenci()
    #     print(dict)
    dict = {}
    pr.open()
    dicConf = GetDicConfig()
    FilePath = dicConf['Testfilepath']
    DicNews = GetDictFromJsonFile(FilePath)
    content = DicNews['content']
    segs = pr.segment(content, pos_english=False, pos_names='child')
    AllList = []
    NamedList = []
    OtherList = []
    for w, c in segs:
        if len(w) < 2:
            continue
        else:
            AllList.append(w)
            if c == '地名' or c == '人名':
                NamedList.append(w)
            else:
                OtherList.append(w)
    # print("NameList=",NamedList)
    # print('OtherList=',OtherList)
    print('Alllist=',AllList)
def  ttt():
    for i in range(3,4):
        print(i)
if __name__ == '__main__':
    #NewFunc()
    #OriginFenci()
    ttt()