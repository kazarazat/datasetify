#!/usr/bin/python3
import re
import nltk
from nltk import pos_tag,word_tokenize,sent_tokenize
from textblob import TextBlob
import pandas as pd

def remove_punc(sentence):
    return re.sub(r'[^\w\s]',' ',sentence).lower()

def get_sentiment(sentence):
	a = TextBlob(sentence)
	return round(a.sentiment[0],4)

def get_typology(sentence):
	"""
	takes word tokens as input
	returns a dictionary object with useful nlp data
	"""
	def index_sent_tokens(sent):
		t = remove_punc(sentence)
		tt = pos_tag(word_tokenize(t))
		index_list = [tt.index(item) for item in tt]
		tag_list = [tag[1] for tag in tt]
		return zip(index_list,tag_list)

	sent_idx = list(index_sent_tokens(sentence))
	verb_tags = ['VB','VBD','VBZ','VBG','VBN']
	noun_tags = ['NN','NNS','PRP','NNP','PRP']
	typology = "UNK"

	try:
		subject_ = [item[0] for item in sent_idx if item[1] in noun_tags][0]
		object_ = [item[0] for item in sent_idx if item[1] in noun_tags][-1]
		verb_ = [item[0] for item in sent_idx if item[1] in verb_tags][0]
		if subject_ < verb_:
			typology = "SVO"
		if subject_ < object_:
			if object_ < verb_:
				typology = "SOV"
	except:
		typology = "-SVO"

	return typology

def categorize_length(word_count):
		if 0 < word_count < 12:
			return "short"
		if word_count > 20:
			return "long"
		else:
			return "medium"

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
		op['Sentence Length'] = categorize_length(len(words))
		op['Word Count'] = len(words)
		op['Nouns'] = self.get_noun_count(grammar)
		op["Verbs"] = self.get_verb_count(grammar)
		op["Typology"] = get_typology(text)
		#op["Sentiment"] = get_sentiment(text)
		return op

def create_dataset(file_path,output_name="summary"):
	with open(file_path, "r") as file:
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


def grammar_length(sentence):
	t = remove_punc(sentence)
	tt = pos_tag(word_tokenize(t))
	index_list = [tt.index(item) for item in tt]
	tag_list = [tag[1] for tag in tt]
	return zip(index_list,tag_list)


print(create_dataset('summary.txt'))

