from gensim.models import word2vec
import jieba
class WORD2VEC():
    def __init__(self):
        self.filename='out.txt'
        self.test_word2vec_filename='test_word2vec.txt'

    def get_model(self):
        sentences=word2vec.Text8Corpus('text8.txt')
        model=word2vec.Word2Vec(sentences=sentences,size=200)
        model.save('PRO.model')

    def get_corpus(self):
        with open(self.filename,'r')as f:
            lines=f.readlines()
            temp_text=''.join(lines)
        seg_list=jieba.cut(temp_text,cut_all=True)
        seg=' '.join(seg_list)
        #print(seg)
        with open(self.test_word2vec_filename,'wb')as f:
            seg=seg.encode('utf-8')
            f.write(seg)
    def test_word2vec(self):
        #self.get_corpus()
        #sentences=word2vec.Text8Corpus(self.english_text_file)
        #model=word2vec.Word2Vec(sentences=sentences,size=200)
        # print(model)
        model_1=word2vec.Word2Vec.load("PRO.model")
        print('model',model_1)
        try:
            y1=model_1.similarity('woman','man')
        except KeyError:
            y1=0
        print('woman and  man  相似度',y1)
        try:
            y2=model_1.most_similar('woman',topn=8)
        except KeyError:
            y2=0
        for word in y2:
            print('word[0]:{},word[1]:{}'.format(word[0],word[1]))
            print('y2:',y2)

if __name__ == '__main__':
    test=WORD2VEC()
    #print(test.get_corpus())

    # test.get_model()
    test.test_word2vec()