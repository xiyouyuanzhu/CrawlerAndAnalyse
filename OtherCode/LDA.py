import jieba
import lda
import numpy as np
from math import *
class LDA():
    def __init__(self):
        self.filename='out.txt'
        self.corpus_list=[]
        self.stop_word_list=[]
        self.countMatrix=None
        self.topics=20
        self.model=None
        self.topic_list=[]
    def get_corpus_list(self):
        with open(self.filename,'r')as f :
            lines=f.readlines()
            test=''.join(lines)
        seg_list=jieba.cut(test,cut_all=True)
        with open('tingyongci.txt','r')as f :
            lines=f.readlines()
            for line in  lines:
                line.strip()
                self.stop_word_list.append(line)
        for word in seg_list:
            if word!=' ':
                if word not in self.stop_word_list:
                    if word not in self.corpus_list:
                        self.corpus_list.append(word)
                        #print('word {} append to corpus success'.format(word))
        return self.corpus_list
    def get_lda_matrix(self):
        corpus_list=self.get_corpus_list()
        Martrix=[]
        with open(self.filename,'r')as f :
            lines=f.readlines()
            for line in lines:
                Per_Matrix = np.zeros(len(corpus_list), dtype=np.int)
                line.strip()
                seg_list=jieba.cut(line,cut_all=True)
                for word in seg_list :
                    if word in corpus_list:
                        Per_Matrix[corpus_list.index(word)]+=1
                Martrix.append(Per_Matrix)
        self.countMatrix=np.array(Martrix)
        #print('countMartrix.shape:{}'.format(self.countMatrix.shape))
        #print('countMartrix:{}'.format(self.countMatrix))
        return self.countMatrix
    def get_fitModel(self,n_iter=1500,_alpha=0.1,_eta=0.01):
        self.model=lda.LDA(n_topics=self.topics,n_iter=n_iter,alpha=_alpha,eta=_eta,random_state=1)
        self.model.fit(self.get_lda_matrix())
        return self.model

    def  print_topic_word(self,n_top_word=5):
        model=self.get_fitModel()
        corpus=self.get_corpus_list()

        '''
          for i  ,topic_dist in  enumerate(model.topic_word_):
            topic_words=np.array(corpus).ar
        '''
        topic_word=model.topic_word_
        #topic_word =(20,431)
        #print('topic_word.shape:{}'.format(topic_word.shape))

        ##验证topic word 行向量和为1
        for i in range(0,topic_word.shape[0]):
            temp_sum=np.sum(topic_word[i,:])
            print("temp_sum:{}".format(temp_sum))
        ##打印主题操作 ,取出最相关的5个主题
        for  i ,topic_dist in enumerate(topic_word):
            topic_words=np.array(corpus)[np.argsort(topic_dist)][:-(n_top_word+1):-1]
            change_dist=np.sort(topic_dist)[:-():]
            print('chage_dist:{}'.format(change_dist))
            #topic_words_prob=topic_dist[np.argsort(topic_dist)]
           #测试 topic_words=np.array(corpus)[np.argsort(topic_dist)][::-1]
            self.topic_list.append(topic_words)
            #print('topic{} topic_list:\n {}'.format(i,topic_words))
    def get_topic_word_list(self):
        self.print_topic_word()
        return self.topic_list


    def print_doc_topic(self):
        model=self.get_fitModel()
        #corpus=self.get_corpus_list()
        Martrix=self.get_lda_matrix()
        doc_topic=model.doc_topic_
        topic_word_list=self.get_topic_word_list()
        #print('doc_topic.shape:\n{} '.format(doc_topic.shape))
        '''
        for i in range(0,doc_topic.shape[0]):
            for j in range(0,doc_topic.shape[1]):
                print('doc_topic[{}][{}]={}'.format(i,j,doc_topic[i][j]))
        '''
        ##doc_topic .shape 为3*20
        topic_word=model.topic_word_
        for i in range(0,len(Martrix)):
            doc_list=doc_topic[i]
            topic_index=doc_topic[i].argmax()
            #print('doc_topic_probility:{}'.format(doc_list))
            print('topic_index:{}'.format(topic_index))
            #print('doc:{}\n top_topic:{} \n topic_distribution  :{}'.format(i,topic_index,doc_list))
            words=topic_word_list[topic_index]
            print('words___91',words)
            sum_prob=np.sum(doc_topic[i])
            print('sum_probility:{}'.format(sum_prob))

    # _______________8.31 日新增代码 测试主题词向量的可行性_________________
    def test_model_topic_word(self):
        model = self.get_fitModel()
        topic_worlds = model.topic_word_

        m=topic_worlds.shape[0]
        #print(m)
            #20
        all_out=0##所有主题间的相似度值和值
        for j in range(m):
            temp_all_out = 0
            for i in range(j+1,m):
                out=0
                vec1=topic_worlds[0]
                vec2=topic_worlds[i]
                print(type(vec1),type(vec2))

                out_up=np.dot(vec1,vec2)
                out_down= sqrt(np.dot(vec1,vec1)+np.dot(vec2,vec2))
                #print('out_up{} outdown{}'.format(out_up,out_down))
                out=out_up/out_down
                temp_all_out +=out
            all_out+=temp_all_out
            print('{}与其他的主题相似度和值为{}'.format(j,temp_all_out))

        print('all_out',all_out)
        all_sim_num=m*(m-1)/2
        all_average=all_out/all_sim_num
        print('all_average',all_average)




        '''
        for i ,topic_dist in enumerate(topic_worlds):
            vec1=topic_dist
        
        '''




        # __________________________上位新增代码___________________________

def test_model():
    t=LDA()
    t.test_model_topic_word()


def test_point_():
    a1=np.array([1,2,3])
    a2=np.array([2,2,2])
    o=np.dot(a1,a2)
    print(o)
if __name__ == '__main__':
    #test_point_()
    test_model()
    #test=LDA()
    #list=test.get_corpus_list()
    #print(len(list))
    #test.print_topic_word()
    #test.print_doc_topic()
    #print( test.get_topic_word_list())