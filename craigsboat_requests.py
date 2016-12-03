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

# Initialize a list that will contain the information about each listing that we collect
results = []

# Manually list out each listings page's endpoint
results_endpoints = ['', '?s=100', '?s=200', '?s=300', '?s=400', '?s=500']


## Defines a function which scrapes all listings pages
def scrape_listings(page):
    results_base= 'https://poconos.craigslist.org/search/boo'
    r = requests.get(results_base + page)
    soup = BeautifulSoup(r.text, "lxml")
    
    # Extract the section that contains the information for each listing
    links = soup.find_all('p', class_='result-info')
    
    # Call get_listings_info to extract each listing's info
    for listing in links:
        get_listings_info(listing)


## Defines a function which extracts information from each listing on the listings page
def get_listings_info(listing):

    # Extract listing_url to pass to get_boat_info function
    listing_link = listing.find(class_='result-title hdrlnk').attrs['href']
    listing_base = 'https://poconos.craigslist.org'
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
    
    # Sleep 'for' loop for 0.75 seconds
    time.sleep(0.75)

    
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
    except:
        pass

    # Return the dictionary that contains the listing's information
    return(boat_attrs)
    

## Run the program!
for endpoint in results_endpoints:
    scrape_listings(endpoint)
    print(len(results))
    print (' collected after scraping ' + endpoint + ' page.')
    print('\n')


## Convert results to pandas DataFrame and export as CSV
resultsDF = pd.DataFrame(results)
resultsDF.to_csv('craigsboat_results_poconos.csv', encoding='utf-8')

    
