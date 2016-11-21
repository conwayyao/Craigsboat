# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup

#this loops through every single listing of boats on the 492 pages
#limit = 492
#boat_id = 
#url = r'https://washingtondc.craigslist.org/search/boo?s='+limit
#while(limit!=492)
#{}


#TO DO: figure out how to return a list of all individual listing page IDs.
url = r'https://washingtondc.craigslist.org/search/boo?s=1'
html = urlopen(url)

listings = BeautifulSoup(html.read())

ids_raw=listings.findAll("a",'data-id')
print(ids_raw)



## everything below extracts the data from a SINGLE boat listing page
"""
url = r'https://washingtondc.craigslist.org/mld/bod/'+id+'.html'
html = urlopen(url)

bsObj= BeautifulSoup(html.read())

address_raw=bsObj.find(class_="mapaddress")

address=address_raw.text
print(address)

price=bsObj.find(class_="price")
print(price.text)

attributes=bsObj.find(class_="attrgroup")

print(attributes)


*this is our dictionary of information that we've extracted from the page

boatdict = {
"id": URL
"address": address
"price": price
}



##
TO DO: extract attributes: LOA, manufacturer, model name, and propulsion.
for child in attributes.children:
    print(child)
    print("break")
"""