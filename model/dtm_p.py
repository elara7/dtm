# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 19:32:54 2017

@author: elara
"""

# create corpus 


from gensim.models import ldaseqmodel
from gensim import corpora
import sys

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")

#参数
para={
	'num_topics':100,
	'initialize':'gensim',
	'em_min_iter':6,
	'em_max_iter':20,
	'lda_inference_max_iter':25,
	'alpha':0.01,
    'top_chain_var':0.005, # 话题k在t时候的beta是均值为t-1时候beta，方差为该参数的正态分布决定，var越小越稳定，越大则可能发现新话题
    'obs_variance':0.5,
    'passes':10,
    'chunksize':100
}

print 'input topic num'
para['num_topics'] = int(raw_input())
print 'use default?(Y/N)'
use_default = raw_input()
if use_default != 'Y':
	while 1:
		print 'which parameter need to be changed?'
		key_para=raw_input()
		if key_para =='':
			print 'config done'
			break
		print 'input the value'
		if key_para in ('em_min_iter','em_max_iter','lda_inference_max_iter','passes','chunksize'):
			para[key_para]=int(raw_input())
		elif key_para in ('alpha','top_chain_var','obs_variance'):
			para[key_para]=float(raw_input())
		elif key_para in ('initialize'):
			para[key_para]=raw_input()

# 工作路径
if sys.platform == 'darwin':
    main_path = '/Users/wangzexian/Desktop/dtm/'
    dtm_path = main_path + 'lib/dtm/main_osx'
    fastdtm_path = main_path + 'lib/fastdtm/FastDTM_osx'
elif sys.platform == 'win32':
    main_path = 'D:/Desktop/dtm/' #win
    dtm_path = main_path + 'lib/dtm/dtm-win64.exe'
elif sys.platform == 'linux2':
	main_path = '/mnt/d/Desktop/dtm/' 
	dtm_path = main_path + 'lib/dtm/main_linux'
	fastdtm_path = main_path + 'lib/fastdtm/FastDTM_linux'
else:
    print 'System does not meet'

# 读取语料

#corpus = corpora.BleiCorpus(main_path + 'corpus/dtm_o/corpus.lda-c')

content_train=[]
t=open(main_path+'corpus/content_train.txt','r')
while 1:
	temp = t.readline()
	if temp == '':
		break
	content_train.append([unicode(i,'utf8') for i in temp.split()])
t.close()

print len(content_train)

print 'load corpus done'

# dtm语料库转化
class DTMcorpus(corpora.textcorpus.TextCorpus):

    def get_texts(self):
        return self.input

    def __len__(self):
        return len(self.input)

corpus = DTMcorpus(input = content_train)    

print 'convert corpus done'

# 读取时间段

t=open(main_path+'corpus/dtm_o/time_series.txt','r')
time_series =[int(i) for i in t.read().split()]
t.close()
# 建模

model_gen = ldaseqmodel.LdaSeqModel(corpus=corpus, time_slice=time_series, id2word=corpus.dictionary, alphas=para['alpha'], 
 num_topics=para['num_topics'], initialize=para['initialize'], sstats=None, lda_model=None, 
 obs_variance=para['obs_variance'], 
 chain_variance=para['top_chain_var'], passes=10, random_state=None, 
 lda_inference_max_iter=para['lda_inference_max_iter'], 
 em_min_iter=para['em_min_iter'], em_max_iter=para['em_max_iter'], 
 chunksize=100)


# model_gen = LdaSeqModel(corpus = corpus, time_slice=time_series, id2word = dictionary, num_topics = num_topics)
print 'model training finish'
model_gen.save(main_path + 'result/dtm_o_' + sys.platform + '_topic_' + str(para['num_topics']) + '.model')
print 'model saving finish'
#model1 = DtmModel.load('topic1.model')
#topics = model1.show_topic(topicid=0, time=0, topn=10)

#for i in range(10):
#    print pd.DataFrame(model.show_topic(topicid=i, time=1, topn=10))

#corpora.textcorpus.TextCorpus(5)
