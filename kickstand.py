import time
import requests
from bs4 import BeautifulSoup
import sopel.module

@sopel.module.commands('kickstand')
def kickstand(bot, trigger):
    comicbaseaddress = 'http://yehudamoon.com/comic/'
    today = time.strftime("%Y-%m-%d")
    request = requests.get(comicbaseaddress + today)

# Check if there is a new comic strip today
    if request.status_code == 200:
#        print('Web site exists')
        comicurl = comicbaseaddress + today + '/'
# If yes, print the link
#        print('The address is ' + comicurl)
	bot.say('Nouveau Kickstand Comics:' + ' | ' + comicurl)

# As of 2017-01-11, there is no title associated with the comic strip so I skipped that part.
# And print the title of the comic
#        html = BeautifulSoup(request.text, 'html.parser')
#        fulltitlenodate = html.title.text[11:]
#        where_dash = fulltitlenodate.find(' - ')
#        if where_dash == -1:
#            bot.say(fulltitlenodate + ' ' + comicurl)
#        bot.say('Nouveau Kickstand Comics:' + fulltitlenodate[:where_dash] + ' | ' + comicurl)

# If no, do nothing
    else:
        bot.say('Pas de Kickstand Comics aujourd\'hui.') 
