import requests
import json
import pandas as pd
from tf_vectorizer import tokenize, strim_space, stem
import logging


def is_female(word):
    return word.endswith('a') or word.endswith('as')


def is_male(word):
    return word.endswith('o') or word.endswith('os')


def gender_victim(text, emoticons=None, emoji=None, violent_dict_stemmed=None):
    """
    Dado un texto, trata de calcular el genero prevalente en  el texto
    :param text: Texto a detectar el genero
    :return: -1 si es masculino, 0 si es neutro, 1 si es femenino
    """
    x = tokenize(text, emoticons, emoji)
    x = strim_space(x)
    pos_uri = 'http://golem.iimas.unam.mx/pos/api/v1.0/tag/{0}'.format(x)
    pos_response = requests.get(pos_uri)
    pos_tags = json.loads(pos_response.content.decode('utf-8'))['POS']

    #logging.info('Entering gender_victim()')
    #logging.info(violent_dict_stemmed)

    male_occ = 0
    feme_occ = 0
    for i, tok in enumerate(pos_tags):
        w_stemmed = stem([tok[0]])[0]
        if w_stemmed in violent_dict_stemmed:
            logging.info('Found word {0}'.format(w_stemmed))
            if 0 < i < len(pos_tags) - 1:
                logging.info('Coincident: {},{},{}'.format(pos_tags[i-1][0], tok[0], pos_tags[i+1][0]))
                logging.info('Coincident: {},{},{}'.format(pos_tags[i-1][1], tok[1], pos_tags[i+1][1]))
                feme_occ += int(is_female(pos_tags[i-1][0]))
                feme_occ += int(is_female(pos_tags[i+1][0]))
                feme_occ += int(is_female(tok[0]))
                male_occ += int(is_male(pos_tags[i-1][0]))
                male_occ += int(is_male(pos_tags[i+1][0]))
                male_occ += int(is_male(tok[0]))
            elif i == 0:
                logging.info('Coincident: {},{}'.format(tok[0], pos_tags[i+1][0]))
                logging.info('Coincident: {},{}'.format(tok[1], pos_tags[i+1][1]))
                feme_occ += int(is_female(pos_tags[i+1][0]))
                feme_occ += int(is_female(tok[0]))
                male_occ += int(is_male(pos_tags[i+1][0]))
                male_occ += int(is_male(tok[0]))
            else:
                logging.info('Coincident: {},{}'.format(pos_tags[i-1][0], tok[0]))
                logging.info('Coincident: {},{}'.format(pos_tags[i-1][1], tok[1]))
                feme_occ += int(is_female(pos_tags[i-1][0]))
                feme_occ += int(is_female(tok[0]))
                male_occ += int(is_male(pos_tags[i-1][0]))
                male_occ += int(is_male(tok[0]))
    logging.info('Scores: M={}, F={}'.format(male_occ, feme_occ))

    return 0


if __name__ == '__main__':
    tweet1 = "Payne con \"Nebraska\", le hizo ganar a Dern, el premio a Mejor Actor en Cannes 2013Entérate de qué va aquí... http://t.co/lAOIBTpZVv"
    tweet2 = "Necesito una novia :( estoy de cursi"
    tweet3 = "RT @FrankGuevara92: Con @Just_edDs viendo peliculas. Que buen fin. http://t.co/H3hHA3jEv7"
    tweet4 = "RT @UnCrackMas: Real Madrid en 2014:✓17 partidos✓15 ganados✓2 empatados✓44 goles anotados✓6 recibidos¡INVENCIBLES! http://t.co/yR9fa…"
    tweet5 = "RT @seffh: STIRT-CTM-STyPS Conmemoran  Día Internacional de la Mujer Homenajeando a Mujeres Exitosas en Puebla @cocacastillo http://t.co/mw…"
    tweets = [tweet1, tweet2, tweet3, tweet4, tweet5]

    emos = open('data/emoticons.txt').read().splitlines()
    emoj = list(pd.read_csv('data/emojis.csv')['emoji'])
    dict = []

    for tw in tweets:
        gender_victim(tw, emos, emoj, dict)
