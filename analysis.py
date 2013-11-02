#!/usr/bin/env python
# -*- coding: utf-8-*-
import re
import json
from operator import itemgetter
""" 連進資料庫START  """
import MySQLdb as mdb 
import mosql
from mosql.query import *
from mosql.util import raw
import mosql.mysql
import _mysql 
import xmlrpclib 
""" 連進資料庫END    """
""" connect server  database    """
""" get movie list """
from movie_link_parser import getmovielist

""" crawl movie description"""
from crawl_a_movie import craw_a_movie


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
        # crawl a movie       
        movie_detail = craw_a_movie(movie_words[movie_name]['url'])
        for (type,value) in movie_detail.iteritems():
            movie_words[movie_name][type] = value
    file = open('movie.txt',"w")
    file.write(json.dumps(movie_words))
    """
    file = open('movie.txt',"r")
    movie_words= json.loads(file.read())
    """
    
    for movie in movie_words:
        movie_type = movie_words[movie]
        #tmp = sorted(movie_type['term'].items(), key=itemgetter(1),reverse=True)
        pat = re.compile("([0-9]*).([0-9]*)." )
        duration = re.findall(pat,movie_type['long']  )
        long = 0
        try :
            clock = int(duration[0][0])
            min = int(duration[0][1])
            long = clock * 60 * 60 + min * 60  
            print long
        except:
            print duration
        count = 0
        dict = {}
        for k, v in sorted(movie_type['term'].items(), key=lambda kv: kv[1], reverse=True):
            dict[k] = v
            count += 1
            if count >= 10 :
                break
        cur.execute(insert('movie_source',{ "movie_name":movie.decode("utf-8"),"movie_description":movie_type['description'].decode("utf-8"),"movie_url":movie_type['url'],"movie_duration":long,"movie_pic":movie_type['cover'],"word_json":json.dumps(dict),"good":movie_type["good"],"bad":movie_type['bad'],"cast":movie_type["cast"],"director":movie_type["director"]})) 
if __name__ == '__main__':         
    analysis()
