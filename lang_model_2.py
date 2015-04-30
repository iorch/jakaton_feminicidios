import math
import os.path

import pickle

import glob
import nltk
from nltk.corpus.reader import XMLCorpusReader

import deviger


class LangModel:
    def __init__(self, order, alpha, sentences):
        self.order = order
        self.alpha = alpha
        if order > 1:
            self.backoff = LangModel(order - 1, alpha, sentences)
            self.lexicon = None
        else:
            self.backoff = None
            self.n = 0
        self.ngramFD = nltk.FreqDist()
        lexicon = set()
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            wordNGrams = nltk.ngrams(words, order)
            for wordNGram in wordNGrams:
                self.ngramFD[wordNGram] += 1
                # self.ngramFD.inc(wordNGram)
                if order == 1:
                    lexicon.add(wordNGram)
                    self.n += 1
        self.v = len(lexicon)

    def log_prob(self, ngram):
        return math.log(self.prob(ngram))

    def prob(self, ngram):
        if not self.backoff is None:
            freq = self.ngramFD[ngram]
            backoffFreq = self.backoff.ngramFD[ngram[1:]]
            if freq == 0:
                return self.alpha * self.backoff.prob(ngram[1:])
            else:
                return freq / backoffFreq
        else:
            # laplace smoothing to handle unknown unigrams
            return (self.ngramFD[ngram] + 1) / (self.n + self.v)


def train():
    """
    Creates a language model
    :return:
    """

    tweets_list = deviger.load_dataset('train.txt')

    sentences = []
    i = 0
    for tw in tweets_list:
        if i > 0 and i % 500 == 0:
            print("%d/%d tweet loaded, #-sentences: %d" % (i, len(tweets_list), len(sentences)))
        sentences.extend(nltk.sent_tokenize(tw))
        i += 1
    lm = LangModel(3, 0.4, sentences)

    pickle.dump(lm, open("lm.bin", "wb"))


def test():
    lm1 = pickle.load(open("lm.bin", 'rb'))

    tweets_list = deviger.load_dataset('test.txt')

    for line in tweets_list:
        sentences = nltk.sent_tokenize(line.strip())
        print("Tweet sentences:", sentences)
        for sent in sentences:
            words = nltk.word_tokenize(sent)
            word_trigrams = nltk.trigrams(words)
                sum_log_prob = 0
            for trigram in word_trigrams:
                logprob = lm1.log_prob(trigram)
                sum_log_prob += logprob
            print("(", sum_log_prob / len(words), ")")


def main():
    train()
    test()


if __name__ == "__main__":
    main()
