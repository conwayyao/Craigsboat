# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 16:08:16 2016

@author: conway.yao
"""

import requests
from bs4 import BeautifulSoup
import re

results_base= 'https://washingtondc.craigslist.org/search/boo'

r = requests.get(results_base)
soup = BeautifulSoup(r.text, "lxml")

links = soup.find_all('li', class_='result-row')

results = []

for listing in links[0:5]:
    
    listing_link = listing.find(class_ = 'result-title hdrlnk').attrs['href']
    listing_base = 'https://washingtondc.craigslist.org'
    listing_url = listing_base + listing_link
    
    boat_info = get_boat_info(listing_url)
    boat_info['price'] = listing.find(class_ = 'result-price').text
    boat_info['title'] = listing.find(class_ = 'result-title hdrlnk').text
    boat_info['id'] = listing.find(class_ = 'result-title hdrlnk').attrs['data-id']
    boat_info['url'] = listing_url



## Function to extract info from a single listing

def get_boat_info(listing_url):
    
    # Use BS4 to parse page
    r = requests.get(listing_url)
    bsoup = BeautifulSoup(r.text, "lxml")
    
    # Extract attributes and store into a dictionary
    boat_attrs= {}
    attrsoup = bsoup.find_all('p', class_='attrgroup')
    for attribute in attrsoup[0].find_all('span'):    
        # Regex parsing to get just the attribute
        m = re.search('[^:]*', attribute.contents[0])
        # Add attribute into dictionary
        boat_attrs[m.group(0)] = attribute.contents[1].text
    
    # Extract description and join into one string
    description = []
    for string in bsoup.find(id='postingbody').stripped_strings:
        description.append(string)
    description = (' '.join(description[1:]))
    
    # Add description string into dictionary
    boat_attrs['description'] = description

    # Return everything
    return(boat_attrs)
