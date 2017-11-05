# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 19:32:54 2017

@author: elara
"""

# create corpus 


import logging
from gensim import corpora, models
from gensim.models.wrappers.dtmmodel import DtmModel
#from gensim.models.ldaseqmodel import LdaSeqModel 
#import numpy as np
#from matplotlib import pyplot as plt
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")


#参数
num_topics = int(sys.argv[1])

# 工作路径
if sys.platform == 'darwin':
    main_path = '/Users/wangzexian/Desktop/dtm/'
    dtm_path = main_path + 'lib/dtm/main_osx'
    fastdtm_path = main_path + 'lib/fastdtm/FastDTM_osx'
elif sys.platform == 'win32':
    main_path = 'C:/Users/elara/Desktop/dtm/' #win
    dtm_path = main_path + 'lib/dtm/dtm-win64.exe'
elif sys.platform == 'linux2':
	main_path = '/mnt/c/Users/elara/Desktop/dtm/' 
	dtm_path = main_path + 'lib/dtm/main_linux'
	fastdtm_path = main_path + 'lib/fastdtm/FastDTM_linux'
else:
    print 'System does not meet'

# 读取语料

corpus = corpora.BleiCorpus(main_path + 'corpus/dtm_o/corpus.lda-c')

# 读取时间段

t=open(main_path+'corpus/dtm_o/time_series.txt','r')
time_series =[int(i) for i in t.read().split()]
t.close()
# 建模

model_gen = DtmModel(dtm_path, corpus, time_series, num_topics=num_topics
                 , initialize_lda=True)

# model_gen = LdaSeqModel(corpus = corpus, time_slice=time_series, id2word = dictionary, num_topics = num_topics)

model_gen.save(main_path + 'result/dtm_o_' + sys.platform + '_topic_' + str(num_topics) + '.model')
#model1 = DtmModel.load('topic1.model')
#topics = model1.show_topic(topicid=0, time=0, topn=10)

#for i in range(10):
#    print pd.DataFrame(model.show_topic(topicid=i, time=1, topn=10))

#corpora.textcorpus.TextCorpus(5)