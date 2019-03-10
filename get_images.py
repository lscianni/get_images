#!/usr/bin/env python
# Scrapes all images off a page and save them to disk
#
# 04/23/2018
# Louis Scianni
"""
      Copyright (C) <year>  <name of author>

          This program is free software; you can redistribute it and/or modify
          it under the terms of the GNU General Public License as published by
          the Free Software Foundation; either version 2 of the License, or
          (at your option) any later version.

          This program is distributed in the hope that it will be useful,
          but WITHOUT ANY WARRANTY; without even the implied warranty of
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
          GNU General Public License for more details.

         You should have received a copy of the GNU General Public License along
         with this program; if not, write to the Free Software Foundation, Inc.,
         51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
         
         lscianniit@gmail.com
"""
import requests, os #, re
from urllib.parse import urlparse
from lxml import html
from sys import platform, argv

# Check what platform we are running on
if platform == 'linux' or platform == 'darwin':
    clear = 'clear'
elif platform == 'win32':
    clear = 'cls'

try:
    url = argv[1]
 
except IndexError: 
    # have the user tell us what url to scrape
    url = input('Enter a url(With http:// prefix): ')
    

def get_parsed_page(url):
    """ 
        Return the content of the websites from the url
        Then grab all the links and put them in a list
        also print out the status code and header for the site
    """
    sess = requests.Session()
    r0 = sess.get(url)
    parsed_page = html.fromstring(r0.content)                                      # parse the html on the page
    os.system(clear)
    print('Generating image list for %s' % url)
    image_paths = parsed_page.xpath('//img')                                       # find all the img tags
    print('\nHeader: \n',r0.headers, '\n', '\nStatus: ', r0.status_code, '\n')
    
    images = []                                                                     # initialize an empty list
    for src in image_paths:                                                         # for each src attribute append to the images list
        images.append(src.attrib['src'])
        
    return images

#get_parsed_page(url)
    
#print(get_parsed_page(url))

def save_images():
    """
    Save images from the parsed page with a return status of 'OK' to disk
    """
    
    # parse the url so we can split it up
    o = urlparse(url)

    #img_num = 0 # intialize image number
    
    for img in get_parsed_page(url): # for each image in the images list returned by get_parsed_page
        img_url = '%s://%s/%s' % (o.scheme, o.netloc, img)
        
        #header_content_value = requests.get(img_url).headers['content-type'] # get the 'content-type' header value
        
        #content = requests.get(img_url).headers['content-disposition']
        #file_name = re.findall('filename=(.+)', content)
        
        response = requests.get(img_url, stream=True)                        # Send get request for image path
        #print(response.headers['content-type'])
        file_name = img_url.split('/')[-1].split('#')[0].split('?')[0]
        with open("%s" % (file_name), 'wb') as handle: # Open a file for writing
            #print(response.headers['content-type'])
        
            if not response.ok:
                print('%s %s\n' % (img_url, response))
                
            elif response.ok:
                print('%s saved as %s\n' % (img_url ,handle.name))
                
                for block in response.iter_content(1024):                        # write image bytes to the file
                    if not block:
                        break
            
                    handle.write(block)
                    
        #img_num += 1 

if __name__ == '__main__':
    save_images()
