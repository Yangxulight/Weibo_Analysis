import jieba
import numpy as np
from gensim.models import word2vec
CUT_SYMBOL = '|'

def cut_sentences(sentences, search=False):
    if search:
       seg_list = jieba.cut_for_search(sentence)
    else:
        seg_list = jieba.cut(sentence)
    return CUT_SYMBOL.join(seg_list)

def remove_stopwords(seg_list):
    with open('stopwords.txt') as f:
        stopwords = f.readlines()
    stopwords = [line.strip().decode('utf-8') for line in stopwords]
    stopwords = set(stopwords)
    final_list = []
    for word in seg_list:
        if word not in stopwords:
            final_list.append(word)
    return final_list

def get_word2vec(word_list):
    


