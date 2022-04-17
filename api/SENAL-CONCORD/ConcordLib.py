import sys
import re

class color:
   CYAN = '\033[36m'
   END = '\033[0m'

def process(fpobj):
    fp = open(fpobj, 'r')
    print("---------------------------------------------------------------")
    for sent in fp.read().split('\n\n'):
        sent_id = '' # the sentence id

        if sent.strip() == '': # if there is no data in the sentence then skip it
            continue

        #for each of the lines in the sentence
        for line in sent.split('\n'):
            if line[0] !='#':
                noun = ""
                det = ""
                ngram = []
                referent = ""

                if re.findall('DET', line):
                    if (re.findall('Gender', line)) and (re.findall('Number', line)):
                        det = line.split("\t")[5]
                        referent = line.split("\t")[6]
                        ngram.append(line.split("\t")[1])
                        for line in sent.split('\n'):
                            if line[0] != '#':
                                if line.split("\t")[0] == referent:
                                    if re.findall('NOUN', line):
                                        noun = line.split("\t")[5]
                                        ngram.append(line.split("\t")[1])
                                        if noun not in det:
                                            print(color.CYAN, "Agreement error ->", color.END, ngram[0], ngram[1])


    fp.close()

    print("---------------------------------------------------------------")
