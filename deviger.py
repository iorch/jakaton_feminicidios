#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Detector de violencia de género en redes sociales. """

import csv
import io
import json
import logging
import numpy as np
import os
import pandas as pd
import re
import Stemmer
import sys
import time
from collections import Counter, OrderedDict

__author__ = "Miguel Salazar, Jorge Martínez, Fernando Aguilar"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"

THRESHOLD = 0
DATAPATH = "data"
VIOLENT = "dict.txt"
TRAINING_SET = "train.txt"
STOPWORDS = "stopwords_spanish.txt"
EMOTICONS = "emoticons.txt"
EMOJIS = "emojis.csv"


def load_dataset(dataset):
	path = os.path.dirname(os.path.abspath(__file__))
<<<<<<< HEAD
	filename = os.path.join(path,DATAPATH,dataset)
	
=======
	filename = os.path.join(path,"data",dataset)
>>>>>>> 15b6d080a6de26f07556416e23a455a94c320646
	tweets = []

	with open(filename) as fin:
		reader = csv.reader(fin)
		for row in reader:
			tweet = row[0].split("_sep_")
			tweets.append(tweet[1])
	return tweets

<<<<<<< HEAD
def load_dictionary(dictionary):
	"""
	Loads the dictionary of violent words.
	:param dictionary: Dictionary filename. Must be placed in the /data directory.
	:return: The list of violent words that were loaded from the dictionary.
	"""
	path = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(path,DATAPATH,dictionary)
	
	dictlist = []
=======

def load_dictionary():
	filename = "data/dict.txt"
	dictionary = []
>>>>>>> 15b6d080a6de26f07556416e23a455a94c320646
	with open(filename) as fin:
		reader = csv.reader(fin)
		for word in reader:
			dictionary.append(word[0])
	return dictlist

<<<<<<< HEAD
def tf_vector(tweet):
=======

# Gets a dictionary with the frequency count of each word in the corpus.
def tf_vector(txt, stopwords=None, emoticons=None, emojis=None):
>>>>>>> 15b6d080a6de26f07556416e23a455a94c320646
	"""
	Transform a string into a Term-Frecuency dictionary
	:param tweet: Text to process
	:param stopwords: A list of string of stopwords
	:param emoticons: A list of string of emoticons (see __main__ in this script)
	:param emojis: A list of string of emoticons (see __main__ in this script)
	:return: a dict object in the form {term=count}, with all terms preprocessed
	"""
	path = os.path.dirname(os.path.abspath(__file__))
	stopwords = open(os.path.join(path,DATAPATH,STOPWORDS)).read().splitlines()
	emoticons = open(os.path.join(path,DATAPATH,EMOTICONS)).read().splitlines()
	emoj = pd.read_csv(os.path.join(path,DATAPATH,EMMOJIS))
	emojis = list(emoj['emoji'])
 
	token_list = ['URL', 'EMAIL', 'MENTION', 'HASHTAG', 'NUMBER', 'EMOTICON', 'EMOJI']

	x = tweet
	x = re.sub("(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]", " URL ", x)
	x = re.sub("^[_A-Za-z0-9-\\\\+]+(\\\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\\\.[A-Za-z0-9]+)*(\\\\.[A-Za-z]{2,})$", " EMAIL ", x)
	x = re.sub("@[A-Za-z0-9]+", " MENTION ", x)
	x = re.sub("#[A-Za-z0-9]+", " HASHTAG ", x)
	x = re.sub("\\d+(\\.\\d*)?°?", " NUMBER ", x)
	for em in emoticons:
		x = x.replace(em, ' EMOTICON ')
	for ej in emojis:
		x = x.replace(ej, ' EMOJI ')
	x = re.sub(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+', ' EMOJI ', x)
	x = re.sub("[\\\"\\$%&@\\.,:;\\(\\)¿\\?`+\\-_\\*=!¡\\\\/#{}\\[\\]]", " ", x)
	x = re.sub("\\s+", " ", x)
	x = x.strip()
 
	words = x.split(' ')
	words_nonstop = [w for w in words if not w in stopwords]
	words_nonstop_lower = [w.lower() if not w in token_list else w for w in words_nonstop]
 
	stemmer = Stemmer.Stemmer('spanish')
	words_nonstop_lower_stemmed = stemmer.stemWords(words_nonstop_lower)
 
	return dict(Counter(words_nonstop_lower_stemmed))

# Vector space model
def get_similarity(tw_vector, dict_vector):

	keys_tweet = set(tw_vector.keys())
	keys_dict = set(dict_vector.keys())
	intersection = keys_tweet & keys_dict

	num = 0
	for element in intersection:
		num += tw_vector[element] * dict_vector[element]

	if ( len(tw_vector) or len(dict_vector) ) == 0:
		return similarity = 0
	else:
		denA = 0
		for element in tw_vector:
			denA += tw_vector[element]**2
		denB = 0
		for element in dict_vector:
			denB += dict_vector[element]**2
		similarity = num/(denA*denB)

	return similarity


def main():
	print("DeViGeR")
	logging.basicConfig(level=logging.INFO)
	logging.info("Starting DeViGeR...")

	dictionary = load_dictionary(VIOLENT)
	tweets = load_dataset(TRAINING_SET)

	dict_vector = tf_vector(dictionary)
	d = []
	for tweet in tweets:
		tw_vector = tf_vector(tweet)
		similarity = get_similarity(tw_vector, dict_vector)
		if similarity >= THRESHOLD:
			gender_score = gender_victim(tweet)
			if gender_score > 0:
				d.append(tweet)
			
	#od = OrderedDict(sorted(d.items(), key=lambda t: t[1]), reverse=True)
	print(d)


if __name__ == '__main__':
	main()
