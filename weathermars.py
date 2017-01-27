# -*- coding: utf-8 -*-

import sopel.module
import json
import urllib2
from sopel.module import commands, example

degree_sign= u'\N{DEGREE SIGN}'

@commands('weathermars')
@example('.weathermars')
def weathermars(bot, trigger):
    weather_url = 'http://marsweather.ingenology.com/v1/latest/?format=json'
    weather_data = urllib2.urlopen(weather_url)
    data_json = json.load(weather_data)
    min_temp = data_json['report']['min_temp']
    max_temp = data_json['report']['max_temp']
    pressure = data_json['report']['pressure']/1000
    climate = data_json['report']['atmo_opacity']
    bot.say('Il fait un peu froid sur Mars aujourd\'hui: minimum %.1f %sC, maximum %.1f %sC' % (min_temp, degree_sign, max_temp, degree_sign))
    bot.say('La pression est de %.3f kPa, et les conditions climatiques sont %s' % (pressure, climate))
