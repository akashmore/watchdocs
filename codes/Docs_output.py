# -*- coding: utf-8 -*-
import numpy as np
import pickle
from pymongo import MongoClient
from scipy import linalg,spatial

#terms=dict()
#documents=dict()
useful_keywords = list()
documents_list = list()

with open('useful_keywords.pkl', 'rb') as fp:
    useful_keywords=pickle.load(fp)

with open('useful_documents.pkl', 'rb') as fp:
    useful_documents=pickle.load(fp)

concept_terms=np.zeros((1,1))
concept_documents=np.zeros((1,1))

with open ('concept_terms.pkl', 'rb') as fp:
    concept_terms = pickle.load(fp)
	
with open ('concept_documents.pkl', 'rb') as fp:
    concept_documents = pickle.load(fp)	

useful_documents=list(useful_documents)
useful_keywords=list(useful_keywords)
	
'''with open('terms_dict.pkl', 'rb') as fp:
    terms=pickle.load(fp)

with open('docs_dict.pkl', 'rb') as fp:
    documents=pickle.load(fp)'''
	
print(useful_keywords)
print("These Keywords are available for querying")

query=raw_input("Enter your query:").split(" ")
print(query)

query_list=list()
for i in query:
	term_index=useful_keywords.index(i)
	query_list.append(list(concept_terms[term_index]))

query_arr=np.array(query_list)
query_arr=query_arr.sum(axis=0)
#print(query_arr)
#print(query_arr.shape)
#print(len(query_list))
#print(concept_documents[:,0].shape)
#print(len(query_list[0]))

#print(query_arr.shape)
query_arr=np.divide(query_arr,float(len(query)))
query_mag=np.linalg.norm(query_arr)
prob_dict=dict()	
i=0
#print(concept_documents[:,0].shape)
for i in range(len(useful_documents)):
	doc=concept_documents[:,i]
	doc_mag=np.linalg.norm(doc)
	prob=(np.dot(doc,query_arr))/float(query_mag*doc_mag)
	#prob=spatial.distance.cosine(query_arr,doc)
	prob_dict[useful_documents[i]]=prob
print(i)
prob_sorted = sorted(prob_dict, key=prob_dict.get, reverse=True)
#print(prob_sorted)
#print(prob_dict)
count=1
for item in prob_sorted:
	print(item,prob_dict[item])
	