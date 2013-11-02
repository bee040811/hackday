#!/usr/bin/python
# -*- coding: utf-8-*-
import urllib
import re
""" 連進資料庫START  """
"""
import MySQLdb as mdb 
import _mysql 
import xmlrpclib 
"""
""" 連進資料庫END    """
""" connect server  database    """
#con = mdb.connect('localhost', 'bee', '1234', 'train',charset='utf8') 
#cur = con.cursor() 
i = 1018
url = "http://www.ptt.cc/bbs/movie/index" + str(i) + ".html"
file = urllib.urlopen(url)
for lines in file.readlines():
    pat = re.compile('<a href="(/bbs.*)">(.*)</a>')
    title = re.findall(pat,lines)
    if(title):
        if(title[0][1].find("好雷") != -1):
            print "http://www.ptt.cc" + title[0][0]
        elif(re.search("負雷",title[0][1]) != -1):
            print "http://www.ptt.cc" + title[0][0]
            
