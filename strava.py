#!/usr/bin/python3

'''
strava.py - strava activity module

author: Norm1 <normand.cyr@gmail.com>
found here: https://github.com/normcyr/sopel-modules
'''

import requests
from bs4 import BeautifulSoup
from sopel.module import commands, example

def fetch_new_activity(url):

    r = requests.get(url)
    if r.status_code == 200:
        return(r)
    else:
        print('URL error')

def make_soup(r):

    soup = BeautifulSoup(r.text, 'html.parser')

    return(soup)

def retreive_activity_info(soup):

    athlete_name  = soup.find('h2', {'class': 'bottomless'}).text.strip()
    activity_title = soup.find('div',  {'class': 'hgroup'}).text.strip()
    activity_type = soup.find('div', {'class': 'activity-type-date'}).find('strong').text.strip()
    activity_distance = soup.find('li', {'class': 'distance'}).find('strong').text.strip()
    activity_info = {'Name': athlete_name, 'Title': activity_title, 'Type': activity_type, 'Distance': activity_distance}

    return(activity_info)

@commands('strava')
@example('.strava https://www.strava.com/activities/1474462480')
def strava(bot, trigger):
    '''.strava <activity_url> - Retreive the Strava data from an activity. This assumes that the activity is public.'''

    url = trigger.group(2)
    #url = 'https://www.strava.com/activities/1474462480'

    try:
        r = fetch_new_activity(url)
        soup = make_soup(r)
        activity_info = retreive_activity_info(soup)

        bot.say('{} just did a {} {}.'.format(activity_info['Name'], activity_info['Distance'], activity_info['Type']))
        #print('{} just did a {} {}.'.format(activity_info['Name'], activity_info['Distance'], activity_info['Type']))

    except:
        return bot.say("No URL given")

#if __name__ == '__main__':
    #strava()
