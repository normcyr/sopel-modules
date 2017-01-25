import sys
import requests
from bs4 import BeautifulSoup
import mechanicalsoup as ms
import sopel.module
from sopel import web

@sopel.module.commands('babac')

def search_babac(bot, trigger):
#def search_babac():

    # Query
    #query = str(sys.argv[1])
    query = trigger.group(2)
    if not query:
        return bot.reply('.babac what? Please specify your query. For example ".babac Training wheels"')
    bot.say('Searching in the Babac catalog for: %s' % query)
    #print('Searching in the Babac catalog for: %s' % query)

    # Search
    browser = ms.Browser()
    search = requests.get('http://cyclebabac.com/fr/', params='?s='+query)
    searchpage = search.text
    soupsearchpage = BeautifulSoup(searchpage, "html.parser")
    itemsfound = soupsearchpage.findAll(attrs={'class': 'itemTitle'})

    # Output of search
    if len(itemsfound)>0:
        bot.say('Returning %i items.' % len(itemsfound))
        #print('Returning %i items.' % len(itemsfound))
        bot.say('#Babac | Item name' )
        #print('#Babac | Item name' )
        for itemname in itemsfound:
            shortitemname = itemname.contents[1].string
            for itemlink in itemname.find_all('a'):
                #print(itemlink.get('href'))
                itempage = requests.get(itemlink.get('href'))
                itempagetext = itempage.text
                soupitempagetext = BeautifulSoup(itempagetext, "html.parser")
                skushort = str(soupitempagetext.find_all("span", attrs={"class": "sku"}))[34:40]
            bot.say(skushort + ' | ' + shortitemname)
            #print(skushort + ' | ' + shortitemname)
    else:
        bot.say('No product found :(')
        #print('No product found :(')
    return

#if __name__ == '__main__':

    #search_babac()
