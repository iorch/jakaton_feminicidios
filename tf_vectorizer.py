import Stemmer
from collections import Counter
import os
import re
import pandas as pd


token_list = ['URL', 'EMAIL', 'MENTION', 'HASHTAG', 'NUMBER', 'EMOTICON', 'EMOJI']


def tokenize(txt, emoticons=None, emojis=None):
    if emoticons is None:
        raise ValueError('You must provide an emoticons list')
    if emojis is None:
        raise ValueError('You must provide an emojis list')

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
    x = re.sub(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+', ' EMOJI ', x)
    return x


def remove_punctuation(txt):
    x = re.sub("[\\\"\\$%&@\\.,:;\\(\\)¿\\?`+\\-_\\*=!¡\\\\/#{}\\[\\]]", " ", txt)
    return x


def strim_space(txt):
    """
    Strip and trim whitespace characters
    :param txt:
    :return:
    """
    x = txt.strip()
    x = re.sub("\\s+", " ", txt)
    return x


def lowercase(words_list):
    li = [w.lower() if not w in token_list else w for w in words_list]
    return li


def remove_stopwords(words_list, stopwords_list):
    words_nonstop = [w for w in words_list if not w in stopwords_list]
    return words_nonstop


def stem(words_list):
    # TODO: How to detect language!?
    stemmer = Stemmer.Stemmer('spanish')
    words_stemmed = stemmer.stemWords(words_list)
    return words_stemmed


def preprocess(txt, emoticons=None, emojis=None):
    x = tokenize(txt, emoticons=emoticons, emojis=emojis)
    x = remove_punctuation(x)
    x = strim_space(x)
    return x


