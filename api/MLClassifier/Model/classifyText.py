import os
import tarfile
from simpletransformers.classification import ClassificationModel
import sys
import os
import nltk
import json

sentences = []

def unpack_model(model_name=''):
  tar = tarfile.open(f"MLClassifier/Model/{model_name}.tar.gz", "r:gz")
  tar.extractall()
  tar.close()

def main():
  # define hyperparameter
  train_args ={"reprocess_input_data": True,
               "fp16":False,
              "num_train_epochs": 10, 
              'overwrite_output_dir': True,
              'train_batch_size':  32,
              'max_seq_length': 128}

  # Create a ClassificationModel with our trained model
  model = ClassificationModel("bert", 'MLClassifier/Model/outputs', num_labels=6, args=train_args, use_cuda=False)

  class_list = ['Lower Beginner','Upper Beginner','Lower Intermediate','Upper Intermediate', 'Lower Advanced', 'Upper Advanced']

  if __name__ == '__main__':    
    predictions, raw_outputs = model.predict(sentences)
    prediction_values = list(map(lambda x: class_list[x], predictions))

    phrase_table_data = [["Phrase", "Predicted Level"]]
    for i in range(len(sentences)): # imprimimos
      phrase_table_data.append([sentences[i], prediction_values[i]])

    output = {
        'output' : {
            'table' : [{'data' : phrase_table_data, 'title' : 'Phrase Classification'}]
        }
    }
    print(json.dumps(output))

sentences = [sys.argv[1]]
os.environ["TOKENIZERS_PARALLELISM"] = "false"
main()