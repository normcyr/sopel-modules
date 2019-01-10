#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Extraire information sur les conditions de ski de fond à Montréal

Conditions de neige dans les grands parcs
Description du fichier ici: http://donnees.ville.montreal.qc.ca/dataset/conditions-ski/resource/5b19d41c-468d-4f37-b289-e9b044346615
Source XML: http://montreal2.qc.ca/ski/donnees/conditions_neige.xml'

Conditions de ski et sentiers en arrondissements (à implémenter - peut-être)
Description du fichier ici: http://donnees.ville.montreal.qc.ca/dataset/conditions-ski/resource/41721587-bfc4-4ea5-a8d9-2a7584d9979e
Source XML: http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_PISTE_SKI.xml'

À faire:
* possibilité de donner le nom du parc au lieu du numéro
* présenter les accumulations de neige etc.
* implémenter les conditions de ski et sentiers en arrondissements (peut-être)
'''

import requests
from bs4 import BeautifulSoup
from sopel.module import commands, example


def faire_requete_test(fichier_test):

    with open(fichier_test, 'r') as donnees:
        texte_xml = donnees.read()

    return(texte_xml)


def faire_requete(url_base):

    requete = requests.get(url_base)

    # vérifier si la page existe
    if requete.status_code != 200:
        #print('Information non disponible')
        bot.say('Information non disponible')

    else:
        texte_xml = requete.text

    return(texte_xml)


def faire_soupe(texte_xml):

    soupe = BeautifulSoup(texte_xml, 'xml')

    return(soupe)


def extraire_info_parc(infos_parc):

    nom_parc = infos_parc.find('nom_fr').text
    date_maj = infos_parc.find('date_maj').text
    pourcentage_trace = infos_parc.find('ski_piste_tracees_pourcent').text
    etat_conditions = infos_parc.find('etat_general').find('ski').find('etat').text

    reponse = {'nom parc': nom_parc, 'date de mise à jour': date_maj, 'pourcentage tracé': pourcentage_trace, 'état des conditions': etat_conditions}

    return(reponse)


def donner_reponse(reponse):

    print(reponse)


@commands('skidefond')
@example('.skidefond 6')
def main(bot, trigger):
    '''.skidefond <numéro du parc> - Donne les conditions de ski de fond d'un Parc-Nature de Montréal.'''
#def main():

    # fichier XML pour tester
    # fichier_test = 'conditions_neige.xml'
    # texte_xml = faire_requete_test(fichier_test)
    # no_parc = '6' # Mont-Royal

    url_base = 'http://montreal2.qc.ca/ski/donnees/conditions_neige.xml'
    texte_xml = faire_requete(url_base)
    soupe = faire_soupe(texte_xml)

    no_parc = trigger.group(2)
    if not no_parc:
        bot.say('J\'ai besoin d\'un numéro de parc pour vous aider. Par exemple: .skidefond 6 pour les conditions au Mont-Royal')
        return(bot.say('Index: 1=Bois-de-Liesse, 2=Île-Bizard, 3=Cap-Saint-Jacques, 4=Île-de-la-Visitation, 5=Pointe-aux-Prairies, 6=Mont-Royal'))

    infos_parc = soupe.find('parc', {'id': no_parc})
    reponse = extraire_info_parc(infos_parc)
    #donner_reponse(reponse)
    bot.say('{}: tracé à {}%, {}. Mis à jour {}'.format(reponse['nom parc'], reponse['pourcentage tracé'], reponse['état des conditions'], reponse['date de mise à jour']))


if __name__ == '__main__':
    main()
