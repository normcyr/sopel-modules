#!/usr/bin/python
# -*- coding: utf-8 -*-

from sopel.module import commands, example
from sopel import web
from bs4 import BeautifulSoup
import cookielib
import mechanize
import yaml

def get_query(bot, trigger):
    query = trigger.group(2)

    return query

def load_config():
    with open('config.yml') as ymlfile:
        cfg = yaml.load(ymlfile)

    username = cfg['login']['username']
    password = cfg['login']['password']

    return username, password

def login(username, password):
    br = mechanize.Browser()
    login_url = "http://cyclebabac.com/wp-login.php"

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages? Uncomment this
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)

    # Perform the actual login
    br.open(login_url)
    br.select_form(nr=0)
    br.form['log'] = str(username)
    br.form['pwd'] = str(password)
    br.submit()

    return br

def search_item(br, query):
    url = "http://cyclebabac.com/"
    if query != None:
        search_url = url + '?s=' + query
    else:
        search_url = url
    search = br.open(search_url)
    searchpage = search.read()
    soupsearchpage = BeautifulSoup(searchpage, 'html.parser')
    itemsfound = soupsearchpage.findAll(attrs={'class': 'itemTitle'})

    return itemsfound

def print_results(bot, br, itemsfound):
    if len(itemsfound)>0:
        if 1 <= len(itemsfound) <= 10:
            bot.say('Returning %i items.' % len(itemsfound))
        elif len(itemsfound) > 10:
            bot.say('I found a lot of items. Returning the first 10 items.')
        bot.say('#Babac | ' + 'Item name'.ljust(50, ' ') + ' | Price' )
        for itemname in itemsfound:
            shortitemname = itemname.contents[1].string[:50]
            for itemlink in itemname.find_all('a'):
                itempage = br.open(itemlink.get('href'))
                itempagetext = itempage.read()
                soupitempagetext = BeautifulSoup(itempagetext, 'html.parser')
                skushort = str(soupitempagetext.find_all('span', attrs={'class': 'sku'}))[34:40]
                price = soupitempagetext.find('meta', itemprop='price')
                pricenumber = float(str(price[u'content']))
                val = str('%.2f') % pricenumber
            bot.say(skushort + ' | ' + shortitemname.ljust(50, ' ') + ' | ' + val.rjust(6) + ' $')
    else:
        bot.say('No product found :(')

@commands('babac')
@example('.babac training wheels')
def babac(bot, trigger):
    query = get_query(bot, trigger)

    if query != None:
        terms_searched = query
        query = query.replace(' ', '+')
        bot.say('Searching in the Babac catalog for: %s' % terms_searched)
    else:
        return bot.reply('.babac what? Please specify your query. For example ".babac training wheels"')
        exit(0)

    username, password = load_config()
    br = login(username, password)
    itemsfound = search_item(br, query)
    print_results(bot, br, itemsfound)
