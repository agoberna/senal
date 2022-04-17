import sys
import re
import difflib
from collections import Counter
import json
from os.path import exists

def findFirstAlpha(line):
    i = 0
    while(not str.isalpha(line[i])):
        i += 1
    return i

def findNextSpace(line, start):
    i = start
    while(str.isalpha(line[i])):
        i += 1
    return i

def process(fpobj, filepath):
    words = []
    nouns = []
    verbs = []
    verbs_pres_ind = []
    verbs_pres_sub = []
    verbs_pret = []
    verbs_imp_ind = []
    verbs_imp_sub = []
    verbs_fut = []
    verbs_cond = []
    adj = []
    adv = []

    fp = open(fpobj, 'r')
    for sent in fp.read().split('\n\n'):
        sent_id = '' # the sentence id
        verbs_list = 0
        verbs_pres_list = 0
        verbs_pres_sub_list = 0
        verbs_imp_list = 0
        verbs_imp_sub_list = 0
        verbs_pret_list = 0
        verbs_fut_list = 0
        verbs_cond_list = 0
        nouns_list = 0
        adj_list = 0
        adv_list = 0
        others = 0
        word_list = 0
        glossary = ['casa', 'arbol']
        glossary_list = []

        if sent.strip() == '': # if there is no data in the sentence then skip it
            continue
        #for each of the lines in the sentence
        for line in sent.split('\n'):
            if line[0] =='#' or line.count("PUNCT"):
                continue
            start_i = findFirstAlpha(line)
            end_i = findNextSpace(line, start_i)
            word_list += 1
            words.append(line[start_i:end_i])
            

            if (re.findall('Tense=Pres', line)) and (re.findall('Mood=Sub', line)):
                verbs_list += 1
                verbs_pres_sub_list += 1

            if (re.findall('Tense=Pres', line)) and (re.findall('Mood=Ind', line)):
                verbs_list += 1
                verbs_pres_list += 1

            if line.count('Tense=Past'):
                verbs_list += 1
                verbs_pret_list += 1

            if (re.findall('Tense=Imp', line)) and (re.findall('Mood=Ind', line)):
                verbs_list += 1
                verbs_imp_list += 1

            if (re.findall('Tense=Imp', line)) and (re.findall('Mood=Sub', line)):
                verbs_list += 1
                verbs_imp_sub_list += 1

            if line.count('Tense=Fut'):
                verbs_list += 1
                verbs_fut_list += 1

            if line.count('Mood=Cnd'):
                verbs_list += 1
                verbs_cond_list += 1

            if line.count('NOUN'):
                nouns_list += 1

            if line.count('ADJ'):
                adj_list += 1

            if line.count('ADV'):
                adv_list += 1

        for x in range((nouns_list)):
            nouns.append(nouns_list)
        for x in range((verbs_list)):
            verbs.append(verbs_list)
        for x in range((verbs_pres_list)):
            verbs_pres_ind.append(verbs_pres_list)
        for x in range((verbs_pres_sub_list)):
            verbs_pres_sub.append(verbs_pres_sub_list)
        for x in range((verbs_imp_list)):
            verbs_imp_ind.append(verbs_imp_list)
        for x in range((verbs_imp_sub_list)):
            verbs_imp_sub.append(verbs_imp_sub_list)
        for x in range((verbs_pret_list)):
            verbs_pret.append(verbs_pret_list)
        for x in range((verbs_fut_list)):
            verbs_fut.append(verbs_fut_list)
        for x in range((verbs_cond_list)):
            verbs_cond.append(verbs_cond_list)
        for x in range((adj_list)):
            adj.append(adj_list)
        for x in range((adv_list)):
            adv.append(adv_list)

    fp.close()

    totals = [len(nouns), len(adj), len(adv), len(verbs)]
    verb_totals = [len(verbs_pres_ind), len(verbs_pres_sub), len(verbs_imp_ind),len(verbs_imp_sub), len(verbs_pret), len(verbs_fut), len(verbs_cond)]

    labels = ['Sustantivos', 'Adjetivos', 'Adverbios', 'Verbos']
    verb_labels = ["Presente de Indicativo", "Presente de Subjuntivo", "Imperfecto de Indiccativo", "Imperfecto de Subjuntivo", "Preterito de Indicativo", "Futuro Simple", "Condicional Simple"]

    # Load the vocabulary into the list "glossary"
    insertIndex = filepath.rindex('/')
    possibleVocabPath = filepath[0:insertIndex+1]+'vocab'+filepath[insertIndex+1:]

    if(exists(possibleVocabPath)):
        with open(possibleVocabPath, 'r') as f:
            for word in f:
                glossary.append(word.lstrip().rstrip().lower()) 
    else:
        with open('Stats/lists/VOCABULARY.txt', 'r') as f:
            for word in f:
                glossary.append(word.lstrip().rstrip().lower())

    f.close()

    # Check if the words from the text are in the "glossary"
    for i in words:
        if i in glossary:
            glossary_list.append(i)

    counter_obj = Counter(glossary_list)
    glossary_totals = counter_obj.most_common(min(20,len(list(counter_obj))))
    glossary_words, glossary_word_counts = zip(*glossary_totals) # Words from glossary used



    output = {
        'output' : {
            'pie' : [{'data' : {'totals' : totals, 'labels': labels}, 'title' : 'Word Breakdown'}, {'data' : {'totals' : verb_totals, 'labels' : verb_labels}, 'title': "Verb Breakdown"}],
            'bar' : [{'data' : {'y-value' : glossary_word_counts, 'x-value': glossary_words}, 'title' : 'Count of Glossary Words Used in Text'}]
        }
    }
    print(json.dumps(output))
