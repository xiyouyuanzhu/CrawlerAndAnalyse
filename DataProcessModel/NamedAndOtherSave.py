from ToolCode .Tinytool import *
import os
def demo1():
    '''
    dict.update({'NameList':NamedList})
    dict.update({'OtherList':OtherList})
    dict.update({'AllList':AllList})
    :return:
    '''
    FileDir='/home/yuanzhu/Desktop/NewsData/美食'
    filelist = os.listdir(FileDir)
    for file in filelist:
        filepath = os.path.join(FileDir,file)
        dictNews=GetDictFromJsonFile(filepath)
        content =dictNews['content']
        dictworld=fenci(content)
        NamedList = dictworld['NamedList']
        OtherList = dictworld['OtherList']
        print('NamedList:',NamedList)
        print('OtherList',OtherList)
    
if __name__ == '__main__':

    demo1()
