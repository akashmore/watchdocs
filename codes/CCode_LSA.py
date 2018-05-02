# -*- coding: utf-8 -*-
import numpy as np
import pickle
from pymongo import MongoClient
from scipy import linalg

client = MongoClient('localhost', 27017)
db = client['documents']
collection= db['useful_keywords']
collection2= db['useful_documents']

concept_terms=np.zeros((1,1))
concept_documents=np.zeros((1,1))

with open ('concept_terms.pkl', 'rb') as fp:
    concept_terms = pickle.load(fp)
	
with open ('concept_documents.pkl', 'rb') as fp:
    concept_documents = pickle.load(fp)
	
'''print(concept_terms)
print(concept_terms.shape)
print(concept_documents)
print(concept_documents.shape)'''

w1,h1=concept_terms.shape
w2,h2=concept_documents.shape

terms=dict()
documents=dict()
useful_keywords = set()
documents_list = set()

with open('useful_keywords.pkl', 'rb') as fp:
    useful_keywords=pickle.load(fp)

with open('useful_documents.pkl', 'rb') as fp:
    useful_documents=pickle.load(fp)

useful_keywords=list(useful_keywords)
useful_documents=list(useful_documents)

i=0
while i<w1:
	terms[useful_keywords[i]]=concept_terms[i]
	i=i+1

i=0
while i<h2:
	documents[useful_documents[i]]=concept_documents[:,i]
	i=i+1

#print(concept_terms.shape)
#print(concept_documents.shape)	
#print(terms)
#print(len(terms))
#print(documents)
#print(len(documents))

tmparr=np.array(concept_terms[0])
tmparr2=np.array(concept_documents[:,0])
#tmparr2=tmparr2.reshape((-1,1))
tmplist=list()
for i in documents:
	tmplist.append(i)
print(tmplist)
print(useful_documents)
'''count=1
i=0
for i in terms:
	print(i,terms[i])
	print(terms[i].shape,tmparr.shape)
	print(np.array_equal(terms[i],concept_terms[0]))
	print(np.array_equal(tmparr,concept_terms[0]))
	print(tmparr)
	count=count+1
	if(count==2):
		break
count=1
i=0
for i in documents:
	print(i,documents[i])
	print(documents[i].shape,tmparr2.shape)
	print(np.array_equal(documents[i],tmparr2))
	count=count+1
	if(count==2):
		break'''
'''print(type(terms))
print(type(documents))
with open('terms_dict.pkl', 'wb') as fp:
    pickle.dump(terms, fp)
with open('docs_dict.pkl', 'wb') as fp:
    pickle.dump(documents, fp)'''