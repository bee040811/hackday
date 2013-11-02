import urllib
import sys
import json

from BeautifulSoup import BeautifulSoup as Soup
import BeautifulSoup
from soupselect.soupselect import select

def movie_link_parser(file_name,list):
    file_ob = urllib.urlopen(file_name)
    soup = Soup(file_ob)
    for out in select(soup, '.bd.vlist h4 a'):
        list[out.string.encode("utf-8")] = out['href']
        #s = BeautifulSoup.BeautifulSoup(out)
        #print s
        #print Soup(out)

if __name__ == '__main__':
    list = {}
    """
    movie_link_parser(sys.argv[1])
    print json.dumps(list, sort_keys=False, indent=4, separators=(',', ': '))
    """
    #pass url in
    try:
        movie_link_parser(sys.argv[1],list)
    except:
        url_base = "http://tw.movie.yahoo.com/movie_intheaters.html?p="
        for i in range(1,9):
            movie_link_parser(url_base+str(i),list)
        print json.dumps(list, sort_keys=False, indent=4, separators=(',', ': '))

def getmovielist():
    list = {}
    url_base = "http://tw.movie.yahoo.com/movie_intheaters.html?p="
    for i in range(1,9):
        movie_link_parser(url_base+str(i),list)
    return list
