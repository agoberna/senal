#pip install googletrans==3.1.0a0
#captura proto
import googletrans
from googletrans import Translator
import pandas as pd
import numpy as np
import nltk
import sklearn
import sys
from numpy import argmax
import json

sourcetext = sys.argv[1]

output_table = []

def translGenEn(text):
    translator = Translator()
    rv = translator.translate(text,dest='en')
    return(rv.text)

def translGenSp(text):
    translator = Translator()
    rv = translator.translate(text,dest='es')
    return(rv.text)

comptrans = translGenEn(sourcetext)
comptransback = translGenSp(translGenEn(translGenSp(comptrans)))
comparison = [sourcetext, comptrans, comptransback]

output_table.append(['Original Text', sourcetext])
output_table.append(['Re-translated text', comptransback])



# Preprocessing: https://github.com/makcedward/nlp/blob/master/sample/nlp-3_basic_distance_measurement_in_text_mining.ipynb
sourcetext_tokens = nltk.word_tokenize(sourcetext)
comptrans_tokens = nltk.word_tokenize(comptrans)
comptransback_tokens = nltk.word_tokenize(comptransback)


def transform(composition):
    tokens = [w for s in composition for w in s ]

    results = []
    label_enc = sklearn.preprocessing.LabelEncoder()
    onehot_enc = sklearn.preprocessing.OneHotEncoder()

    encoded_all_tokens = label_enc.fit_transform(list(set(tokens)))
    encoded_all_tokens = encoded_all_tokens.reshape(len(encoded_all_tokens), 1)

    onehot_enc.fit(encoded_all_tokens)

    for comp_tokens in composition:
        encoded_words = label_enc.transform(comp_tokens)

        encoded_words = onehot_enc.transform(encoded_words.reshape(len(encoded_words), 1))

        results.append(np.sum(encoded_words.toarray(), axis=0))

    return results

transformed_results = transform([
    sourcetext_tokens, comptrans_tokens, comptransback_tokens])

#Euclidean distance

for i, compo in enumerate(comparison):
    score = sklearn.metrics.pairwise.euclidean_distances([transformed_results[i]], [transformed_results[0]])[0][0]
    if(i == 2):
        output_table.append(['Euclidean Distance', '%.2f (Complete match = 0)' % (score)])

# Cosine similarities
for i, compo in enumerate(comparison):
    score = sklearn.metrics.pairwise.cosine_similarity([transformed_results[i]], [transformed_results[0]])[0][0]
    if(i == 2):
        output_table.append(['Cosine Distance', '%.2f (Complete match = 1)' % (score)])


#Jaccard Siilarities
"""
    Finding the posistion (from lookup table) of word instead of using 1 or 0
    to prevent misleading of the meaning of "common" word
"""

def calculate_position(values):
    x = []
    for pos, matrix in enumerate(values):
        if matrix > 0:
            x.append(pos)
    return x

"""
    Since scikit-learn can only compare same number of dimension of input.
    Add padding to the shortest sentence.
"""
def padding(sentence1, sentence2):
    x1 = sentence1.copy()
    x2 = sentence2.copy()

    diff = len(x1) - len(x2)

    if diff > 0:
        for i in range(0, diff):
            x2.append(-1)
    elif diff < 0:
        for i in range(0, abs(diff)):
            x1.append(-1)

    return x1, x2

y_actual = calculate_position(transformed_results[0])

for i, compo in enumerate(comparison):
    y_compare = calculate_position(transformed_results[i])
    x1, x2 = padding(y_actual, y_compare)
    score = sklearn.metrics.jaccard_score(x1, x2, average='weighted')
    if((i == 2)):
        output_table.append(['Jaccard Distance', '%.2f (Complete match = 1)' % (score)])

output = {
    'output' : {
        'table' : [{'data' : output_table, 'title' : 'Plagiarism Similarity Score'}]
    }
}
print(json.dumps(output))
