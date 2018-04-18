# -*- coding: utf-8 -*-
import nltk
import sys
import os
import pickle
import textrazor
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer	
from sklearn.decomposition import TruncatedSVD


reload(sys)
sys.setdefaultencoding('utf8')


'''textrazor.api_key = "f8656917eff9fdb7989aafbb22a8c8e1b74ebd076f1040c75de4dfcc"
client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_classifiers(["textrazor_newscodes"])
client.set_language_override("eng")'''


stopset=set(stopwords.words('english'))
stopset.update(['field','font','normal','rgb','style','family','letter','line','none','weight','times','new','strong','video','title','white','word','apple','class','br','amp','quot','field','font','0px','rgb'])


docList=list()
fileCount=1
dir_path='D:\Study\Final Year Sem 1\Project\Programs\WatchDocs\Test documents'
for filename in os.listdir(dir_path):
	file = open(dir_path+'\\'+filename,"r") 
	fileContents = file.read()
	stringOfText = fileContents
	stringOfText=stringOfText.lower()
	docList.append(stringOfText)
	fileCount+=1
	if(fileCount==101):
		break
#print(len(docList))


vectorizer= TfidfVectorizer(stop_words=stopset,use_idf=True,ngram_range=(1,3))
X=vectorizer.fit_transform(docList)
#print(X[0])
print(X.shape)
print(X[0].shape)


'''print(type(X))
with open('scimatrix.pkl', 'wb') as fp:
    pickle.dump(X, fp)'''
lsa=TruncatedSVD(n_components=2, n_iter=100)
lsa.fit(X)
#print(lsa.components_[0])


concept_terms=list()
concept_topics=list()
concept_categories=list()
terms=vectorizer.get_feature_names()
for i,comp in enumerate(lsa.components_):
	tmptopics=list()
	tmpcategories=list()
	termsInComp=zip(terms,comp)
	sortedTerms=sorted(termsInComp,key=lambda x: x[1], reverse=True)[:10]
	print("Concept %d:"%i)
	words_list=''
	count=0
	for term in sortedTerms:
		print(term[0])
		#words_list=words_list+str(term[0])+" "
	#words_list=words_list.decode("utf-8")
	#concept_terms.append(words_list)
	#print(words_list)
	#print(type(words_list))

	'''response = client.analyze(words_list)
	print("---Document topics---")
	for topic in response.topics():
		if(topic.score > 0.3):
			topic.label=topic.label.encode('utf-8')
			print topic.label
			tmptopics.append(topic.label)
	concept_topics.append(tmptopics)
	print("---Document categories---")
	for category in response.categories():
		print category.label,category.score
		tmpcategories.append(category.label)
	concept_categories.append(tmpcategories)
	print(" ")

with open("conceptterms.pkl",'wb') as fp:
	pickle.dump(concept_terms,fp)
with open("concepttopics.pkl",'wb') as fp:
	pickle.dump(concept_topics,fp)
with open("conceptcategories.pkl",'wb') as fp:
	pickle.dump(concept_categories,fp)'''

