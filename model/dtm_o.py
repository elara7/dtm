# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 19:32:54 2017

@author: elara
"""

# create corpus 


import logging
from gensim import corpora
from gensim.models.wrappers.dtmmodel import DtmModel
#from gensim.models.ldaseqmodel import LdaSeqModel 
#import numpy as np
#from matplotlib import pyplot as plt
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.debug("test")


#参数
para={
	'num_topics':100,
	'mode':'fit',
	'model':'dtm',
	'id2word':None,
	'prefix':None,
	'lda_sequence_min_iter':6,
	'lda_sequence_max_iter':20,
	'lda_max_em_iter':10,
	'alpha':0.01,
	'top_chain_var':0.005,
	'rng_seed':0,
	'initialize_lda':True
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
		if key_para in ('lda_sequence_min_iter','lda_sequence_max_iter','lda_max_em_iter','rng_seed','initialize_lda'):
			para[key_para]=int(raw_input())
		elif key_para in ('alpha','top_chain_var'):
			para[key_para]=float(raw_input())
		elif key_para in ('mode','model'):
			para[key_para]=raw_input()

if para['initialize_lda'] ==0:
	para['initialize_lda'] = False
else:
	para['initialize_lda'] = True
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

model_gen = DtmModel(dtm_path, corpus=corpus, time_slices=time_series, mode=para['mode'], 
				 model=para['model'], num_topics=para['num_topics'], 
				 id2word=corpus.dictionary, prefix=None, 
				 lda_sequence_min_iter=para['lda_sequence_min_iter'], 
				 lda_sequence_max_iter=para['lda_sequence_max_iter'], 
				 lda_max_em_iter=para['lda_max_em_iter'], 
				 alpha=para['alpha'], 
				 top_chain_var=para['top_chain_var'], 
				 rng_seed=para['rng_seed'], 
				 initialize_lda=para['initialize_lda']
				 )

# model_gen = LdaSeqModel(corpus = corpus, time_slice=time_series, id2word = dictionary, num_topics = num_topics)
print 'model training finish'
model_gen.save(main_path + 'result/dtm_o_' + sys.platform + '_topic_' + str(para['num_topics']) + '.model')
print 'model saving finish'
#model1 = DtmModel.load('topic1.model')
#topics = model1.show_topic(topicid=0, time=0, topn=10)

#for i in range(10):
#    print pd.DataFrame(model.show_topic(topicid=i, time=1, topn=10))

#corpora.textcorpus.TextCorpus(5)