import textrazor

textrazor.api_key = "f8656917eff9fdb7989aafbb22a8c8e1b74ebd076f1040c75de4dfcc"
client = textrazor.TextRazor(extractors=["entities", "topics"])
#client.set_cleanup_mode("cleanHTML")
client.set_classifiers(["textrazor_newscodes"])
input_file= open("upload/12#40.txt","r").read()
response = client.analyze(input_file)
entities = list(response.entities())
entities.sort(key=lambda x: x.relevance_score, reverse=True)
seen = set()
for entity in entities:
    if entity.id not in seen:
        print(entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)
        seen.add(entity.id)
print("--------------------------------------------")
for topic in response.topics():
    if topic.score > 0.3:
        print(topic.label)
print("------------------------------------------------------")
for category in response.categories():
    print(category.category_id, category.label, category.score)
