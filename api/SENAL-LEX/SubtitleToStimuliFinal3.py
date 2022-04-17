# read in the subtitle  frequency file and add the data to dictionary where the key is the word form
import sys
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import json

IN = open("SENAL-LEX/data/FreqCorpus.txt") # abrimos el corpus del español
dictlist = {}

for w in IN:
    data = w.split()
    key, value = data[0], data[1:] # generamos un diccionario con las palabras más la frecuencia
    dictlist[key] = value
IN.close()

# read through the stimuli file and print out. Aquí debemos declararlo en el command line así: cat results/wordlist.txt | python3 SubtitleToStimuliFinal3.py
filename = sys.argv[1]
with open(filename) as file:
    text = file.readlines()

freqlist = []
for inline in text:
    inline = inline.strip()
    if inline not in dictlist:
        continue
    freq = dictlist[inline]
    freqlist.append((inline, freq))


x = list(zip(*freqlist))[0] # sacamos la información que necesitamos
y = list(zip(*freqlist))[1]
z = list(zip(*y))[1]

tokens = []
tokens2 = []
for i in x: # creamos las dos tablas
    data2 = i.split()
    data2 = i.strip()
    tokens.append(data2)


for y in z:
    data3 = y.split()
    data3 = y.strip()
    tokens2.append(data3)

cnt = 0

# Plot. Para hacer los gráficos necesitamos convertir los strings a floats.
num = [float(i) for i in z] # convertimos los strings a floats
mean = (sum(num)/len(num)) # generamos el promedio
#print("\nEl promedio de frecuencia global es:", round(mean), mean)

frecuencia = ('Lexicon')
promedio = [mean]

boxplot_data = [["Frequency", num]]
output = {"boxplot" : [{"data" : boxplot_data, "title" : 'Global Frequency in Spanish'}]}

print(json.dumps(output))