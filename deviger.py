#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Detector de violencia de género en redes sociales. """
from collections import Counter

import csv
import logging
import os
import pandas as pd

from gender_detection import gender_victim
from tf_vectorizer import preprocess, lowercase, remove_stopwords, stem


__author__ = "Miguel Salazar, Jorge Martínez, Fernando Aguilar"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"

THRESHOLD = 0.01
DATAPATH = "data"
VIOLENT = "dict.txt"
TRAINING_SET = "train.txt"
STOPWORDS = "stopwords_spanish.txt"
EMOTICONS = "emoticons.txt"
EMOJIS = "emojis.csv"


def load_dataset(dataset):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path,DATAPATH,dataset)
    filename = os.path.join(path,"data",dataset)
    tweets = []

    with open(filename) as fin:
        reader = csv.reader(fin)
        for row in reader:
            tweet = row[0].split("_sep_")
            tweets.append(tweet[1])
    return tweets

def load_dictionary(dictionary):
    """
    Loads the dictionary of violent words.
    :param dictionary: Dictionary filename. Must be placed in the /data directory.
    :return: The list of violent words that were loaded from the dictionary.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path,DATAPATH,dictionary)

    dictlist = []

    with open(filename) as fin:
        reader = csv.reader(fin)
        for word in reader:
            dictlist.append(word[0])
    return dictlist

# Vector space model
def get_similarity(tw_vector, dict_vector):
    keys_tweet = set(tw_vector.keys())
    keys_dict = set(dict_vector.keys())
    intersection = keys_tweet & keys_dict

    num = 0
    for element in intersection:
        num += tw_vector[element] * dict_vector[element]

    if len(tw_vector) == 0 or len(dict_vector)  == 0:
        # similarity = 0
        return 0
    else:
        denA = 0
        for element in tw_vector:
            denA += tw_vector[element]**2
        denB = 0
        for element in dict_vector:
            denB += dict_vector[element]**2
        similarity = num/(denA*denB)

    return similarity



def tf_vector(tweet, stopwords, emoticons, emojis):
    """
    Transform a string into a Term-Frecuency dictionary
    :param tweet: Text to process
    :param stopwords: A list of string of stopwords
    :param emoticons: A list of string of emoticons (see __main__ in this script)
    :param emojis: A list of string of emoticons (see __main__ in this script)
    :return: a dict object in the form {term=count}, with all terms preprocessed
    """
    x = preprocess(tweet, emoticons, emojis)

    words = x.split(' ')
    words = lowercase(words)
    words = remove_stopwords(words, stopwords_list=stopwords)
    words = stem(words)

    return dict(Counter(words))


def main():
    print("DeViGeR")
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting DeViGeR...")

    dictionary = load_dictionary(VIOLENT)
    dictionary_stemmed = [stem([x])[0] for x in dictionary]
    #print(dictionary)
    #print(dictionary_stemmed)

    tweets = load_dataset(TRAINING_SET)

    path = os.path.dirname(os.path.abspath(__file__))
    stopwords = open(os.path.join(path,DATAPATH,STOPWORDS)).read().splitlines()
    emoticons = open(os.path.join(path,DATAPATH,EMOTICONS)).read().splitlines()
    emojis = list(pd.read_csv(os.path.join(path,DATAPATH,EMOJIS))['emoji'])

    dict_vector = tf_vector(' '.join(dictionary), stopwords, emoticons, emojis)
    d = []
    for tweet in tweets:
        tw_vector = tf_vector(tweet, stopwords, emoticons, emojis)
        similarity = get_similarity(tw_vector, dict_vector)
        if similarity >= THRESHOLD:
            print(tweet)
            gender_score = gender_victim(tweet, emoticons=emoticons, emoji=emojis, violent_dict_stemmed=dictionary_stemmed)
            if gender_score > 0:
                d.append(tweet)

    #od = OrderedDict(sorted(d.items(), key=lambda t: t[1]), reverse=True)
    print(d)


if __name__ == '__main__':
    main()
