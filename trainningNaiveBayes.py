#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

from textblob.classifiers import NaiveBayesClassifier
import pickle

TRAIN_FILE="./treinamento/training_set.csv"
TEST_FILE="./treinamento/training_set_test.csv"
PICKLE="./treinamento/naivebayes.pickle"

train = open(TRAIN_FILE, "r")
cl = NaiveBayesClassifier(train)
train.close()

test = open(TRAIN_FILE, "r")
print("Classifier accuracy percent:", (cl.accuracy(test))*100)
test.close()

saveClassifier = open(PICKLE, "wb")
pickle.dump(cl, saveClassifier)
saveClassifier.close()
