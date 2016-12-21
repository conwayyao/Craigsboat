#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 23:09:59 2016

@author: conway.yao
"""

scrape4 = ['Washington']
scrape5 = ['SouthCarolina']
scrape6 = ['Mississippi', 'Kentucky', 'Oregon', 'Missouri', 'Nebraska', 'Kansas', 'Arkansas']
states_to_scrape =  scrape4 + scrape5 + scrape6

import json
with open('states_list.json') as data_file:
    data = json.load(data_file)

f = open('scraper_log.txt', 'w')
import craigsboat_requests
for state in states_to_scrape:
    count = craigsboat_requests.scrape_locality(state, data[state])
    f.write('Completed '+str(state)+' with '+str(count)+' results\n')
f.close()
