# -*- coding:utf-8 -*-
import urllib
import sys
import json
import re
""" 連進資料庫START  """
import mosql
from mosql.query import *
import mosql.mysql
import MySQLdb as mdb 
import _mysql 
import xmlrpclib 
""" 連進資料庫END    """

from BeautifulSoup import BeautifulSoup as Soup
import BeautifulSoup
from soupselect.soupselect import select

time_data = {}

def craw_a_movie(url):
    fd = urllib.urlopen(url)
    soup = Soup(fd)
    data = {}
    raw = select(soup, '.dta')
    data['open'] = raw[0].string
    data['class'] = raw[1].string
    data['long'] = raw[2].string
    data['director'] = raw[3].string
    data['cast'] = raw[4].string
    for tmp in select(soup, '.border img')[0].attrs:
        if tmp[0] == 'src':
            data['cover'] = str(tmp[1])
            break
    raw = select(soup, '#ymvs .bd .full p')
    data['description'] = re.sub("<.*?>","",str(raw))
    return data

def get_cross_data():
    film_list = []
    area_list = []
    target = urllib.urlopen("http://tw.m.yahoo.com/w/twmovie/schedulesearch_bp.php?movieId=4883&areaId=6&__submit=%E6%9F%A5%E8%A9%A2")
    soup = Soup(target)
    options = select(soup, "select[name=movieId] option")
    for option in options:
        attrs = option.attrs
        try:
            for attr in attrs:
                if str(attr[0]) == 'value':
                    film_list.append(int(attr[1]))
        except:
            pass
    areas = select(soup, "select[name=areaId] option")
    for area in areas:
        attrs = area.attrs
        try:
            for attr in attrs:
                if str(attr[0]) == 'value':
                    area_list.append(int(attr[1]))
        except:
            pass
    film_list = [4883, 4954, 4951, 4851, 4948, 4731, 4924, 4913, 4925, 4908, 4886, 4946, 4912, 4936, 4901, 4903, 4915, 4850, 4940, 4941, 4919, 4904, 4899, 4833, 4878, 4875, 4911, 4807, 4914, 4768, 4891, 4837, 4887, 4868, 4839, 4848, 4803, 4828, 4869, 4855, 4844, 4863, 4865, 4861, 4822, 4818, 4808, 4767, 4753, 4812, 4700, 4778, 4733, 4584, 4687, 4765, 4769, 4789, 4723, 4526, 4772, 4648, 4587, 4796, 4223, 4694, 4365, 4521, 4470, 3941, 3026, 2924]
    #area_list =     [18, 16, 20, 22, 19, 13, 21, 10, 17, 11, 12, 14, 23]
    area_list =     [20,6,2,10]
    return film_list, area_list

def get_theater_list():
    """
    target = urllib.urlopen("http://www.ezding.com.tw/yahoo/mmb.do?campaign_code=yahoophone")
    soup = Soup(target)
    options = select(soup, '#cinemaId option')
    for option in options:
        print name
    """
    return [u"中影屏東影城",
    u"in89豪華數位影城",
    u"新民生戲院",
    u"信義威秀影城",
    u"京站威秀影城",
    u"日新威秀影城",
    u"板橋大遠百威秀影城",
    u"美麗華(大直影城)",
    u"華威天母影城",
    u"美麗華台茂",
    u"新竹大遠百威秀影城",
    u"新竹巨城威秀影城",
    u"台中老虎城威秀影城",
    u"台中新時代威秀影城",
    u"台中大遠百威秀影城",
    u"台南威秀影城",
    u"高雄威秀影城"]

def craw_out_time(i, j, url):
    """ connect server  database    """

    con = mdb.connect('localhost', 'root', '1234', 'hackday',charset='utf8') 
    cur = con.cursor() 

    target = urllib.urlopen(url)
    soup = Soup(target)
    html = select(soup, '.bd-container div.row')
    for segment in html:
        store = select(segment, "a")[0].string
        if  store in white_list:
            print store
            times = select(soup, '.mtcontainer span')
            for sec in times:
                second = time2sec(sec.string)
                #print insert('movie_time',{"movie_id":i,"theater":store,"area":j,"seconds":second})
                cur.execute(insert('movie_time',{"movie_id":i,"theater":store,"area":j,"seconds":second}))
                #print "[{0}:{1}:{2}]".format(i,j,second)
                # i movie yahoo id
                # j area theater
                # second time
            con.commit()

def time2sec(format_t):
    output = re.search(r"(\d*) : (\d*) ([A-Z]*)", format_t ).groups()
    if  output[2] == 'PM':
        hour = int(output[0])+12
    else:
        hour = int(output[0])
    second = int(output[1]) + hour*60
    return second

if __name__ == '__main__':
    white_list = get_theater_list()
    crossdata = get_cross_data();
    print crossdata
    ct=0
    for i in crossdata[0]:  #movie
        for j in crossdata[1]:  #area
            print ct
            url_tmpl = "http://tw.movie.yahoo.com/movietime_result.html?id={0}&area=(1)".format(i, j)
            craw_out_time(i, j, url_tmpl)
            ct+=1
