import sopel.module

@sopel.module.commands('jaifaim')
@sopel.module.example('.jaifaim')
def jaifaim(bot, trigger):
    bot.say('Pas mon probl' + u'\u00E8' + 'me el\'gros.')
