from rake_nltk import Rake
r = Rake()
sample_file = open("C:/Users/champ/Documents/watchdocgit/Testdocuments/1#78.txt", 'r')
text = sample_file.read()
r.extract_keywords_from_text(text)
print(r.get_ranked_phrases())