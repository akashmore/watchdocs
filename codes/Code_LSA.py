# -*- coding: utf-8 -*-
import numpy as np
import pickle
from pymongo import MongoClient
from scipy import linalg

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
documents=len(useful_keywords)
#print(documents)
terms=len(documents_list)
#print(terms)

w,h=documents,terms
TDMatrix=[[0 for x in range(w)] for y in range(h)]
with open ('save.pkl', 'rb') as fp:
    TDMatrix = pickle.load(fp)
	
myarray=np.asarray(TDMatrix)
count=np.count_nonzero(myarray)
'''print(terms*documents)
print(count)
print(count/float(terms*documents))
i=0
j=0
count=0
while(i<terms):
	while(j<documents):
		if TDMatrix[i][j]>0:
			count=count+1'''
			
U, s, Vh = linalg.svd(myarray)
M,N = myarray.shape
Sig = linalg.diagsvd(s,M,N)
#print(U.shape)
#print(s.shape)
#print(Vh.shape)
#print(Sig)
#print(Sig.shape)

'''w1,h1=Sig.shape
i=0
while(i<w1):
	print(Sig[i][i])
	print(i)
	i=i+1'''
red_sig=Sig[:400,:400]
red_u=U[:,:400]
red_vh=Vh[:400,:]
'''w1,h1=red_sig.shape
i=0
while(i<w1):
	print(red_sig[i][i])
	print(i)
	i=i+1'''
'''print(red_sig)
print(red_u.shape)
print(red_sig.shape)
print(red_vh.shape)
'''
concept_terms=np.zeros(red_u.shape)
concept_documents=np.zeros(red_vh.shape)
for i in range(len(red_u)):
	for j in range(len(red_sig[0])):
		for k in range(len(red_sig)):
			concept_terms[i][j]+=red_u[i][k]*red_sig[k][j]
with open('concept_terms.pkl', 'wb') as fp:
    pickle.dump(concept_terms, fp)
for i in range(len(red_sig)):
	for j in range(len(red_vh[0])):
		for k in range(len(red_vh)):
			concept_documents[i][j]+=red_sig[i][k]*red_vh[k][j]
with open('concept_documents.pkl', 'wb') as fp:
    pickle.dump(concept_documents, fp)
print(concept_terms)
print(concept_terms.shape)
print(concept_documents)
print(concept_documents.shape)