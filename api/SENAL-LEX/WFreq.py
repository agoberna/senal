import sys
import nltk
import seaborn as sns
import matplotlib.pyplot as plt
import math
import json

with open(sys.argv[1], 'r') as ifile: # abrimos el archivo. Aqui debemos declararlo en el command line asi: python3 Wfreq.py data/TestFile.txt
    text = ifile.read()
ifile.close()

# RUN NEXT TWO LINES ON SERVER
# nltk.download('punkt')
# nltk.download('stopwords')

text = text.lower() # Enter NLTK
myFD = nltk.FreqDist(text)

tokens = nltk.word_tokenize(text) # tokenization
tokens = [w.lower() for w in tokens]

# remove punctuation from each word
import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]

# remove remaining tokens that are not alphabetic
words = [word for word in stripped if word.isalpha()]

from nltk.corpus import stopwords # removing stop words
stop_words = set(stopwords.words('spanish'))
words = [w for w in words if not w in stop_words]

# Distribution
myTokenFD = nltk.FreqDist(words)

# relative frequency try. Hay que intentar incluir la freq. relativa a las tablas de palabras mas comunes.

total= float(sum(myTokenFD.values())) # relative frequency
total = int(total)


# Unigrams and Bigrams
# Unigrams
unigram_table_data = [["Token", "Frequency", "Relative Frequency"]]
for i in myTokenFD.most_common(20): # imprimimos
    unigram_table_data.append([i[0],i[1], (i[1]/total)])

# bigrams
myTokenBigrams = nltk.ngrams(words, 2)
bigrams = list(myTokenBigrams)
myBigramFD = nltk.FreqDist(bigrams)
totalbi= float(sum(myBigramFD.values())) # relative frequency
totalbi = int(totalbi)
#print("These are the 20 most common bigrams in the dataset:")
bigram_table_data = [["Bigram", "Frequency", "Relative Frequency"]]
for ngram in list(myBigramFD.most_common(20)): # imprimimos
    bigram_table_data.append([ngram[0][0] + ' ' + ngram[0][1], ngram[1], (ngram[1]/totalbi)])

bag = []
for token in list(myTokenFD.items()): # creamos una tabla con todas las palabras generadas
    bag.append(token[0])

wordlist_filepath = 'SENAL-LEX/results/' + sys.argv[2] + 'wordlist.txt'

f=open(wordlist_filepath,'w')
bag=map(lambda x:x+'\n', bag) # creamos el archivo txt para ser procesado por el script SubtitleToStimuliFinal3.py
f.writelines(bag)
f.close()

#PLOTS
#Unigrams
common_words = [word[0] for word in myTokenFD.most_common(20)]
common_counts = [word[1] for word in myTokenFD.most_common(20)]


common_bigrams = [bigram[0] for bigram in myBigramFD.most_common(10)]
common_bigrams = [' '.join(i) for i in common_bigrams] # use list comprehensio instead
bigram_counts = [bigram[1] for bigram in myBigramFD.most_common(10)]

output = {'output' : {
                'table' : [{'data' : unigram_table_data, 'title' : 'Unigram Frequency'}, {'data' : bigram_table_data, 'title' : 'Bigram Frequency'}],
                'bar' : [{'data' : {'y-value' : common_counts, 'x-value': common_words}, 'title' : 'Most Common Unigrams'}, {'data' : {'y-value' : bigram_counts, 'x-value' : common_bigrams}, 'title' : 'Most Common Bigrams'}]},
          'parsedPath' : wordlist_filepath}
print(json.dumps(output))
