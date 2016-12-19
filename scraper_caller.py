#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 23:09:59 2016

@author: conway.yao
"""
scrape1 = ['Maine', 'Florida', 'NewYork', 'California']
scrape2 = ['Pennsylvania', 'NewJersey', 'Virginia', 'Texas']
scrape3 = ['Maryland', 'Delaware', 'RhodeIsland', 'Michigan']
states_to_scrape = scrape1 + scrape2 + scrape3

import json
with open('states_list.json') as data_file:
    data = json.load(data_file)

import craigsboat_requests
for state in states_to_scrape:
    craigsboat_requests.scrape_locality(state, data[state])
