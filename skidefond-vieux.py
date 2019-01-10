'''
Extraire information sur les conditions de ski de fond au Mont-Royal
À faire:
* lister toutes les possibilités
'''

import requests
from bs4 import BeautifulSoup
from sopel.module import commands, example

def ski():
    url_base = 'http://ville.montreal.qc.ca/portal/page?_pageid=7377,94551572&_dad=portal&_schema=PORTAL'

    # paramètres pour ski de fond (7) au Mont-Royal (81)
    num_parc = 81
    num_activite = 7

    # construire et effectuer la requête
    payload = {'id' : num_parc, 'sc' : num_activite}
    requete = requests.get(url_base, params = payload)

    # vérifier si la page existe
    if requete.status_code != 200:
        #print('Information non disponible')
        bot.say('Information non disponible')

    else:
        return(requete)

def soupe(requete):

    # faire la soupe
    page = BeautifulSoup(requete.text, 'html.parser')

    # extraire l'information pertinente
    section_info = page.find('div', {'class' : 'fiche_contenu'})
    nom_parc = section_info.find('h1').text

    section_pistes = section_info.find('div', {'class' : 'a_noter'})
    pistes = section_pistes.find_all('p')

    section_etat = section_info.find_all('h3')

    conditions = {'État des pistes de ski' : section_etat[0].text,
                  'Qualité de la neige' : section_etat[9].text,
                  'Enneigement' : section_etat[10].text,
                  #'Commentaires' : pistes[3].text
                  }

    return(nom_parc, conditions)


#@example('.skidefond montroyal')
@commands('skidefond')
def main(bot, trigger):
    requete = ski()
    nom_parc, conditions = soupe(requete)

    #print(nom_parc)
    bot.say(nom_parc)
    bot.say(conditions['État des pistes de ski'])
    bot.say(conditions['Qualité de la neige'])
    #bot.say(conditions['Enneigement'])
