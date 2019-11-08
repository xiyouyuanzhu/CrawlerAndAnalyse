
#Author  YZ
#Time 2019-11-8
#Func Crawler And Analyse Syestem Consol
import getopt
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from CrawlerMOdel.CrawTopicNews import *
from DataProcessModel.GetKeyWoldByPynlpir import *
def showUsage(execFileName='CAASC.sh',boolErrFlg=False):
    if boolErrFlg:
        out =sys.stderr
        out.write('Command not Fount \n')
    else:
        out = sys.stdout
    out.write('\n Usage :{} option ...\n')
    out.write('Crawler And Analyse  Sysetem Consol,CAASC \n')
    out.write('Opthions:\n')
    out.write('-h  --help      print help message,\n')
    out.write('-c  --cmd       excute Crawler And Analyse Systen command,\n')
    out.write('......,se,-----------Start extract news,\n')
    out.write('......,sa,-----------Start analyse hot info, \n')
    out.write('...... , --StartDate       指定新闻开始日期,\n')
    out.write('...... , --EndDate         指定新闻结束日期,\n')
    out.write('...... , --Topic           指定要抓取的新闻主题,\n')
    out.write('......CAASC.sh ,  --cmd se --Topic [InputTopic] , \n')
    out.write('......CAASC.sh ,  --cmd sa --StartDate [InputStartDate]  , --EndDate [InputEndDate]  \n')

'''
/home/yuanzhu/anaconda3/bin/python ControlModul.py  --cmd se --StartDate 20190909  --EndDate 20190915  
   
   opts= [('--cmd', 'se'), ('--StartDate', '20190909'), ('--EndDate', '20190915')] args= []
'''
def StartExtract(TopicWord):
    #print('Start Extract Running ,topic={}'.format(TopicWord))
    print('新闻爬取系统启动------>  新闻主题：{}\n'.format(TopicWord))
    FuncStartExtract(TopicWord)

def StartAnalyse(StartDate, EndDate):
    #print('Start Analyse Running, StartDate:{}  EndDate :{}'.format(StartDate,EndDate))
    print('新闻热点提取系统启动------>  起始时间：{}   截止时间：{}\n'.format(StartDate,EndDate))
    FuncStartAnalyse(StartDate,EndDate)


def parseCommand():
    execFileName='ControlModel'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "cmd=", "StartDate=", "EndDate=", "Topic="])
        # print('opts=',opts,'args=',args)
    except getopt.GetoptError:
        showUsage(execFileName,True)
        sys.exit(1)
    if len(opts)==0:
        showUsage(execFileName,True)
        sys.exit(1)

    cmdTarget = None
    StartDate=None
    EndDate=None
    TopicWord=None
    for cmdName,cmdValue in opts:
        if 'cmd' in cmdName:
            cmdTarget=cmdValue
        if 'StartDate' in cmdName:
            StartDate=cmdValue
        if 'EndDate' in cmdName:
            EndDate=cmdValue
        if 'Topic' in cmdName:
            TopicWord=cmdValue
    #  如果输入为help则输入帮助信息
    if not cmdTarget:
        showUsage()
        exit(1)
    #
    # print('cmd=',cmdTarget)
    # print('StartDate=',StartDate)
    # print('EndDate=',EndDate)
    # print('TopicWord=',TopicWord)
    if cmdTarget=='se':
        if TopicWord=='':
            showUsage()
            exit(1)
        if StartDate or EndDate:
            showUsage()
            print('False 1')
            exit(1)
    if  cmdTarget=='sa' :
        if not ( StartDate and EndDate):
            showUsage()
            print('False 2')
            exit(1)
        if  TopicWord :
            showUsage()
            print('Flase 3')
            exit(1)
    if cmdTarget=='se':
        StartExtract(TopicWord)
    elif cmdTarget=='sa':
        if int(StartDate)>int(EndDate):
            strLogerr = '输入日期有误'
            sys.stderr.write(strLogerr)
            showUsage()
            exit(1)
        StartAnalyse(StartDate,EndDate)





def LocalTest():
    opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "cmd=", "StartDate=", "EndDate=","Topic="])
    print('opts=', opts, 'args=', args)
    # if 'h' or 'help' in opts[0]:
    #     showUsage()


if __name__ == '__main__':
    parseCommand()
    #LocalTest()
    #showUsage()