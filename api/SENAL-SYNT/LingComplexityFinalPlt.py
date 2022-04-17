"""
text = Seguí andando por el mismo camino que me había solido.
1	Seguí	Seguí	ADV	_	_	2	advmod	_	_
2	andando	andar	VERB	_	VerbForm=Ger	0	root	_	_
3	por	por	ADP	_	_	6	case	_	_
4	el	el	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	6	det	_	_
5	mismo	mismo	ADJ	_	Gender=Masc|Number=Sing	6	amod	_	_
6	camino	camino	NOUN	_	Gender=Masc|Number=Sing	2	obl	_	_
7	que	que	SCONJ	_	_	10	mark	_	_
8	me	yo	PRON	_	Case=Acc,Dat|Number=Sing|Person=1|PrepCase=Npr|PronType=Prs	10	iobj	_	_
9	había	haber	AUX	_	Mood=Ind|Number=Sing|Person=3|Tense=Imp|VerbForm=Fin	10	aux	_	_
10	solido	solir	VERB	_	Gender=Masc|Number=Sing|Tense=Past|VerbForm=Part	6	acl:relcl	_	SpaceAfter=No
11	.	.	PUNCT	_	_	2	punct	_	_
"""
import sys
import matplotlib.pyplot as plt
import numpy as np
import fileinput
import json

# for each of the sentences in the file
v = []
w = []
aux = []
rel = []
adv = []
clauses = []
t = []
conj = []
numsent = 0

filename = sys.argv[1]

with open(filename) as file: 
    text = file.read()

for sent in text.split('\n\n'):
    sent_id = '' # the sentence id
    ntokens = 0 # number of words/tokens
    nverbs = 0
    naux = 0
    npunct = 0
    nrelclaus = 0
    finverb = 0
    nconj= 0
    tunits= 0
    advclaus = 0
    comp = 0
    numsent += 1
    if sent.strip() == '': # if there is no data in the sentence then skip it
        continue
    #for each of the lines in the sentence
    for line in sent.split('\n'):
        # if the line contains the string 'sent_id', then sent the sent id to be the part after the '='
        if line.count('sent_id') > 0:
            sent_id = line.split('=')[1].strip()
            # if the line doesn't start with a # then increment the number of words
        if line[0] !='#':
            ntokens += 1
        #row = line.split('\t')
        #if not row[1].outnum():
         #   npunct+=1
        if line.count('\tPUNCT\t') > 0:
            npunct += 1
        if line.count('\tVERB\t') > 0:
            nverbs +=1
        if line.count('\tAUX\t') > 0:
            naux +=1
        if line.count('\tacl:relcl\t') > 0:
            nrelclaus +=1
        if line.count('\tadvcl\t') > 0:
            advclaus += 1
        if line.count('\tccomp\t') > 0:
            comp += 1
        if line.count('\tVerbForm=Fin\t') > 0:
            finverb += 1
        if line.count('\tCCONJ\t') > 0:
            nconj += 1
        if line.count('\tconj\t') > 0 or line.count('\tparataxis\t'):
            tunits += 1

    t_units = tunits  + 1
    nwords = ntokens-npunct
    #nclauses = nverbs + naux + nrelclaus - infverb -conj
    nclauses = nrelclaus + advclaus + t_units

    # print out sentence id, number of words, and verbs per clause. This is for creating a table if desiredfor further analysis
    # print('%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d' % (sent_id, nwords, ntokens, npunct, nverbs, naux, nrelclaus, advclaus, nclauses, t_units, nconj))

# here we are attaching the numbers in the counters to specific lists.
    v.append(nverbs)
    w.append(nwords)
    aux.append(naux)
    rel.append(nrelclaus)
    adv.append(advclaus)
    clauses.append(nclauses)
    t.append(t_units)
    conj.append(nconj)

# print('sent_id','nwords', 'ntokens', 'npunct', 'nverbs', 'naux', 'nrelclaus', 'advclaus','nclaus', 't_units', 'nconj')
# creating floats for the plots
vnum = [float(i) for i in v]
vmean = (sum(vnum)/(numsent-1))
wnum = [float(i) for i in w]
wmean = (sum(wnum)/(numsent-1))
auxnum = [float(i) for i in aux]
auxmean = (sum(auxnum)/(numsent-1))
relnum = [float(i) for i in rel]
relmean = (sum(relnum)/(numsent-1))
advnum = [float(i) for i in adv]
advmean = (sum(advnum)/(numsent-1))
clausenum = [float(i) for i in clauses]
clausemean = (sum(clausenum)/(numsent-1))
tnum = [float(i) for i in t]
tmean = (sum(tnum)/(numsent-1))
conjnum = [float(i) for i in conj]
conjmean = (sum(conjnum)/(numsent-1))

#creating a nice printing table
average = [vmean, wmean, auxmean, relmean, advmean, clausemean, tmean, conjmean]
names = ["Verbs", "Words", "AUX", "Relative", "Adverbial", "Clauses", "T-Units", "Coordination"]
dct = {names[i]: average[i] for i in range(len(names))}

# print("\nThis is the mean frequency of the syntactic predictors")
# print("Measure:\t\tMean Frequency:")
table_data = [['Syntactic Predictor', 'Average']]
for k, v in dct.items():
    table_data.append([k,v])
#    print(k, '\t', v)

# attaching all the lists to a dataset without 'wnum'
boxplot_data = [["Verbs",vnum], ["AUXVerbs",auxnum], ["RelClauses",relnum], ["AdvClauses",advnum], 
                ["Clauses",clausenum], ["T-Units",tnum], ["Coordination",conjnum]]
output = {"table" : [{"data" : table_data, "title" : 'Mean Frequency Syntactic Predictors'}], "boxplot" : [{"data" : boxplot_data, "title" : "Syntactic Complexity"}]}
print(json.dumps(output))


