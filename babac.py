import sys
import requests
from bs4 import BeautifulSoup
import mechanicalsoup as ms
#import sopel.module
#from sopel import web

#@sopel.module.commands('babac')
#def searchbabac(bot, trigger):
    #bot.say('Je cherche une piece sur le site de Babac')

browser = ms.Browser()

# Query
print('Searching for:', end=' ')
print(sys.argv[1])
#query =
query = sys.argv[1]

# Search
search = requests.get('http://cyclebabac.com/fr/', params='?s='+query)
searchpage = search.text
soupsearchpage = BeautifulSoup(searchpage, "html.parser")
itemsfound = soupsearchpage.findAll(attrs={'class': 'itemTitle'})

# Output of search
print('#Babac | Item name' )
for itemname in itemsfound:
    shortitemname = itemname.contents[1].string
    for itemlink in itemname.find_all('a'):
        #print(itemlink.get('href'))
        itempage = requests.get(itemlink.get('href'))
        itempagetext = itempage.text
        soupitempagetext = BeautifulSoup(itempagetext, "html.parser")
        skushort = str(soupitempagetext.find_all("span", attrs={"class": "sku"}))[34:40]
    print(skushort + ' | ' + shortitemname)
