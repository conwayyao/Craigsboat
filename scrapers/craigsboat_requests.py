# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 16:08:16 2016

@author: conway.yao
"""
import random
import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import os

# Change into CSV folder
os.listdir('./')
os.chdir('csv')

## Defines a function which scrapes all listings pages
def scrape_listings(endpt, locality_URL):
    
    # Search for trailing locality identifiers (e.g. 'miami.craigslist.org/brw'), which have different listing page URLs
    baseCLpattern = re.compile('.+org\/')
    splitURL = baseCLpattern.split(locality_URL)
    results_base = ''
    if splitURL[1] == '':
        results_base = 'https:' + locality_URL + 'search/boo'
    elif splitURL[1] != '':
        baseCL = re.search(baseCLpattern, locality_URL)
        results_base = 'https:' + baseCL.group() + 'search/' + splitURL[1] + 'boo'
    
    # Extract the section that contains the information for each listing
    r = requests.get(results_base + endpt)
    soup = BeautifulSoup(r.text, "lxml")
    links = soup.find_all('p', class_='result-info')

    # Call get_listings_info to extract each listing's info
    results = []
    for listing in links:
        results.append(get_listings_info(listing, locality_URL))
    
    return(results)
    
## Defines a function which extracts information from each listing on the listings page
def get_listings_info(listing, locality_URL):

    # Extract listing_url to pass to get_boat_info function
    listing_link = listing.find(class_='result-title hdrlnk').attrs['href']

    # If locality_URL has trailing locality (e.g. 'brw/'), strips that out
    baseCLpattern = re.compile('.+org\/')
    baseCL = re.search(baseCLpattern, locality_URL)
    locality_URL_2 = baseCL.group()
    
    locality_URL_3 = locality_URL_2[0:-1]  # Strips the extra '/' at end of locality_URL
    listing_base = 'https:' + locality_URL_3
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

    # Sleep 'for' loop for random seconds to prevent IP blocking
    
    # Return dictionary of info about a boat
    return(boat_info)

## Defines a function to extract info from a single listing page
def get_boat_info(listing_url):

    # Use BS4 to parse page
    r = requests.get(listing_url)
    bsoup = BeautifulSoup(r.text, "lxml")

    # Extract attributes and store into a dictionary
    boat_attrs= {}
    attrsoup = bsoup.find_all('p', class_='attrgroup')
    try:
        for attribute in attrsoup[0].find_all('span'):
            # Regex parsing to get just the attribute
            m = re.search('[^:]*', attribute.contents[0])
            # Add attribute into dictionary
            boat_attrs[m.group(0)] = attribute.contents[1].text
    except:
        pass

    # Extract description and join into one string
    description = []
    try:
        for string in bsoup.find(id='postingbody').stripped_strings:
            description.append(string)
        description = (' '.join(description[1:]))
    
        # Add description string into dictionary
        boat_attrs['description'] = description
    except:
        pass

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
    count = 0
    for key, value in locality_dict.items():   
        
        # Initialize a list that will contain the information about each listing that we collect
        results = []
        
        # Hardcode the possible listings page's endpoints
        results_endpoints = ['']
        # '?s=100', '?s=200', '?s=300', '?s=400', '?s=500']
        
        for endpoint in results_endpoints:
            start = time.time()
            results.extend(scrape_listings(endpoint, value))
            print(len(results))
            print(' results collected after scraping ' + endpoint + ' page of ' + key)
            end = time.time()
            
            # Time how long it takes to extract one page of results
            print('Runtime for this page of results: ' + str(end - start) + ' seconds')
            print('\n')
        
        # Convert results to pandas DataFrame and export as CSV with title constructed from state+locality+results
        resultsDF = pd.DataFrame(results)
        if len(resultsDF) > 10:
            output_file_title = state + '_' + key + '_results.csv'
            resultsDF.to_csv(output_file_title, encoding='utf-8')
            count = count+len(resultsDF)
        else:
            print('Failed '+state+key)
    return count
