from flask import *
from flask import Flask, render_template
import os, sys, json, nltk, gensim, pickle
from gensim import corpora, models, similarities
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from flask import send_from_directory
from rake_nltk import Rake
import textrazor
# database connection
client = MongoClient('localhost', 27017)
mydb = client['watchdoc']
collection = mydb['doccat']
UPLOAD_FOLDER = 'C://Users//champ//Documents//watchdocgit//upload'
# UPLOAD_FOLDER='D:\\Study\\Final Year Sem 1\\Project\\watchdocs-master\\upload'

# start app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# index
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# upload file
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
       # print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #for checking file count and tran model
        fileCount = len([name for name in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], name))])
        if(fileCount%20==0):
            filelist = list()

            path = "C:\Users\champ\Documents\watchdocgit\Testdocuments"
            for file in os.listdir(path):
                filepath = path + '\\' + file
                f = open(filepath, 'r')
                filecontents = f.read()
                filecontents = filecontents.split()
                filelist.append(filecontents)
                f.close()
            model = gensim.models.Word2Vec(filelist, min_count=5, size=200, window=5, workers=4)
            model.save("modelfile")

    return redirect(url_for('categarize', filename=filename))


# categorize file
@app.route('/categarize/<filename>')
def categarize(filename):
    finalcat = []
    finalscore = []
    textrazor.api_key = "f8656917eff9fdb7989aafbb22a8c8e1b74ebd076f1040c75de4dfcc"
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    # client.set_cleanup_mode("cleanHTML")
    path = app.config['UPLOAD_FOLDER'] + '//' + filename
    client.set_classifiers(["textrazor_newscodes"])
    #input_file = file(path).read().decode("ISO-8859-1")
    input_file = file(path).read().decode("utf-8")
    r = Rake()
    r.extract_keywords_from_text(input_file)
    #print(r.get_ranked_phrases())
    startLines = input_file[0:100]
    #print(startLines)
    # os.system("LSA.py")
    response = client.analyze(input_file)
    entities = list(response.entities())
    entities.sort(key=lambda x: x.relevance_score, reverse=True)
    seen = set()
    keywords = list()
    info = list()
    for entity in entities:
        if entity.id not in seen:
            #print (entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)
            seen.add(entity.id)
            keywords.append(entity.id)
    mydb.keywords.insert({"keywords": keywords, "name": filename})
    print("--------------------------------------------")
    topiclist = list()
    for topic in response.topics():

        if topic.score > 0.3:
            #print (topic.label)
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

            print(category.label)
            # print(alterLabel[-1])
            # print category.score
            categorylist.append(alterLabel[-1])
            mydb.category.insert({"category": alterLabel[-1]})
        mydb.doccat.insert({"classified": k, "Document": filename, "Score": s, "startLines": startLines})
        mydb.record.insert(
            {"name": filename, "description": [{"keywords": keywords, "topic": topiclist, "category": categorylist}]})
        output = "Category : " + str(k)
        return jsonify(result=output)
    except:
        return jsonify(result="unable to categarize")


@app.route('/search', methods=['POST', 'GET'])
def search():
    jsonResultDocuments = {}
    docScore = {}
    resultdocuments = {}
    if request.method == 'POST':
        keyword = request.form['searchkeyword']
        keyword = keyword.lower()
        model = gensim.models.Word2Vec.load("modelfile")
        try:
            resultlist = model.most_similar(keyword)
        #print(resultlist)
            numberofresults = 7
        # print "Words similar to searched keyword are"
            for i in range(numberofresults):
                print resultlist[i][0]
                for document in collection.find():
                     category = document['classified'].lower()
                     if (keyword in category or category in keyword):
                        docScore[document['Document']] = document['Score'], document['startLines']
                        # print(docScore)
                     for i in range(len(resultlist)):
                        if (resultlist[i][0] in category or category in resultlist[i][0]):
                            docScore[document['Document']] = document['Score'], document['startLines']
                     # print(docScore)
                     for key, value in sorted(docScore.iteritems(), key=lambda (k, v): (v, k), reverse=True):
                            resultdocuments[key] = value[1]
        except:
              print("keywordnot found")
        jsonResultDocuments["files"] = resultdocuments
        if len(resultdocuments)==0:
            resultOutput = 0
        else:
            resultOutput = 1



        return redirect(url_for('searchResult',filejson=json.dumps(jsonResultDocuments),is_result = resultOutput))


@app.route('/searchResult/<filejson>/<is_result>')
def searchResult(filejson,is_result):
    # print(filejson)
    responejson = json.loads(filejson)
    fileArray = responejson["files"]
    show_result = is_result
    # print(fileArray)
    return render_template('search.html', files=fileArray,show_div=int(show_result))


# for reading files
@app.route('/fileread', methods=['GET', 'POST'])
def fileReading():
    if request.method == 'GET':
        requestFile = request.args.get('filename')
        return send_from_directory(app.config['UPLOAD_FOLDER'], requestFile)

#for donloading files
@app.route('/filedownload', methods=['GET', 'POST'])
def fileDownloading():
    if request.method == 'GET':
        downloadFile = request.args.get('filename')
        path = app.config['UPLOAD_FOLDER'] + '//' + downloadFile
        return send_from_directory(app.config['UPLOAD_FOLDER'], downloadFile)

# main function
if __name__ == '__main__':
    app.run(debug=True)
