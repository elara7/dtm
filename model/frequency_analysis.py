# -*- coding: utf-8 -*-
"""
Created on Sun Nov 05 20:42:16 2017

@author: elara
"""



import pandas as pd
from collections import defaultdict
import logging
from gensim import corpora, models
#from gensim.models.ldaseqmodel import LdaSeqModel 
#import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")



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
    
i=0
content=[]
f=open(main_path+'corpus/content.txt','r')
while 1:
    print i
    temp = f.readline()
    if temp == '':
        print 'read content done'
        f.close()
        break
    content.append(temp.split())
    i = i + 1
    
# 词频统计
frequency = defaultdict(int)
for text in content:
    for token in text:
        frequency[token] += 1

# 词频分布统计
fre_values= frequency.values()
t1 = sorted(frequency.iteritems(), key=lambda x:-x[1])[:10]
# 词频排名前十
print pd.DataFrame(t1)
# 总词个数
sum(fre_values)
# 总词数
len(frequency)
# 最小词频
min(fre_values)
# 词频中位数
np.median(fre_values)
# 词频均值
np.mean(fre_values)
# 词频图
bins = np.arange(0,100,1)
plt.hist(frequency.values(),bins=bins,alpha=0.5)
plt.xlabel(unicode('frequency',"utf8"))
plt.ylabel(unicode('count',"utf8"))
# 只出现一次的词个数
s=0
for i in fre_values:
    if i==1:
        s=s+1
print s,float(s)/float(len(frequency))

# 排除只出现一次的词为content1
content1 = [[token for token in text if frequency[token] > 1] for text in content]

dictionary_all = corpora.Dictionary(content)

# 序列化
content_bow = [dictionary_all.doc2bow(x) for x in content]  # 原始文本
# tfidf 模型
tfidf = models.TfidfModel(content_bow) # 使用原始文本 1
# 计算文档词tfidf
content_tfidf = tfidf[content_bow] # 一个list，内部嵌套list，每个内部list是一个文档，文档内tuple二元表示id，value

# 探索最长文档的tfidf结构
lll = [len(x) for x in content_tfidf]
lll.index(max(lll)) # 11058
tfidf_11058 = [x[1] for x in content_tfidf[11058]]
max(tfidf_11058)
bins = np.arange(0,0.2,0.001)
plt.hist(tfidf_11058,bins=bins)
np.median(tfidf_11058)
np.percentile(tfidf_11058,0.25)

uni_11058=[]
for i in content_tfidf[11058]:
    uni_11058.append((dictionary_all[i[0]],i[1]))
df_11058=pd.DataFrame(uni_11058)
df_11058=df_11058.sort_values(1,ascending=[False])

        


