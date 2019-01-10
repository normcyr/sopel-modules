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
* faire choisir le parc
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

def extraire_info_parc(parc_individuel):

    nom_parc = parc_individuel.find('nom_fr').text
    date_maj = parc_individuel.find('date_maj').text
    pourcentage_trace = parc_individuel.find('ski_piste_tracees_pourcent').text
    etat_conditions = parc_individuel.find('etat').text

    reponse = {'nom parc': nom_parc, 'date de mise à jour': date_maj, 'pourcentage tracé': pourcentage_trace, 'état des conditions': etat_conditions}

    return(reponse)


def donner_reponse(reponse):

    print(reponse)


@commands('skidefond')
def main(bot, trigger):
#def main():

    # fichier XML pour tester
    # fichier_test = 'conditions_neige.xml'
    # texte_xml = faire_requete_test(fichier_test)

    url_base = 'http://montreal2.qc.ca/ski/donnees/conditions_neige.xml'
    texte_xml = faire_requete(url_base)

    soupe = faire_soupe(texte_xml)

    info_parcs = soupe.find_all('parc', {'id': '6'})
    for parc_individuel in info_parcs:
        reponse = extraire_info_parc(parc_individuel)
        #donner_reponse(reponse)
        bot.say('{}: tracé à {}%.'.format(reponse['nom parc'], reponse['pourcentage_trace']))


if __name__ == '__main__':
    main()
