#!/usr/bin/python
# -*- coding: utf-8-*-
import re
""" 連進資料庫START  """
import MySQLdb as mdb 
import mosql
from mosql.query import *
from mosql.util import raw
import mosql.mysql
import _mysql 
import xmlrpclib 

from movie_link_parser import getmovielist
""" 連進資料庫END    """
""" connect server  database    """

def analysis():
    con = mdb.connect('localhost', 'root', '1234', 'hackday',charset='utf8') 
    con.autocommit(1)
    cur = con.cursor()

    file = open('term','r')
    terms = file.read()
    data = terms.split(" ")
    movie_words = {}
    movie_list= getmovielist()
    for movie in movie_list:
        movie_name = movie
        if (movie_name not in movie_words) :
            movie_words[movie_name] = {}
            movie_words[movie_name]['term'] = {}
            movie_words[movie_name]['good'] = 0
            movie_words[movie_name]['bad'] = 0
            movie_words[movie_name]['url'] = movie_list[movie_name]
        # search movie name    
        cur.execute(select('ptt_movie',{"title like": "%"+ movie_name + "%"}))
        for ptt in cur.fetchall():
            for word in data:
                if( word not in movie_words[movie_name]['term']):
                    movie_words[movie_name]['term'][word] = 0
                title = ptt[4].encode("utf-8")
                times = title.count(word)
                movie_words[movie_name]['term'][word] += times
            if ptt[1] == 1:    # good
                movie_words[movie_name]['good'] += 1
            elif ptt[1] == 2:  # bad
                movie_words[movie_name]['bad'] += 1

    print movie_words                
if __name__ == '__main__':         
    analysis()
