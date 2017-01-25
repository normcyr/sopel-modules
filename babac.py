import sys
import requests
from bs4 import BeautifulSoup
import mechanicalsoup as ms
import sopel.module
from sopel import web

@sopel.module.commands('babac')

def search_babac(bot, trigger):
#def search_babac():

    query = trigger.group(2)
    if not query:
        return bot.reply('.babac what?')

    # Intro text
    bot.say('Searching in the Babac catalog for: %s' % query)
    bot.say('Return the 10 first items.')
    bot.say('#Babac | Item name' )

    # Query
    browser = ms.Browser()

    # Search
    search = requests.get('http://cyclebabac.com/fr/', params='?s='+query)
    searchpage = search.text
    soupsearchpage = BeautifulSoup(searchpage, "html.parser")
    itemsfound = soupsearchpage.findAll(attrs={'class': 'itemTitle'})

    # Output of search
    for itemname in itemsfound:
        shortitemname = itemname.contents[1].string
        for itemlink in itemname.find_all('a'):
            #print(itemlink.get('href'))
            itempage = requests.get(itemlink.get('href'))
            itempagetext = itempage.text
            soupitempagetext = BeautifulSoup(itempagetext, "html.parser")
            skushort = str(soupitempagetext.find_all("span", attrs={"class": "sku"}))[34:40]
        bot.say(skushort + ' | ' + shortitemname)
    return

#if __name__ == '__main__':
    #search_babac()
