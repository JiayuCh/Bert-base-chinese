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
