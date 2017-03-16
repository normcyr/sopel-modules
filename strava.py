import sopel.module
import kudos as strava

@sopel.module.interval(600)

def check_for_new_activities:

    new_activities = False

    email, password, athlete_ids = strava.load_config()
    browser, csrf_token, feed_page = strava.login_strava(email, password)
    activities = strava.find_activities_from_feed_page(feed_page)

    if activities != None:
        new_activities = True

    return new_activities

def get_athlete_name(athlete_ids):

    for athlete in athlete_ids:
        athlete_url = urllib.request.Request(base_url + str(athlete), data=None, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'})
        athlete_page = urllib.request.urlopen(athlete_url)
        soup = BeautifulSoup(athlete_page, parser)
        athlete_name = soup.find('h1', attrs={'class': 'bottomless'}).get_text()

    return athlete_name, athlete_fav_activity

def retreive_activity_info(new_activities):

    athlene_name
    activity_title
    activity_type
    activity_distance

    return athlene_name, activity_title, activity_type, activity_distance

def publish_activity(bot, new_activities):
    '''Publish the new activiy that appeared on Strava'''

    retreive_activity_info()

    if new_activities = True:
        if '#test_sopel_norm' in bot.channels:
            bot.msg('#test_sopel_norm', "Activité terminée!")
