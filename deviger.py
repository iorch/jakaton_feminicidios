#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Detector de violencia de género en redes sociales. """

import csv
import io
import json
import os
import pandas as pd
import re
import Stemmer
import sys
import time
from collections import Counter


__author__ = "Miguel Salazar, Jorge Martínez, Fernando Aguilar"
__license__ = "GPL"
__version__ = "1.0"
__status__ = "Prototype"

def load_dataset(dataset):
	print("loading dataset...")

	path = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(path,"data",dataset)
	
	tweets = []
	with open(filename) as fin:
		reader = csv.reader(fin)
		for row in reader:
			tweet = row[0].split("_sep_")
			tweets.append(tweet[1])
	return tweets

# Gets a dictionary with the frequency count of each word in the corpus.
def tf_vector(txt, stopwords=None, emoticons=None, emojis=None):
	"""
	Transform a string into a Term-Frecuency dictionary
	:param txt: Text to process
	:param stopwords: A list of string of stopwords
	:param emoticons: A list of string of emoticons (see __main__ in this script)
	:param emojis: A list of string of emoticons (see __main__ in this script)
	:return: a dict object in the form {term=count}, with all terms preprocessed
	"""
	if stopwords is None:
		raise ValueError('You must provide a stopwords list')
	if emoticons is None:
		raise ValueError('You must provide an emoticons list')
	if emojis is None:
		raise ValueError('You must provide an emojis list')
	if not isinstance(txt, str):
		raise ValueError('txt must be a string')
 
	token_list = ['URL', 'EMAIL', 'MENTION', 'HASHTAG', 'NUMBER', 'EMOTICON', 'EMOJI']
 
	x = txt
	x = re.sub("(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]", " URL ", x)
	x = re.sub("^[_A-Za-z0-9-\\\\+]+(\\\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\\\.[A-Za-z0-9]+)*(\\\\.[A-Za-z]{2,})$", " EMAIL ", x)
	x = re.sub("@[A-Za-z0-9]+", " MENTION ", x)
	x = re.sub("#[A-Za-z0-9]+", " HASHTAG ", x)
	x = re.sub("\\d+(\\.\\d*)?°?", " NUMBER ", x)
	for em in emoticons:
		x = x.replace(em, ' EMOTICON ')
	for ej in emojis:
		x = x.replace(ej, ' EMOJI ')
	x = re.sub("[\\\"\\$%&@\\.,:;\\(\\)¿\\?`+\\-_\\*=!¡\\\\/#{}\\[\\]]", " ", x)
	x = re.sub("\\s+", " ", x)
	x = x.strip()
 
	words = x.split(' ')
	words_nonstop = [w for w in words if not w in stopwords]
	#words_nonstop_lower = words_nonstop
	words_nonstop_lower = [w.lower() if not w in token_list else w for w in words_nonstop]
 
	# TODO: How to detect language!?
	stemmer = Stemmer.Stemmer('spanish')
	words_nonstop_lower_stemmed = stemmer.stemWords(words_nonstop_lower)
 
	return dict(Counter(words_nonstop_lower_stemmed))


def main():
	print("DeViGeR")
	tweets = load_dataset("train.txt")

	stops = open('data/stopwords_spanish.txt').read().splitlines()
	emos = open('data/emoticons.txt').read().splitlines()
	emojis = pd.read_csv('data/emojis.csv')
	emoj = list(emojis['emoji'])

	bow = {}
	i = 1
	for tweet in tweets:
		print("tweet",i)
		vector = tf_vector(tweet, stopwords=stops, emoticons=emos, emojis=emoj)
		print(vector)
		for word in vector:
			if word in bow:
				bow[word] += vector[word]
			else:
				bow[word] = vector[word]
		i += 1
	print(bow)

if __name__ == '__main__':
	main()
  