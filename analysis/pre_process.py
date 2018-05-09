import jieba
import sys
from os import path
import pandas as pd
import gensim

def read_data(filename):
    pd.read_csv(filename)

def clean_content(sentence):
    if sentence != '':
        sentence = sentence.strip()
        in_tab = b''
        out_tab = b''
        trans_tab = bytearray.maketrans(in_tab, out_tab)
        pun_digit = string.punctuation + string.digits
        pun_digit = pun_digit.encode('utf-8')
        sentence = sentence.encode('utf-8')
        sentence = sentence.translate(trans_tab, pun_digit)
        sentence = sentence.decode('utf-8')
        sentence = re.sub('[a-zA-Z0-9]', '', sentence)
        sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", sentence) 
    return sentence

def sent2word(sentence):
    seg_list = jieba.cut(sentence, cut_all=False)
    seg_result = ''
    for word in seg_list:
        if word != '\t':
            seg_result += word + ' '
    return seg_result.strip()

def words2vec(sentence, model):
    vecs = []
    sentence = clean_content(sentence)
    words = sent2word(sentence)
    for word in words:
        word = word.replace('\n', '')
        try:
            vecs.append(model[word])
        except KeyError:
            continue
    return np.array(vecs, dtype='float')

def build_matrix(train_set, model, avg=True):
    x_train = []
    y_train = []
    i = 1
    print("Building matdix....")
    for row in train_set:
        if i % 1000 == 0:
            print("Building matrix at row {}.".format(i))
        i += 1
        if pd.isna(row[0]):
            continue
        vecs = words2vec(row[0], model)
        if len(vecs) > 0:
            if avg:
                vecs_array = sum(np.array(vecs)/len(vecs)) # Use avg to reduce caltulate cost.
                x_train.append(vecs_array)
            y_train.append(int(row[1]))
    return x_train, y_train

def read_model(model_path):
    return gensim.models.KeyedVectors.load_word2vec_format(model_path)
    
    
