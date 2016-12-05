# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 16:08:16 2016

@author: conway.yao
"""

import requests 
from bs4 import BeautifulSoup 
import re  
import time
import pandas as pd

## Scrapes Craiglist for all localities (e.g. 'washingtondc')
cl_sites_url = 'https://www.craigslist.org/about/sites'
k = requests.get(cl_sites_url)
ksoup = BeautifulSoup(k.text, 'lxml')

# Find all states/countries and store into list
state_list = []
states = ksoup.find_all('h4')
for raw_state in states:
    state = re.sub('\W', '', raw_state.text)
    state_list.append(state)

# Find the lists of localities under each state/country and store into list
localities = ksoup.find_all('ul')
# Delete the Craigslist footer
del(localities[140])

locality_dicts_list = []

# Create a dictionary where the keys are the locality names and the values are the URLs, and append to locality_dicts_list
for ul in localities:
    local = {}
    for region in ul.find_all('a'):
        local[re.sub('\W+', '_', region.text)] = region.attrs['href']
    locality_dicts_list.append(local)

# Combine state_list and locality_list together into one dictionary-of-dictionaries
sites = {}
sites = dict(zip(state_list, locality_dicts_list))

## Defines a function which scrapes all listings pages
def scrape_listings(page, locality_URL):
    results_base= 'https:' + locality_URL + 'search/boo'
    r = requests.get(results_base + page)
    soup = BeautifulSoup(r.text, "lxml")
    
    # Extract the section that contains the information for each listing
    links = soup.find_all('p', class_='result-info')
    
    # Call get_listings_info to extract each listing's info
    for listing in links:
        get_listings_info(listing, locality_URL)

## Defines a function which extracts information from each listing on the listings page
def get_listings_info(listing, locality_URL):

    # Extract listing_url to pass to get_boat_info function
    listing_link = listing.find(class_='result-title hdrlnk').attrs['href']
    listing_base = 'https:' + locality_URL
    listing_url = listing_base + listing_link

    # Pass listing_url to get_boat_info function, and get back a dictionary
    boat_info = get_boat_info(listing_url)

    # Populate dictionary with further information
    boat_info['title'] = listing.find(class_='result-title hdrlnk').text
    boat_info['id'] = listing.find(class_='result-title hdrlnk').attrs['data-id']
    boat_info['url'] = listing_url
    boat_info['date'] = listing.find(class_='result-date').attrs['datetime']
    try:
        boat_info['price'] = listing.find(class_ ='result-price').text
        boat_info['region'] = listing.find(class_='result-hood').text
    except:
        pass
    
    # Return dictionary into results list
    results.append(boat_info)
    
    # Sleep 'for' loop for 0.8 seconds to prevent IP blocking
    time.sleep(0.8)
    
## Defines a function to extract info from a single listing page
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

    # Extract coordinates of posting
    try:
        maplink = bsoup.find(target='_blank').attrs['href']
        boat_attrs['map_URL'] = maplink
        coords = re.findall('-?\d+\.\d+', maplink)
        boat_attrs['coord_pair'] = coords
        boat_attrs['lat'] = coords[0]
        boat_attrs['long'] = coords[1]
    except:
        pass

    # Return the dictionary that contains the listing's information
    return(boat_attrs)

## Define a function to run the program on a locality
def scrape_locality(state, locality_dict):    
    for key, value in locality_dict.items():   
        
        # Initialize a list that will contain the information about each listing that we collect
        results = []
        
        # Hardcode the possible listings page's endpoints
        results_endpoints = ['']
        #'?s=100', '?s=200', '?s=300', '?s=400', '?s=500']
        
        for endpoint in results_endpoints:
            start = time.time()
            scrape_listings(endpoint, value)
            print(len(results))
            print (' results collected after scraping ' + endpoint + ' page.')
            end = time.time()
            
            # Time how long it takes to extract one page of results
            print('Runtime for this page of results: ' + str(end-start) + ' seconds')
            print('\n')
        
        # Convert results to pandas DataFrame and export as CSV with title constructed from state+locality+results
        resultsDF = pd.DataFrame(results)
        output_file_title = state + '_' + key + '_results.csv'
        resultsDF.to_csv(output_file_title, encoding='utf-8')

## Define a function to run on a state
test = {'WashingtonDC': {'washingtondc':'//washingtondc.craigslist.org/'}}

def scrape_state(state_list):
    for key, value in state_list.items():
        scrape_locality(key, value)

scrape_state(test)