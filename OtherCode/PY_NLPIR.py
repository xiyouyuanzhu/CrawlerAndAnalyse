import pynlpir as pr
###分词器

def test():
    pr.open()#打开分词器
    s='中美联手破获特大跨国走私武器弹药案近日，中美执法部门联手成功破获特大跨国走私武器弹药案，在中国抓获犯罪嫌疑人２３名，缴获各类枪支９３支、子弹５万余发及大量枪支配件。在美国抓获犯罪嫌疑人３名，缴获各类枪支１２支。' \
      '这是公安部与美国移民海关执法局通过联合调查方式侦破重大跨国案件的又一成功案例。'
    items= pr.segment(s)
    verb_list=[]
    for item in items:
        #print('{}\t \t词性为{}'.format(item[0],item[1]))
        if item[1]=='verb':
            verb_list.append(item[0])
            print('{} save to verb_list '.format(item))
    pr.close()
    print('长度为{}'.format(len(verb_list)))
    print(verb_list)
def test1():
    s = '中美联手破获特大跨国走私武器弹药案近日，中美执法部门联手成功破获特大跨国走私武器弹药案，在中国抓获犯罪嫌疑人２３名，缴获各类枪支９３支、子弹５万余发及大量枪支配件。在美国抓获犯罪嫌疑人３名，缴获各类枪支１２支。' \
        '这是公安部与美国移民海关执法局通过联合调查方式侦破重大跨国案件的又一成功案例。'
    pr.open()
    #保留除了数字还有标点以外的所有的词语
    items=pr.segment(s,pos_english=False)
    Target_list=[]
    for item in items:
        if item[1]=='动词' or item[1]=='名词':
            Target_list.append(item[0])
            pr########sdfgsdfaasdint('{} save to list'.format(item[0]))

    print('长度{} \n 内容\n{}'.format(len(Target_list),Target_list))




def main():
    test1()
if __name__=="__main__":
    main()