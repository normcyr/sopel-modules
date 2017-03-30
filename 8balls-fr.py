"""
8ball.py - Ask the magic 8ball a question
Copyright 2013, Sander Brand http://brantje.com
Licensed under the Eiffel Forum License 2.
http://sopel.dfbta.net

Translation to French by Norm Cyr http://github.com/normcyr
Possible answers in French found here: https://fr.wikipedia.org/wiki/Magic_8_Ball
"""

import sopel
import random

def get_random_comment():
    with open('/home/norm/.sopel/modules/liste-commentaires-boule-cristal.txt') as liste:
        listereader = liste.readlines()
        nb_commentaire = len(listereader)
    return(listereader, nb_commentaire)

@sopel.module.commands('8', 'boule', 'cristal', 'medium')
def ball(bot, trigger):
#if __name__ == '__main__':
    """Demande a la boule de cristal une question! Utilisation: .8 <question>"""
    listereader, nb_commentaire = get_random_comment()
    answer = random.randrange(0, nb_commentaire)
    bot.say(listereader[answer])
    #print(listereader[answer])
