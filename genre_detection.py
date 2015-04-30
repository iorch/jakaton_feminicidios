import requests
import json
import deviger
import pandas as pd


def detect_genre(text, emoticons=None, emoji=None, violent_dict=None):
    """
    Dado un texto, verificar si existe
    :param text: Texto a detectar el genero
    :return: -1 si es masculino, 0 si es neutro, 1 si es femenino
    """
    x = deviger.tokenize(text, emoticons, emoji)
    x = deviger.strim_space(x)
    pos_uri = 'http://golem.iimas.unam.mx/pos/api/v1.0/tag/{0}'.format(x)
    pos_response = requests.get(pos_uri)
    pos_tags = json.loads(pos_response.content.decode('utf-8'))['POS']
    violent_dict_stemmed = [deviger.stem([x])[0] for x in violent_dict]

    for i, tok in enumerate(pos_tags):
        w_stemmed = deviger.stem([tok[0]])[0]
        if w_stemmed in violent_dict_stemmed:
            if 0 < i < len(pos_tags) - 1:
                print(pos_tags[i-1][0], tok[0], pos_tags[i+1][0])
            elif i == 0:
                print(tok[0], pos_tags[i+1][0])
            else:
                print(pos_tags[i-1][0], tok[0])


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
        detect_genre(tw, emos, emoj, dict)
