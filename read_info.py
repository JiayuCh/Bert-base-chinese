import jieba
import jieba.posseg as pseg
import pandas as pd
import numpy as np
import json
# import pymysql
import re
import gensim.models as g
# solve probelms encoutered when loading gensim
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')
import time
from operator import itemgetter
from functools import reduce
from gensim import corpora,similarities,models 
from collections import defaultdict
#r = re.compile("[^A-Za-z\+\-*/|\%^=()（）<>.\u4e00-\u9fa5\u0370-\u03ff]*")
r = re.compile("[^\u4e00-\u9fa5A-Za-z+\-*/|\%^=]")
#匹配中文和英文字母
stopwords=[line.strip() for line in open('data/stopwords.txt').readlines()] 
def textParse(sentence):
    '''
    1、对句子进行正则匹配;2、结巴分词;3、去除停用词
    '''
    sentenc=r.sub('',sentence)
    texts = list(jieba.cut(sentenc))
    text = [word for word in texts if word not in stopwords]
    return text
print(stopwords)
test_sentence = "加几个特fsadgfasd殊符号试试()（）.1+3-5*1=35"
print(textParse(test_sentence))
r_num = re.compile("[^A-Za-z0-9\+\-*/|\%^=()（）<>.\u4e00-\u9fa5\u0370-\u03ff]*")
def find_num(sentence):
    '''
    与text_Parse相比加上数字
    '''
    sentenc=r_num.sub('',sentence)
    texts = list(jieba.cut(sentenc))
    text = [word for word in texts if word not in stopwords]
    return str(text)
def num(x):
    '''
    找到所有数字返回list
    '''
    y = re.findall("[\d+][\.\d*]*",x)
    return (y)
#subject-id 1-语文 2-数学 3-英文 4-物理 5-化学 6-生物 7-NA 8-历史 9-地理 10-政治
def read_info(tk):
    # 读取文件
    tk_info = pd.read_csv(tk)
    # 选取数学题
    tk_info = tk_info[tk_info['subject_id'] == 1]
    #tk_info = tk_info[tk_info['grade_group_id'] == 2]
    # 处理文件
    tk_info = tk_info.dropna(subset = ['content'])
    tk_info = tk_info.reset_index(drop = True)
    tk_info = tk_info.loc[:, ['que_id', 'content', 'analysis', 'subject_id','grade_group_id','knowledge']].copy()
    tk_info = tk_info.fillna(' ')
    # 将习题内容和解答连接（训练时没用这个）
    tk_info['text'] = tk_info['content'] + tk_info['analysis']
    #tk_info['text'] = tk_info['text'].apply(lambda x:reduce(lambda x,y:x+y, re.findall(r'[\u4e00-\u9fa5\u0370-\u03ff_a-zA-Z0-9^*/|\%=()\（\）\+\-\.><]',x)))
    # 知识点json格式解码
    tk_info['knowledge'] = tk_info['knowledge'].apply(lambda x: json.loads(x))
    # 对习题内容进行处理（不含数字）
    tk_info['content_cut'] = tk_info['content'].apply(lambda x:textParse(x))
    # 对习题内容进行处理（包含数字）
    tk_info['content_num'] = tk_info['content'].apply(lambda x:find_num(x))
    # 对习题内容进行处理（只含数字）
    tk_info['num'] = tk_info['content'].apply(lambda x:num(x))
    tag_list = []
    for i in range(len(tk_info)):
        for j in tk_info['knowledge'][i].keys():
            tk_info['knowledge'][i][j] = set(tk_info['knowledge'][i][j])
            if tk_info['knowledge'][i][j] not in tag_list:
                tag_list.append(tk_info['knowledge'][i][j])
    tk_info['tag_1'] = tk_info['knowledge'].apply(lambda x:x.get('1'))
    tk_info['tag_2'] = tk_info['knowledge'].apply(lambda x:x.get('2'))
    tk_info['tag_3'] = tk_info['knowledge'].apply(lambda x:x.get('3'))
    tk_info['tag_4'] = tk_info['knowledge'].apply(lambda x:x.get('4'))
    tk_info['tag_5'] = tk_info['knowledge'].apply(lambda x:x.get('5'))
    return tk_info