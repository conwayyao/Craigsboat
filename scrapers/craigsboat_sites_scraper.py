#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 22:03:40 2016

@author: conway.yao
"""

import requests 
from bs4 import BeautifulSoup 
import re  
import json

cl_sites_url = 'https://www.craigslist.org/about/sites'
k = requests.get(cl_sites_url)
ksoup = BeautifulSoup(k.text, 'lxml')

# Find all states/countries and store into list
state_list = []
states = ksoup.find_all('h4')
for raw_state in states:
    state = re.sub('\W', '', raw_state.text)
    state_list.append(state)

# Find the lists of localities under each state/country
localities = ksoup.find_all('ul')
# Delete the Craigslist footer
del(localities[140])

# Create a dictionary where the keys are the locality names and the values are the URLs, and append to locality_dicts_list
locality_dicts_list = []
for ul in localities:
    local = {}
    for region in ul.find_all('a'):
        local[re.sub('\W+', '_', region.text)] = region.attrs['href']
    locality_dicts_list.append(local)

# Combine state_list and locality_list together into one dictionary-of-dictionaries
sites = {}
sites = dict(zip(state_list, locality_dicts_list))

# Output to a JSON file
json_sites = json.dumps(sites)
f = open('states_list.json', 'w')
f.write(json_sites)
f.close()
