import urllib
import sys
import json

from BeautifulSoup import BeautifulSoup as Soup
import BeautifulSoup
from soupselect.soupselect import select

def craw_a_movie(url):
    fd = urllib.urlopen(url)
    soup = Soup(fd)
    data = {}
    data["location"] = select(soup, 'h1')
    return data

if __name__ == '__main__':
    url = "cinema.html"
    print craw_a_movie(url)
