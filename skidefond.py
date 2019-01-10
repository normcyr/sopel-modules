#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Extraire information sur les conditions de ski de fond et de fatbike
dans les Parcs-Nature de la Ville de Montréal

Conditions de neige dans les grands parcs
---
Description du fichier ici: http://donnees.ville.montreal.qc.ca/dataset/conditions-ski/resource/5b19d41c-468d-4f37-b289-e9b044346615
Source XML: http://montreal2.qc.ca/ski/donnees/conditions_neige.xml'

Conditions de ski et sentiers en arrondissements (à implémenter - peut-être)
---
Description du fichier ici: http://donnees.ville.montreal.qc.ca/dataset/conditions-ski/resource/41721587-bfc4-4ea5-a8d9-2a7584d9979e
Source XML: http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_PISTE_SKI.xml'

À faire:
* possibilité de donner le nom du parc au lieu du numéro
* implémenter les conditions de ski et sentiers en arrondissements (peut-être)
'''


import requests
from bs4 import BeautifulSoup
from sopel.module import commands, example


def faire_requete():

    url_base = 'http://montreal2.qc.ca/ski/donnees/conditions_neige.xml'
    requete = requests.get(url_base)

    if requete.status_code != 200:
        return(bot.say('Information non disponible'))
    else:
        texte_xml = requete.text

    soupe = BeautifulSoup(texte_xml, 'xml')

    return(soupe)


@commands('skidefond')
@example('.skidefond 6')
def commande_skidefond(bot, trigger):
    '''.skidefond <numéro du parc> - Donne les conditions de ski de fond d'un Parc-Nature de Montréal.'''

    mode = 'skidefond'
    soupe = faire_requete()
    donner_reponse(bot, trigger, mode, soupe)


@commands('fatbike')
@example('.fatbike 6')
def commande_fatbike(bot, trigger):
    '''.fatbike <numéro du parc> - Donne les conditions pour la pratique du vélo à pneus surdimensionnés dans un Parc-Nature de Montréal.'''

    mode = 'fatbike'
    soupe = faire_requete()
    donner_reponse(bot, trigger, mode, soupe)


def donner_reponse(bot, trigger, mode, soupe):

    no_parc = trigger.group(2)
    liste_parcs = ['1', '2', '3', '4', '5', '6']

    if no_parc not in liste_parcs:
        return(bot.say('J\'ai besoin d\'un numéro de parc pour vous aider. Par exemple: .skidefond 6 pour les conditions au Mont-Royal. Index: 1=Bois-de-Liesse, 2=Île-Bizard, 3=Cap-Saint-Jacques, 4=Île-de-la-Visitation, 5=Pointe-aux-Prairies, 6=Mont-Royal'))

    info_parc = soupe.find('parc', {'id': no_parc})
    nom_parc = info_parc.find('nom_fr').text

    if mode == 'skidefond':

        pourcentage_trace = info_parc.find('ski_piste_tracees_pourcent').text
        etat_conditions = info_parc.find('etat_general').find('ski').find('etat').text

        enneigement = info_parc.find('enneigement').find('qualite').find('type').text
        nb_cm_neige = info_parc.find('enneigement').find('precipitations').find('nb_cm').text
        date_maj = info_parc.find('date_maj').text

        bot.say('{}: tracé à {}%, {}.'.format(nom_parc, pourcentage_trace, etat_conditions))
        bot.say('Type de neige: {}. Accumulation récente: {} cm. Mis à jour {}'.format(enneigement, nb_cm_neige, date_maj))

    if mode == 'fatbike':

        try:
            etat_fatbike = info_parc.find('fatbike').find('etat').text
            if etat_fatbike != 'non appliquable':
                bot.say('{}: conditions pour la pratique du fatbike: {}'.format(nom_parc, etat_fatbike))
            else:
                bot.say('{}: pas de fatbike ici!'.format(nom_parc))
        except:
            bot.say('{}: pas de fatbike ici!'.format(nom_parc))
