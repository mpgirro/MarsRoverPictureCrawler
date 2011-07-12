#!/usr/bin/python2.6

# MarsRoverPictureCrawler (mrpc): 
# A download bot for OPPORTUNITY and SPIRIT Mars Rover Pictures
#
# Copyright (C) 2011 by Maximilian Irro <maximilian.irro@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Please note that this license is for the software only. The picture material 
# the software collects is owned by Courtesy NASA/JPL-Caltech and released by 
# them under their JPL Image Use Policy. 
#
# For more information see the files README and LICENSE. Copys of them should 
# have reached you among with this program. If not, see the GitHub repository
# at http://github.com/mpgirro/MarsRoverPictureCrawler.git

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from os import system
import sys
from urllib2 import HTTPError, URLError

PIC_BASE = 'http://marsrover.nasa.gov/gallery/all/' 
GALLERY = 'http://marsrover.nasa.gov/gallery/all/%s_%s%03d_text.html' # %( ROVER, CAMERA, SOL)
PATH_BASE = 'mars_rovers/'
ROVERS = [ 'opportunity', 'spirit']
CAMERAS = [ 'f', 'r', 'n', 'p', 'm' ]
NAME_CODE = {
    'opportunity' : 'OPPORTUNITY',
    'spirit'      : 'SPIRIT',
    'f'           : 'Front Hazcam',
    'r'           : 'Rear Hazcam',
    'n'           : 'Navigation Camera',
    'p'           : 'Panoramic Camera',
    'm'           : 'Microscopic Imager'
}

def crawl(start, end, path=PATH_BASE):
	# crawls the NASA rover index from the sol 'start' to
	# the sol 'end'. the pictures will be downloaded to the
	# directory 'path'. default is PATH_BASE.
	
    if path is not PATH_BASE and path[-1] is not '/':
    	path = "%s/" %(path)
    
    for sol in range( start, end+1): 
        for rover in ROVERS:
            for cam in CAMERAS:
                gal = GALLERY % ( rover, cam, sol)
                pics = get_pictures( gal)
                load_pics( pics, path, rover, sol, cam)

def get_pictures(url):
	# scans a given url for links (a tag) and returns
	# a list of all hrefs leading to a .JPG file
	
    pics = []
    try:
        c = urllib2.urlopen( url )
    except HTTPError, e:
    	#print 'picture retrievel from %s failed because of %s' %(url,e)
        return pics

    soup = BeautifulSoup( c.read() )
    links = soup('a')
    for link in links:
        if 'href' in dict(link.attrs):
            if link['href'][-4:] == '.JPG':
                href = link['href']
                pics.append(href)
    return pics


def load_pics( pics, savepath, rover, sol, cam):
	# loads all pictures in pics to the directory given through
	# savepath/rover/sol/cam/. not yet existing directorys will be
	# created and download information printed to the standard 
	# outputstream. does not create directorys if pics is empty.

    if pics is None or len(pics) is 0:
        return 
    path = "%s%s/Sol %s/%s (%i img)" % (savepath, NAME_CODE[rover], sol, NAME_CODE[cam], len(pics) )
    system("mkdir -p '%s'" % (path) ) 
    c = 1
    for pic in pics:
        print 'loading %s (%i/%i) from %s at Sol %s to %s' % (NAME_CODE[cam], c, len(pics), NAME_CODE[rover], sol, path) 
        pic_url = "%s%s" % (PIC_BASE, pic)
        load_pic( pic_url, path)
        c += 1
	
def load_pic( pic, dir):
	# downloads and saves a picture to dir. the filename
	# of the picture is given through its url by calling
	# name(pic). odes nothing if the url is somehow invalid.

    try:
		opener = urllib2.build_opener()
		page = opener.open(pic)
		picpage = page.read()
		filename = "%s/%s" % ( dir, name(pic))
		fout = open(filename, "wb")
		fout.write(picpage)
		fout.close()
    except URLError:
    	return
	
def name(url):
	# returns the name of a picture in the provided url
	# by splitting the url at all '/' and returning the 
	# last part. it is not checked if this is a valid 
	# filename nor if it has a datatype appended.
	
    s = url.split("/")
    s.reverse()
    name = s[0]
    return name

if __name__ == '__main__':
	# command line arguments are: start_sol end_sol download_directory(optional)
    # default path is the current_directory/mars_rovers/..
    
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    path = sys.argv[3]
    crawl( start, end, path)