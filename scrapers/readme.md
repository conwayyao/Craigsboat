This folder contains several scraper files:
- *craigsboat_requests.py* is the primary Craigslist scraper. It reads the states from states_list.json and executes a scrape for the states listed in scraper_caller.py
- *scraper_caller.py* is the primary scrape initiator. Open this file to specify what states are to be scraped by craigsboat_requests.py. It also logs completed scrapes to scraper_log.txt
- *states_list.json* is a static list of Craigslist localities in JSON format
- *craigsboat_sites_scraper.py* generates states_list.json
- *scraper_log.txt* is a text file that logs completed scrapes, by state.
- *test.py* tests a single Craigslist page to see if we are blocked.