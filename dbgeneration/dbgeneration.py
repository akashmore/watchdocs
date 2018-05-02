from pymongo import MongoClient
import textrazor
import os
client = MongoClient('localhost', 27017)
mydb = client['watchdoc']
collection = mydb['doccat']
DOCUMENT_FOLDER='C://Users//champ//Documents//watchdocgit//Testdocuments//6451to100204'
textrazor.api_key = "0db9955a7bd9f0d9ac9f96a28c0093123b4546dd3bfff2cfd6f0f505"
client = textrazor.TextRazor(extractors=["entities", "topics"])
client.set_classifiers(["textrazor_newscodes"])
for filename in os.listdir(DOCUMENT_FOLDER):
    fileProcessed=0
    selectedFile=open(DOCUMENT_FOLDER+"/"+filename,"r")
    selectedFilePath=str(DOCUMENT_FOLDER+"/"+filename)
    print(filename)
    finalcat = []
    finalscore = []
    input_file = file(selectedFilePath).read().decode("utf-8")
    startLines = input_file[0:100]
    #print(startLines)
    response = client.analyze(input_file)
    entities = list(response.entities())
    entities.sort(key=lambda x: x.relevance_score, reverse=True)
    seen = set()
    keywords = list()
    info = list()
    for entity in entities:
        if entity.id not in seen:
            # print (entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)
            seen.add(entity.id)
            keywords.append(entity.id)
    mydb.keywords.insert({"keywords": keywords, "name": filename})
    print("--------------------------------------------")
    topiclist = list()
    for topic in response.topics():

        if topic.score > 0.3:
            # print (topic.label)
            topiclist.append(topic.label)
            mydb.topic.insert({"topic": topic.label})

    print("------------------------------------------------------")
    categorylist = list()
    try:
        for category in response.categories():
            alterLabel = (category.label).split(">")
            finalcat.append(alterLabel[-1])
            finalscore.append(category.score)

            k = finalcat[0]
            s = finalscore[0]

            # print(category.label)
            # print(alterLabel[-1])
            # print category.score
            categorylist.append(alterLabel[-1])
            mydb.category.insert({"category": alterLabel[-1]})
        mydb.doccat.insert({"classified": k, "Document": filename, "Score": s, "startLines": startLines})
        mydb.record.insert(
            {"name": filename, "description": [{"keywords": keywords, "topic": topiclist, "category": categorylist}]})
        output = "Category : " + str(k)
        print("recorded")
        print("---")
    except:
        print("unable")
        print("---")
        pass

