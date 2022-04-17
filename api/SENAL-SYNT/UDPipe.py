# This file is part of UDPipe <http://github.com/ufal/udpipe/>.
#
# Copyright 2016 Institute of Formal and Applied Linguistics, Faculty of
# Mathematics and Physics, Charles University in Prague, Czech Republic.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Requirement:
 pip install ufal.udpipe
 or
 python3.6 -m pip install ufal.udpipe
 or
 conda install -c conda-forge ufal.udpipe
"""
import sys
import ufal.udpipe
import json

class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, in_format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(in_format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % in_format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)

        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        """Parse the given ufal.udpipe.Sentence (inplace)."""
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""

        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()

        return output

# taken from: https://github.com/ufal/udpipe/blob/master/bindings/python/examples/udpipe_model.py
# Can be used as
if(len(sys.argv) < 2):
    print('Please input file-name as second argument')
    exit(0)
filepath = sys.argv[1]
filename = sys.argv[2]
filename = filename[0:filename.index('.')]
model = Model('SENAL-SYNT/es.udpipe')
ifile = open(filepath, mode='r', encoding='utf-8')
texto = ifile.read()
ifile.close()
sentences = model.tokenize(texto)
for s in sentences:
    model.tag(s)
    model.parse(s)
conllu = model.write(sentences, "conllu")

parsedFilePath = 'SENAL-SYNT/results/' + filename + 'parsed.collu'
print(parsedFilePath)

f=open(parsedFilePath,'w')
parsing= conllu # creamos el archivo txt para ser procesado por el script SubtitleToStimuliFinal3.py
f.writelines(parsing)
f.close()