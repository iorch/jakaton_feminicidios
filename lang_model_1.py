__author__ = 'fer'

import nltk

print("... build")
brown = nltk.corpus.brown
corpus = [word.lower() for word in brown.words()]

# Train on 95% f the corpus and test on the rest
spl = 95*len(corpus)/100
train = corpus[:spl]
test = corpus[spl:]

# Remove rare words from the corpus
fdist = nltk.FreqDist(w for w in train)
vocabulary = set(map(lambda x: x[0], filter(lambda x: x[1] >= 5, fdist.iteritems())))

train = map(lambda x: x if x in vocabulary else "*unknown*", train)
test = map(lambda x: x if x in vocabulary else "*unknown*", test)

print("... train")


from nltk.model import NgramModel
from nltk.probability import LidstoneProbDist

estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
lm = NgramModel(5, train, estimator=estimator)

print("len(corpus) = %s, len(vocabulary) = %s, len(train) = %s, len(test) = %s" % (len(corpus), len(vocabulary), len(train), len(test)))
print("perplexity(test) =", lm.perplexity(test))
