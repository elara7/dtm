#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:35:25 2017

@author: elara
"""

# url

import requests
import time 

# 工作路径
if sys.platform == 'darwin':
    main_path = '/Users/wangzexian/Desktop/dtm/'
    dtm_path = main_path + 'lib/dtm/main_osx'
    fastdtm_path = main_path + 'lib/fastdtm/FastDTM_osx'
elif sys.platform == 'win32':
    main_path = 'D:/Desktop/dtm/' #win
elif sys.platform == 'linux2':
	main_path = '/mnt/d/Desktop/dtm/' 
	dtm_path = main_path + 'lib/dtm/main_linux'
	fastdtm_path = main_path + 'lib/fastdtm/FastDTM_linux'
else:
    print 'System does not meet'

print 'set path done'

headers = {
    'cache-control': "no-cache",
    'postman-token': "29d1ebbc-c4e1-f43f-1d99-e23ec20bec85"
    }

url = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx"

url_table=[]
#a=1
for a in range(1,266): #pages
    print('start scan page'+str(a))
    querystring = {"type":"SR","sty":"HGYJ","cmd":"4","code":"","ps":"50","p":str(a),"js":"var oCoQmllL={\"data\":[(x)],\"pages\":\"(pc)\",\"update\":\"(ud)\",\"count\":\"(count)\"}","rt":"50193681"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    rows_temp = response.text.split('"')[3:102]
    rows=[]
    for i in rows_temp:
        if i==',':
            continue
        else:
            rows.append(i)
            
    for b in rows: #row
        col=[]
        for c in b.split(','): #col
            col.append(c)
        url_table.append(col)

url_list=[]
for i in url_table:
    url_list.append(['http://data.eastmoney.com/report/' + time.strftime("%Y%m%d",time.strptime(i[0], "%Y/%m/%d %H:%M:%S")) + '/hg,' + i[1] + '.html',
                     i[0],i[5]])

import pandas as pd

url_data = pd.DataFrame(url_list)

url_data.to_csv(main_path + 'crawler/url_data.csv',index =False,encoding = 'utf-8')
