# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#coding:utf-8



#article
import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import sys
import signal

url_list = pd.read_csv("/mnt/c/Users/elara/Documents/url_data.csv")
content_list=[]
error_list=[]
time_out=3

def handler(signum, frame):
    raise AssertionError
    
for a in range(len(url_list)):
    page_url = url_list.iloc[a,0]
    sys.stdout.write(str(round(float(a)/float(len(url_list)),10))+ '   ' + str(len(error_list)) + '        ' + '\r')
    sys.stdout.flush()
    j=0
    succeed=0
    while succeed==0 and j<=3:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(time_out)#time_out为超时时间
            page_request = urllib2.Request(page_url)
            page_response = urllib2.urlopen(page_request)
            page_content = page_response.read()
            soup = BeautifulSoup(page_content,"html5lib")
            newscontents = soup.find("div", class_="newsContent").find_all('p')
            s=''
            for i in range(len(newscontents)):
                s = s + newscontents[i].get_text()
            content_list.append([s,url_list.iloc[a,2],url_list.iloc[a,1]])
            succeed=1
        except:
            succeed=0
            j=j+1
    if succeed==0:
        error_list.append(url_list.iloc[a,0])
        print "error"+str(j)
    

content_data = pd.DataFrame(content_list)

content_data.to_csv('/mnt/c/Users/elara/Documents/content_data.csv',encoding = 'utf-8')

error_data = pd.DataFrame(error_list)

error_data.to_csv('/mnt/c/Users/elara/Documents/error_data.csv',encoding = 'utf-8')

print 'done'




