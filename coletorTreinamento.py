#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from nltk.stem import *
from nltk import word_tokenize          
#from nltk.stem.porter import PorterStemmer
from elasticsearch import Elasticsearch
import time
import json
import pickle
import re
import string
import datetime

#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# declare
TRACK_TERMS=["preguica", "gordice", "sedentario", "sedentarismo", "estressado", "stress", "estresse", "doente", "peso", "acimadopeso", "perderpeso", "recreacao", "recreacional", "sedentarismo", "malhar", "academia", "praticoesporte", "esportista", "euatleta", "fitness", "atleta", "run", "running", "ciclismo", "correr", "alimentacao", "comerbem", "comidasaudavel", "dieta", "sedentarismo",  "yoga", "comidagorda", "projetoverao", "atividadefisica", "vidasaudavel", "exerciciofisico", "saudeebemestar", "saudeemfoco", "foconadieta", "emagrecimento", "emagrecercomsaude", "dietasemsofrer",  "qualidadedevida", "bemestar", "saudemental", "caminhada", "corridinha"]
PICKLE_FILE = "./treinamento/naivebayes.pickle"
CSV_NAME='training_set_full.csv'

# twitter config
ckey = ''
csecret = ''
atoken = ''
asecret = ''

stemmer = SnowballStemmer("portuguese", ignore_stopwords=True)
#stemmer = PorterStemmer()
now = datetime.datetime.now()


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    text = "".join([ch for ch in text if ch not in string.punctuation])
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

class listener (StreamListener):
	
	def on_connect(self):
		print("Connected to streaming server.")

	def on_data(self, data):
		try:
			
			dict_data = json.loads(data)
			raw_tweet = dict_data["text"]

			if not dict_data['retweeted'] and 'RT @' not in dict_data['text'] and '@' not in dict_data['text'] and 'https://t' not in dict_data['text']:
				words = tokenize(raw_tweet)
				tweet = ' '.join(words)

				saveFile = raw_tweet + " ::: " + tweet + " ::: " + str(now.strftime("%Y-%m-%d %H:%M")) + "\n"
				print saveFile
				
				output = open(CSV_NAME, 'a')
				output.write(saveFile)
				output.close

			return True
		except BaseException, e:
			print 'Failed ondata,', str(e)
			time.sleep(5)

	def on_error(self, status):
		print status
		return False

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

twitterStream.filter(track=TRACK_TERMS, languages=["pt"])
