#!/usr/bin/python3
import requests, string, unicodedata
from time import time
import json
import re
import nltk
from nltk import pos_tag,word_tokenize,sent_tokenize
from textblob import TextBlob
import pandas as pd

def remove_punc(sentence):
    return re.sub(r'[^\w\s]','',sentence).lower()

def get_sentiment(sentence):
	a = TextBlob(sentence)
	return round(a.sentiment[0],4)

def get_typology(sentence):
	"""
	takes word tokens as input
	returns a dictionary object with usefule nlp data
	"""
	def grammar_length():
		t = remove_punc(sentence)
		tt = pos_tag(word_tokenize(t))
		index_list = [tt.index(item) for item in tt]
		tag_list = [tag[1] for tag in tt]
		return zip(index_list,tag_list)

	def check_order(grammar_array):
		g = grammar_array
		nn = ['NN','NNS','PRP','NNP','PRP']
		vb = ['VB','VBD','VBZ','VBG','VBN']
		try:
			verb_ = [item[0] for item in g if item[1] in vb][0]
		except:
			verb_ = 0
		try:
			subject_ = [item[0] for item in g if item[1] in nn][0]
		except:
			subject_ = 0
		try:
			object_  = [item[0] for item in g if item[1] in nn][-1]
		except:
			object_ = 0
		group = [[subject_,'S'],[verb_,'V'],[object_,'O']]
		try:
			raw_order = sorted(group, key=lambda x: x[0])
		except:
			return {"typology":'UNK'}
		else:
			typepology = "".join([item[1] for item in raw_order])
		return typepology

	return check_order(grammar_length())


with open("games-corpus.txt", "r") as r:
	data = r.read()


class ProcessedText():

	def __init__(self):
		pass

	def get_word_tokens(self,g):
		return word_tokenize(g)

	def get_noun_count(self,g):
		nn = ['NN','NNS','PRP','NNP','PRP']
		c = [item[1] for item in g if item[1] in nn]
		return len(c)

	def get_verb_count(self,g):
		vb = ['VB','VBD','VBZ','VBG','VBN']
		v = [item[1] for item in g if item[1] in vb]
		return len(v)

	def result(self,text):
		grammar = pos_tag(word_tokenize(remove_punc(text)))
		words = self.get_word_tokens(remove_punc(text))
		op = {}
		op['Word Count'] = len(words)
		op['Nouns'] = self.get_noun_count(grammar)
		op["Verbs"] = self.get_verb_count(grammar)
		op["Typology"] = get_typology(text)
		op["Sentiment"] = get_sentiment(text)
		return op

def create_dataset(file_path,output_name="summary"):
	with open("games-corpus.txt", "r") as file:
		text = file.read()

	sentences = sent_tokenize(text)
	s_length = len(sentences)

	rows = []
	count = 0
	sut = ProcessedText()
	for s in sentences:
		print ("processing row {}".format(count))
		count += 1
		rows.append(sut.result(s))
	pass
	df = pd.DataFrame(rows)
	df.to_csv('csvs/{}-nlp-data.csv'.format(output_name), index=False, header=True)
	print (df.head(10))
	return

create_dataset("games-corpus.txt")

