import urllib
import sys
import json
import re

from BeautifulSoup import BeautifulSoup as Soup
import BeautifulSoup
from soupselect.soupselect import select

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

if __name__ == '__main__':
    url = "movie.html"
    print craw_a_movie(url)
