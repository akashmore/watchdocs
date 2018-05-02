# -*- coding: utf-8 -*-
import numpy as np
import pickle
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['documents']
collection = db['useful_keywords']
collection2 = db['keyword_sources']
collection3 = db['keywords_occurences_document_two']

useful_keywords = set()
documents_list = set()
for document in collection2.find():
	keyword = document['keyword']
	sources_list = document['sources']
	length=len(sources_list)
	if length>=10 :
		useful_keywords.add(keyword)
		for document in sources_list:
			documents_list.add(document)
			
useful_keywords=sorted(useful_keywords)

useful_keywords=list(useful_keywords)
documents_list=list(documents_list)
mini_keywords=list()
mini_documents=list()


i=0
terms=len(useful_keywords)
while i<terms:
	mini_keywords.append(useful_keywords[i])
	i=i+1

	
i=0
documents=len(documents_list)
while i<documents:
	mini_documents.append(documents_list[i])
	i=i+1


'''print(mini_keywords)
print(mini_documents)
print(len(mini_keywords))
print(len(mini_documents))'''


w,h=documents,terms
TDMatrix=[[0 for x in range(w)] for y in range(h)]

i=0
count=0
while i<(documents):
	for document in collection3.find({"document":mini_documents[i]}):
		j=0
		keywords=document[u'keywords']
		occurences=document[u'occurences']
		#print(keywords)
		#print(occurences)
		while j<(terms):
			#print(mini_keywords[j])
			#print(j)
			if(mini_keywords[j] in keywords):
				#print(mini_keywords[j])
				#print(keywords.index(mini_keywords[j]))
				#print(occurences[keywords.index(mini_keywords[j])])
				TDMatrix[j][i]=occurences[keywords.index(mini_keywords[j])]+1
				count=count+1
			j=j+1
	i=i+1

with open('save.pkl', 'wb') as fp:
    pickle.dump(TDMatrix, fp)

TDMatrix2=[[0 for x in range(w)] for y in range(h)]	
with open ('save.pkl', 'rb') as fp:
    TDMatrix2 = pickle.load(fp)
'''for term in TDMatrix2:
	print(term)'''
#print(count)