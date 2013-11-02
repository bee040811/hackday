#!/usr/bin/python
# -*- coding: utf-8-*-
import urllib
import re
from bs4 import BeautifulSoup
""" 連進資料庫START  """
import mosql
from mosql.query import *
import mosql.mysql
import MySQLdb as mdb 
import _mysql 
import xmlrpclib 
""" 連進資料庫END    """
""" connect server  database    """

con = mdb.connect('localhost', 'root', '1234', 'hackday',charset='utf8') 
con.autocommit(1)
cur = con.cursor() 
for i in range(500,1017):
    url = "http://www.ptt.cc/bbs/movie/index" + str(i) + ".html"
    file = urllib.urlopen(url)
    for lines in file.readlines():
        pat = re.compile('<a href="(/bbs.*)">(.*)</a>')
        title = re.findall(pat,lines)
        if(title):
            url = "http://www.ptt.cc" + title[0][0]
            name = title[0][1]
            page = BeautifulSoup( urllib.urlopen(url) ) 
            content = page.find(id="main-content")
            try :
                for match in content.findAll('div'):
                    match.replaceWith("")
                for match in content.findAll('span'):
                    match.replaceWith("")
                #data = " ".join(content.contents)
                if(title[0][1].find("好雷") != -1):
                    comment_type = 1
                elif(title[0][1].find("好雷") != -1):
                    comment_type = 2
                else :
                    comment_type = 3
                try :
                    content = re.sub("\n","",str(content))
                    content = re.sub("<.*?>","",str(content))
                    print insert('ptt_movie',{'comment_type':comment_type,'url':url,"title":name,"content":content})
                    cur.execute(insert('ptt_movie',{'comment_type':comment_type,'url':url,"title":name,"content":content}))
                except:
                    print("error\n")
            except:
                print("no span\n")
