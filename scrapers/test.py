import requests

r=requests.get('https://lasalle.craigslist.org/boa/5921589978.html')
print(r.status_code)
print(r.text)
