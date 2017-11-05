# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 19:32:54 2017

@author: elara
"""

# create corpus 


import pandas as pd
import logging
from gensim import corpora, models
#from gensim.models.ldaseqmodel import LdaSeqModel 
#import numpy as np
import datetime
#from matplotlib import pyplot as plt
import numpy as np
import sys
import re
import codecs
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")

print 'load package done'

# 工作路径
if sys.platform == 'darwin':
    main_path = '/Users/wangzexian/Desktop/dtm/'
    dtm_path = main_path + 'lib/dtm/main_osx'
    fastdtm_path = main_path + 'lib/fastdtm/FastDTM_osx'
elif sys.platform == 'win32':
    main_path = 'C:/Users/elara/Desktop/dtm/' #win
elif sys.platform == 'linux2':
	main_path = '/mnt/c/Users/elara/Desktop/dtm/' 
	dtm_path = main_path + 'lib/dtm/main_linux'
	fastdtm_path = main_path + 'lib/fastdtm/FastDTM_linux'
else:
    print 'System does not meet'

print 'set path done'

# 停用词表

f=open(main_path+'corpus/stop_word')
stop_word=f.read()
f.close()
stop_word = stop_word.split('sperator')
stop_word = [unicode(i,'utf8') for i in stop_word]

print 'load stop word list done'

# 读取分词数据,排除停止词，汇总语料库，content
i=0
content=[]
while 1:
    try:
        print i
        f = open(main_path+ unicode('corpus/output/已分词 ' , "utf8") + str(i)+".txt","r")
        content.append([word for word in [unicode(j,'utf8') for j in f.read().split()] if word not in stop_word and re.search(r'^\d+',word) is None and len(word) > 1 ])
        f.close()
        i = i + 1
    except IOError:
        print 'read raw content done'
        break


#保存content
w=codecs.open(main_path+'corpus/content.txt','w','utf8')
for i in content:
    k=' '.join([j for j in i])
    w.write(k+"\n")
w.close()

print 'save content done'

# 构建字典(使用完整词库）
dictionary_all = corpora.Dictionary(content)
dictionary_all.save(main_path + '/corpus/dictionary_all.dict')

# 序列化
content_bow = [dictionary_all.doc2bow(x) for x in content]  # 原始文本
# tfidf 模型
tfidf = models.TfidfModel(content_bow) # 使用原始文本 1
# 计算文档词tfidf
content_tfidf = tfidf[content_bow] # 一个list，内部嵌套list，每个内部list是一个文档，文档内tuple二元表示id，value


# 排除每个文章中tfidf末尾10%的词
content_train = []
for i in content_tfidf: #对每篇文章
    temp=[]
    value = [x[1] for x in i] #提取tfidf
    th = np.percentile(value,0.10)
    for j in i:
        if j[1]<th:
            continue
        else:
            temp.append(dictionary_all[j[0]])
    content_train.append(temp)

print 'build content_train done'
	
# 划分时间段
raw_content = pd.read_csv(main_path + 'corpus/raw/content_data.csv')

f1_y,f1_m = datetime.datetime.strptime(raw_content.iloc[0,3],'%Y/%m/%d %H:%M:%S').timetuple()[0:2]
s=1
time_series=[]
for i in range(len(raw_content)-1):
    f2_y,f2_m = datetime.datetime.strptime(raw_content.iloc[i+1,3],'%Y/%m/%d %H:%M:%S').timetuple()[0:2]
    if f1_y==f2_y and f1_m==f2_m:
        s=s+1
        f1_y = f2_y
        f1_m = f2_m
    else:
        time_series.append(s)
        s=1
        f1_y = f2_y
        f1_m = f2_m
time_series.append(s)

print 'time series done'

# 保存时间分割点
t=codecs.open(main_path+'corpus/dtm_o/time_series.txt','w','utf8')
k=' '.join([str(j) for j in time_series])
t.write(k)
t.close()

print 'time series saving done'

# dtm语料库转化
class DTMcorpus(corpora.textcorpus.TextCorpus):

    def get_texts(self):
        return self.input

    def __len__(self):
        return len(self.input)

corpus = DTMcorpus(input = content_train)    

corpora.BleiCorpus.serialize(main_path + 'corpus/dtm_o/corpus.lda-c', corpus)

# fastdtm语料库转化

dictionary = corpora.Dictionary(content_train)


# vocabulary_file
d=codecs.open(main_path+'corpus/fastdtm/vocabulary_file.txt','w','utf8')
d.write('\n'.join(dictionary[j] for j in range(len(dictionary))))
d.close()

print 'vocabulary_file done'
#doc

docs = [' '.join([str(word_1) for word_1 in [dictionary.token2id[word] for word in doc]])  for doc in content_train]

start=0
s=0
for count_i in range(len(time_series)):
    end = time_series[count_i] + start
    fd=codecs.open(main_path+'corpus/fastdtm/'+str(count_i)+'.txt','w','utf8')
    fd.write('\n'.join(docs[start:end]))
    fd.close()
    start = end

print 'doc done'




