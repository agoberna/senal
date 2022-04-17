#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
createTrainDev.py

(C) 2021 by Damir Cavar, ...

Test the model with:

python testModel.py ...
"""


import spacy
import os


nlp = spacy.load(os.path.join("model", "model-best"))

def main(text):
    """ """
    if text:
        doc = nlp(text)
        print(doc.cats)


if __name__=="__main__":
    main("Hola!")

